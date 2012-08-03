from flask import url_for, request, flash, redirect
from flask_login import current_user
from flaskext.babel import lazy_gettext as _
from flaskext.oauth import OAuth
from random import choice

from ..ext import db
from .models import User
from .views import users


ASCII_LOWERCASE = 'abcdefghijklmnopqrstuvwxyz'
PROVIDERS = 'twitter',
CLIENTS = dict()


oauth = OAuth()


def config_oauth(app):
    " Configure oauth support. "

    for name in PROVIDERS:
        config = app.config.get('OAUTH_%s' % name.upper())

        if not config:
            continue

        if not name in oauth.remote_apps:
            remote_app = oauth.remote_app(name, **config)

        else:
            remote_app = oauth.remote_apps[name]

        client_class = CLIENTS.get(name)
        client_class(app, remote_app)


class OAuthBase():
    name = 'base'

    def __init__(self, app, remote_app):
        remote_app.tokengetter_func = self.get_token

        def login():
            return remote_app.authorize(
                callback=(
                    url_for('authorize_%s' % self.name,
                            next=request.args.get('next') or request.referrer or None)))

        login_name = 'login_%s' % self.name
        app.add_url_rule('/%s' % login_name, login_name, login)

        authorize_name = 'authorize_%s' % self.name
        app.add_url_rule('/%s' % authorize_name,
                         authorize_name,
                         remote_app.authorized_handler(self.authorize))

    @staticmethod
    def get_token():
        if current_user.is_authenticated() and current_user.oauth_token:
            return current_user.oauth_token, current_user.oauth_secret

    def authorize(self, resp):
        pass


class OAuthTwitter(OAuthBase):
    name = 'twitter'

    def authorize(self, resp):
        next_url = request.args.get('next') or url_for('urls.index')
        if resp is None:
            flash(_(u'You denied the request to sign in.'))
            return redirect(next_url)

        user = current_user
        if not user.is_authenticated():
            user = User.query.filter(User.username == resp['screen_name']).first()

            if user is None:
                user = User(
                    username=resp['screen_name'],
                    pw_hash=''.join(choice(ASCII_LOWERCASE) for c in xrange(15)))
                db.session.add(user)

        user.oauth_token = resp['oauth_token']
        user.oauth_secret = resp['oauth_token_secret']
        db.session.commit()

        users.login(user)

        flash(_('Welcome %(user)s', user=user.username))
        return redirect(next_url)


CLIENTS['twitter'] = OAuthTwitter

# pymode:lint_ignore=F0401
