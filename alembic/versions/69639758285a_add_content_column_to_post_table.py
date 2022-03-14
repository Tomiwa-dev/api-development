"""add content column to post table

Revision ID: 69639758285a
Revises: c3841b69d3ab
Create Date: 2022-03-13 23:29:24.150104

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '69639758285a'
down_revision = 'c3841b69d3ab'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('Post', sa.Column('content', sa.String(), nullable=False))

    pass


def downgrade():
    op.drop_column('Post', 'content')

    pass
