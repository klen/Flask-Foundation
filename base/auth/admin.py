from flask_admin.contrib.sqlamodel import ModelView
from flask_wtf import PasswordField, required

from ..core.ext import admin
from .models import User, Role, Key


class UserView(ModelView):
    column_filters = 'username', 'email'
    column_list = 'username', 'email', 'active', 'created_at', 'updated_at'
    form_excluded_columns = 'oauth_token', 'oauth_secret', '_pw_hash'

    def scaffold_form(self):
        form = super(UserView, self).scaffold_form()
        form.pw_hash = PasswordField(validators=[required()])
        form.roles.kwargs['validators'] = []
        return form

admin.add_model(User, UserView)
admin.add_model(Role)
admin.add_model(Key)
