"""Added Key to auth

Revision ID: 00000003
Revises: 00000002
Create Date: 2012-09-29 20:54:46.332465

"""

# revision identifiers, used by Alembic.
revision = '00000003'
down_revision = '00000002'

from alembic import op
import sqlalchemy as db
from datetime import datetime


def upgrade():
    op.create_table(
        'auth_key',

        db.Column('id', db.Integer, primary_key=True),
        db.Column('created_at', db.DateTime,
                  default=datetime.utcnow, nullable=False),
        db.Column('updated_at', db.DateTime,
                  onupdate=datetime.utcnow, default=datetime.utcnow),

        db.Column('service_alias', db.String),
        db.Column('service_id', db.String),
        db.Column('access_token', db.String),
        db.Column('secret', db.String),
        db.Column('expires', db.DateTime),
        db.Column('refresh_token', db.String),
        db.Column('user_id', db.Integer, db.ForeignKey('auth_user.id')),

        db.UniqueConstraint('service_alias', 'service_id'),
    )


def downgrade():
    op.drop_table('auth_key')
