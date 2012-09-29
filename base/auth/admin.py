from ..core.ext import admin, ModelView
from .models import User, Role, Key
from flask_wtf import PasswordField, required


class UserView(ModelView):
    column_filters = 'username', 'email'
    list_columns = 'username', 'email', 'active', 'created_at', 'updated_at'
    excluded_form_columns = 'oauth_token', 'oauth_secret', '_pw_hash'

    def scaffold_form(self):
        form = super(UserView, self).scaffold_form()
        form.pw_hash = PasswordField(validators=[required()])
        form.roles.kwargs['validators'] = []
        return form

admin.add_model(User, UserView)
admin.add_model(Role)
admin.add_model(Key)
