import abc

from flask import url_for, request, flash, redirect
from flask_login import current_user
from flaskext.babel import lazy_gettext as _
from flask_rauth import RauthOAuth1

from ..ext import db
from .models import User
from .views import users


# Providers and default settings
PROVIDERS = dict(
    twitter=dict(
        base_url='http://api.twitter.com/1/',
        request_token_url='http://api.twitter.com/oauth/request_token',
        access_token_url='http://api.twitter.com/oauth/access_token',
        authorize_url='http://api.twitter.com/oauth/authorize',
    )
)


def config_rauth(app):
    " Config rauth instances. "

    for name, options in PROVIDERS.iteritems():
        config = app.config.get('OAUTH_%s' % name.upper())

        if not config:
            continue

        options.update(config)
        app.logger.info('Init OAuth %s' % name)

        cls = PROVIDERS[name].pop('cls')
        cls(app, name=name, **options)


class RauthBase(object):

    rauth = RauthOAuth1

    __meta__ = abc.ABCMeta

    def __init__(self, app, **options):

        client = self.rauth(**options)

        login_name = 'login_%s' % client.name
        authorize_name = 'authorize_%s' % client.name

        @app.route('/%s' % login_name, endpoint=login_name)
        def login():
            return client.authorize(
                callback=(
                    url_for(authorize_name, _external=True,
                            next=request.args.get('next') or request.referrer)
                ))

        app.add_url_rule('/%s' % authorize_name,
                         authorize_name,
                         client.authorized_handler(self.authorize))

        client.tokengetter_f = self.get_token

    @staticmethod
    def get_token():
        if current_user.is_authenticated() and current_user.oauth_token:
            return current_user.oauth_token, current_user.oauth_secret

    @abc.abstractmethod
    def authorize(self, resp, oauth_token):
        pass


class RauthTwitter(RauthBase):

    def authorize(self, resp, oauth_token):
        next_url = request.args.get('next') or url_for('urls.index')
        if resp is None or resp == 'access_denied':
            flash(_(u'You denied the request to sign in.'))
            return redirect(next_url)

        user = current_user
        if not user.is_authenticated():
            user = User.query.filter(
                User.username == resp.content['screen_name']).first()

            if user is None:
                user = User(username=resp.content['screen_name'])
                user.generate_password()
                db.session.add(user)

        user.oauth_token, user.oauth_token_secret = oauth_token
        db.session.commit()

        users.login(user)

        flash(_('Welcome %(user)s', user=user.username))
        return redirect(next_url)

PROVIDERS['twitter']['cls'] = RauthTwitter

# pymode:lint_ignore=F0401
