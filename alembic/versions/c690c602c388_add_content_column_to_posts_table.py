"""Add content column to posts table

Revision ID: c690c602c388
Revises: e75fe7d27157
Create Date: 2022-12-19 15:55:30.865993

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c690c602c388'
down_revision = 'f2b51b25ff59'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String, nullable=False))


def downgrade() -> None:
    op.drop_column('posts','content')
