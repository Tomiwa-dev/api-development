"""create post table

Revision ID: c3841b69d3ab
Revises: 
Create Date: 2022-03-13 09:47:39.784587

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c3841b69d3ab'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('Post', sa.Column('id', sa.Integer(), nullable=False,
                                       primary_key=True), sa.Column('title', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_table('Post')

    pass
