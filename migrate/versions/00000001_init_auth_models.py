"""Init auth models

Create Date: 2012-08-10 17:29:18.996057

"""

# revision identifiers, used by Alembic.
from datetime import datetime

import sqlalchemy as db
from alembic import op


revision = '00000001'
down_revision = None


def upgrade():

    op.create_table(
        'auth_role',
        db.Column('id', db.Integer, primary_key=True),
        db.Column('created_at', db.DateTime,
                  default=datetime.utcnow, nullable=False),
        db.Column('updated_at', db.DateTime,
                  onupdate=datetime.utcnow, default=datetime.utcnow),
        db.Column(
            'name', db.String(19), nullable=False, unique=True),
    )

    op.create_table(
        'auth_user',
        db.Column('id', db.Integer, primary_key=True),
        db.Column('created_at', db.DateTime,
                  default=datetime.utcnow, nullable=False),
        db.Column('updated_at', db.DateTime,
                  onupdate=datetime.utcnow, default=datetime.utcnow),
        db.Column('username', db.String(50), nullable=False, unique=True),
        db.Column('email', db.String(120)),
        db.Column('active', db.Boolean, default=True),
        db.Column('_pw_hash', db.String(199), nullable=False),
        db.Column('oauth_token', db.String(200)),
        db.Column('oauth_secret', db.String(200)),
    )

    op.create_table(
        'auth_userroles',
        db.Column('user_id', db.Integer, db.ForeignKey('auth_user.id')),
        db.Column('role_id', db.Integer, db.ForeignKey('auth_role.id')),
    )


def downgrade():
    op.drop_table('auth_role')
    op.drop_table('auth_user')
    op.drop_table('auth_userroles')
