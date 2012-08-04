from ..core.ext import admin
from .models import User, Role


admin.add_model(User)
admin.add_model(Role)
