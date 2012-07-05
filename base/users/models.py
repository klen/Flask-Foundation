from datetime import datetime

from flask.ext.login import UserMixin
from werkzeug import check_password_hash, generate_password_hash

from base.admin import admin, AuthModelView
from base.app import db
from base.models import AutoInitMixin


class User(db.Model, AutoInitMixin, UserMixin):

    created = db.Column(db.DateTime, default=datetime.utcnow)
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(120), unique=True)
    pw_hash = db.Column(db.String())
    active = db.Column(db.Boolean, default=True)
    staff = db.Column(db.Boolean, default=False)
    admin = db.Column(db.Boolean, default=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.pw_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pw_hash, password)

    def is_active(self):
        return self.active

    def __repr__(self):
        return '<User %r>' % (self.username)

# Add view
admin.add_view(AuthModelView(User, db.session))
