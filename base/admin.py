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


# Create admin
admin = Admin(name='Admin', index_view=StaffAdminView())
