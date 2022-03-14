"""add username column to user table

Revision ID: f2f60abeb227
Revises: a2a8e1270a3e
Create Date: 2022-03-14 14:32:26.645243

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f2f60abeb227'
down_revision = 'a2a8e1270a3e'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('Users', sa.Column(
        'username', sa.String(), nullable=False), )
    pass


def downgrade():
    op.drop_column('Users', 'username')
    pass
