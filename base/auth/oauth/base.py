from datetime import datetime, timedelta

from flask import url_for, request, flash, redirect
from flask_login import current_user
from flask_rauth import RauthOAuth2, RauthOAuth1
from flaskext.babel import lazy_gettext as _

from ..models import db, Key, User
from ..views import auth


class AbstractRAuth(object):

    client = None

    @property
    def name(self):
        raise NotImplementedError

    @property
    def options(self):
        raise NotImplementedError

    @classmethod
    def get_credentials(cls, response, oauth_token):
        raise NotImplementedError

    @classmethod
    def authorize(cls, response, oauth_token):
        next_url = request.args.get('next') or url_for('urls.index')
        if response is None or 'denied' in request.args:
            flash(_(u'You denied the request to sign in.'))
            return redirect(next_url)

        try:
            credentials = cls.get_credentials(response, oauth_token)
        except Exception:
            return redirect(next_url)

        if credentials.get('expires'):
            expires_in = timedelta(seconds=int(credentials['expires']))
            credentials['expires'] = datetime.now() + expires_in

        key = Key.query.filter(
            Key.service_alias == cls.name,
            Key.service_id == credentials['service_id'],
        ).first()

        user = current_user

        if key:

            if user.is_authenticated():
                key.user = user

            else:
                user = key.user

        else:
            if not user.is_authenticated():
                user = User(username=credentials['username'])
                user.generate_password()
                db.session.add(user)

            key = Key(
                service_alias=cls.name,
                user=user,
                service_id=credentials['service_id'],
                access_token=credentials['access_token'],
                secret=credentials.get('secret'),
                expires=credentials.get('expires'),
            )
            db.session.add(key)

        db.session.commit()
        auth.login(user)
        flash(_('Welcome %(user)s', user=user.username))
        return redirect(next_url)

    @classmethod
    def setup(cls, app):
        options = app.config.get('OAUTH_%s' % cls.name.upper())
        if not options:
            return False

        params = dict()
        if 'params' in options:
            params = options.pop('params')

        app.logger.info('Init OAuth %s' % cls.name)
        cls.options.update(name=cls.name, **options)
        client_cls = RauthOAuth2
        if cls.options.get('request_token_url'):
            client_cls = RauthOAuth1

        cls.client = client_cls(**cls.options)

        login_name = 'oauth_%s_login' % cls.name
        authorize_name = 'oauth_%s_authorize' % cls.name

        @app.route('/%s' % login_name, endpoint=login_name)
        def login():
            return cls.client.authorize(
                callback=(
                    url_for(authorize_name, _external=True,
                            next=request.args.get('next') or request.referrer)
                ), **params)

        cls.client.tokengetter_f = cls.get_token

        app.add_url_rule('/%s' % authorize_name,
                         authorize_name,
                         cls.client.authorized_handler(cls.authorize))

    @classmethod
    def get_token(cls):
        if current_user.is_authenticated():
            for key in current_user.keys:
                if key.service_alias == cls.name:
                    return key.access_token
