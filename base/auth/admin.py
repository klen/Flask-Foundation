from ..core.ext import admin, ModelView
from .models import User, Role


class UserView(ModelView):
    column_filters = 'username', 'email'

admin.add_model(User, UserView)
admin.add_model(Role)
