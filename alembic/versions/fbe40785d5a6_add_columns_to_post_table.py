"""add columns to post table

Revision ID: fbe40785d5a6
Revises: 7b16f4122587
Create Date: 2022-03-13 23:49:18.896216

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fbe40785d5a6'
down_revision = '7b16f4122587'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('Post', sa.Column(
        'published', sa.Boolean(), nullable=False, server_default='TRUE'), )
    op.add_column('Post', sa.Column(
        'timestamp', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')), )
    pass


def downgrade():
    op.drop_column('Post', 'published')
    op.drop_column('Post', 'timestamp')
    pass
