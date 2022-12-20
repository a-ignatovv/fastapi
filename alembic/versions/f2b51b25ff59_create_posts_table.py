"""create posts table

Revision ID: f2b51b25ff59
Revises: 
Create Date: 2022-12-19 15:40:56.936075

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f2b51b25ff59'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True), 
    sa.Column('title', sa.String(), nullable=False)) 
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
