from flask.ext.admin import AdminIndexView, Admin
from flask.ext.admin.contrib.sqlamodel import ModelView

from base.users import permission


class AuthAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return permission.staff.can()


class AuthModelView(ModelView):
    def is_accessible(self):
        return permission.admin.can()


# Create admin
admin = Admin(name='Admin', index_view=AuthAdminIndexView())
