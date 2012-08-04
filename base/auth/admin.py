from flask import current_app

from .models import User, Role


current_app.admin.add_model(User)

current_app.admin.add_model(Role)
