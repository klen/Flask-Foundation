from flask_login import UserMixin
from flask_principal import RoleNeed, Permission
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug import check_password_hash, generate_password_hash

from ..core.models import BaseMixin
from ..ext import db


userroles = db.Table(
    'users_userroles',
    db.Column('user_id', db.Integer, db.ForeignKey('users_user.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('users_role.id'))
)


class Role(db.Model, BaseMixin):
    " User roles. "

    __tablename__ = 'users_role'

    name = db.Column(db.String(19), nullable=False, unique=True)

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return '<Role %r>' % (self.name)


class User(db.Model, UserMixin, BaseMixin):
    " Main user model. "

    __tablename__ = 'users_user'

    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(120))
    active = db.Column(db.Boolean, default=True)
    _pw_hash = db.Column(db.String(199), nullable=False)

    # OAuth creds
    oauth_token = db.Column(db.String(200))
    oauth_secret = db.Column(db.String(200))

    @declared_attr
    def roles(self):
        assert self
        return db.relationship("Role", secondary=userroles, backref="users")

    @hybrid_property
    def pw_hash(self):
        """Simple getter function for the user's password."""
        return self._pw_hash

    @pw_hash.setter
    def pw_hash(self, raw_password):
        """ Password setter, that handles the hashing
            in the database.
        """
        self._pw_hash = generate_password_hash(raw_password)

    @staticmethod
    def permission(role):
        perm = Permission(RoleNeed(role))
        return perm.can()

    def check_password(self, password):
        return check_password_hash(self.pw_hash, password)

    def is_active(self):
        return self.active

    def __unicode__(self):
        return self.username

    def __repr__(self):
        return '<User %r>' % (self.username)


# pymode:lint_ignore=E0611
