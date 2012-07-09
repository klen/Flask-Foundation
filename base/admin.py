from flask.ext.admin import AdminIndexView, Admin
from flask.ext.admin.contrib.sqlamodel import ModelView

from base.users import permission


class StaffAdminView(AdminIndexView):
    " Staff admin home page. "
    def is_accessible(self):
        return permission.staff.can()


class AuthModelView(ModelView):
    def __init__(self, *args, **kwargs):
        self.permission = kwargs.pop('permission', None) or permission.admin
        super(AuthModelView, self).__init__(*args, **kwargs)

    def is_accessible(self):
        return self.permission.can()


# Create admin
admin = Admin(name='Admin', index_view=StaffAdminView())
