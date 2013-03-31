"""init_pages

Revision ID: 00000004
Revises: 00000003
Create Date: 2012-12-12 19:35:23.779969

"""

# revision identifiers, used by Alembic.
revision = '00000004'
down_revision = '00000003'

from alembic import op
import sqlalchemy as db
from datetime import datetime


def upgrade():
    op.create_table(
        'pages_page',

        db.Column('id', db.Integer, primary_key=True),
        db.Column('created_at', db.DateTime,
                  default=datetime.utcnow, nullable=False),
        db.Column('updated_at', db.DateTime,
                  onupdate=datetime.utcnow, default=datetime.utcnow),

        db.Column('active', db.Boolean, default=True),
        db.Column('slug', db.String(100), nullable=False, unique=True),
        db.Column('link', db.String(256)),
        db.Column('content', db.Text),
        db.Column('parent_id', db.Integer, db.ForeignKey('pages_page.id')),
    )


def downgrade():
    op.drop_table('pages_page')
