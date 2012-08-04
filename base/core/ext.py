from flask_admin import AdminIndexView, Admin
from flask_admin.contrib.sqlamodel import ModelView
from flask_login import current_user

from ..ext import db


class StaffAdminView(AdminIndexView):
    " Staff admin home page. "

    def is_accessible(self):
        return current_user.is_authenticated() and current_user.permission('staff')


class AuthModelView(ModelView):
    def __init__(self, *args, **kwargs):
        self.role = kwargs.pop('role', None) or 'admin'
        super(AuthModelView, self).__init__(*args, **kwargs)

    def is_accessible(self):
        return current_user.is_authenticated() and current_user.permission(self.role)


class FlaskAdmin(Admin):

    def __init__(self, **kwargs):
        super(FlaskAdmin, self).__init__(index_view=StaffAdminView(), **kwargs)

    def init_app(self, app):
        self.app = None
        super(FlaskAdmin, self).init_app(app)

        from ..loader import loader
        loader.load_submod('admin')

    def add_model(self, model, view=None, role='admin', **kwargs):
        view = view or AuthModelView
        self.add_view(view(model, db.session))


admin = FlaskAdmin()
