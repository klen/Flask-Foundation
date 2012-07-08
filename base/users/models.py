from flask.ext.login import UserMixin
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from werkzeug import check_password_hash, generate_password_hash

from base.admin import admin, AuthModelView
from base.app import db
from base.core import BaseMixin


usergroups = db.Table('users_usergroups',
    db.Column('user_id', db.Integer, db.ForeignKey('users_user.id')),
    db.Column('group_id', db.Integer, db.ForeignKey('users_group.id'))
)


class Group(db.Model, BaseMixin):

    __tablename__ = 'users_group'

    name = db.Column(db.String(19), nullable=False, unique=True)
    active = db.Column(db.Boolean, default=True)

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return '<Group %r>' % (self.name)

# Add view
admin.add_view(AuthModelView(Group, db.session))


class User(db.Model, UserMixin, BaseMixin):

    __tablename__ = 'users_user'

    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(120), unique=True)
    active = db.Column(db.Boolean, default=True)
    staff = db.Column(db.Boolean, default=False)
    admin = db.Column(db.Boolean, default=False)
    _pw_hash = db.Column(db.String(199), nullable=False)

    @declared_attr
    def groups(cls):
        return relationship("Group", secondary=usergroups, backref="users")

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

    def check_password(self, password):
        return check_password_hash(self.pw_hash, password)

    def is_active(self):
        return self.active

    @property
    def memberof(self, prefix="group:"):
        """Returns a list of groups for which this user is a member,
        with each group appended by the given prefix.
        """
        return ['%s%s' % (prefix or '', g.name) for g in self.groups]

    @property
    def memberofcount(self):
        """Returns the number of groups to which this User is a member
        as an int.
        """
        return len(self.groups)

    def __unicode__(self):
        return self.username

    def __repr__(self):
        return '<User %r>' % (self.username)

# Add view
admin.add_view(AuthModelView(User, db.session))
