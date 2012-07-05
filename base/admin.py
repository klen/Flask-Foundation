from flask.ext.admin import AdminIndexView, Admin
from flask.ext.admin.contrib.sqlamodel import ModelView
from flask.ext.login import current_user


class AuthAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated() and current_user.staff


class AuthModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated() and current_user.staff


# Create admin
admin = Admin(name='Admin', index_view=AuthAdminIndexView())
