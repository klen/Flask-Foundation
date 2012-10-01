"""Fill admin recv

Create Date: 2012-08-11 17:28:35.464047

"""

# revision identifiers, used by Alembic.
from sqlalchemy.ext.declarative import declared_attr
from werkzeug import generate_password_hash

from base.core.models import BaseMixin
from flask_sqlalchemy import SQLAlchemy
from flask import current_app


revision = '00000002'
down_revision = '00000001'

db = SQLAlchemy(current_app)


class MigrateRole(db.Model, BaseMixin):
    __tablename__ = 'auth_role'
    __table_args__ = {'extend_existing': True}
    name = db.Column(db.String(19), nullable=False, unique=True)

userroles = db.Table(
    'auth_userroles',
    db.Column('user_id', db.Integer, db.ForeignKey('auth_user.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('auth_role.id')),
    extend_existing=True,
)


class MigrateUser(db.Model, BaseMixin):
    __tablename__ = 'auth_user'
    __table_args__ = {'extend_existing': True}
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(120))
    active = db.Column(db.Boolean, default=True)
    _pw_hash = db.Column(db.String(199), nullable=False)

    @declared_attr
    def roles(self):
        assert self
        return db.relationship(MigrateRole, secondary=userroles, backref="auth")


def upgrade():
    admin = MigrateRole(name='admin')
    staff = MigrateRole(name='staff')
    user = MigrateUser(username='admin',
                       email='admin@admin.com',
                       _pw_hash=generate_password_hash('adminft7'))
    user.roles.append(admin)
    user.roles.append(staff)
    db.session.add(user)
    db.session.commit()


def downgrade():
    pass

# pymode:lint_ignore=E0611,E0202
