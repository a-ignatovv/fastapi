"""add last columns to posts table

Revision ID: 571ed97c1616
Revises: 9c2749654419
Create Date: 2022-12-19 16:35:34.255368

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '571ed97c1616'
down_revision = '9c2749654419'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE'))
    op.add_column('posts', sa.Column('created_at',
        sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')))


def downgrade() -> None:
    op.drop_column('posts','published')
    op.drop_column('posts','created_at')
