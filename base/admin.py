from flask.ext.admin import AdminIndexView, Admin
from flask.ext.admin.contrib.sqlamodel import ModelView
from flask.ext.login import current_user


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

    def __init__(self, db=None, **kwargs):
        self.db = db
        super(FlaskAdmin, self).__init__(index_view=StaffAdminView(), **kwargs)

    def add_model(self, model, view=None, role='admin', **kwargs):
        view = view or AuthModelView
        self.add_view(view(model, self.db.session))
