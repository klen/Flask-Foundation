from flask import Blueprint
from flask.ext.login import LoginManager, login_required, logout_user, login_user, current_user

from .models import User


class UserManager(Blueprint):

    def __init__(self, *args, **kwargs):
        self._login_manager = None
        super(UserManager, self).__init__(*args, **kwargs)

    def register(self, app, *args, **kwargs):
        if not self._login_manager:
            self._login_manager = LoginManager()
            self._login_manager.user_callback = self.user_loader
            self._login_manager.setup_app(app)
            self._login_manager.login_view = 'users.login'
            self._login_manager.login_message = u'You need to be signed in for this page.'

        super(UserManager, self).register(app, *args, **kwargs)

    @property
    def current(self):
        return current_user

    @staticmethod
    def user_loader(pk):
        return User.query.get(pk)

    @staticmethod
    def login_required(fn):
        return login_required(fn)

    @staticmethod
    def logout():
        return logout_user()

    @staticmethod
    def login(user):
        return login_user(user)
