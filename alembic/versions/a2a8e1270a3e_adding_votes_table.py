"""adding votes table

Revision ID: a2a8e1270a3e
Revises: fbe40785d5a6
Create Date: 2022-03-14 00:00:22.329083

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a2a8e1270a3e'
down_revision = 'fbe40785d5a6'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('votes',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['Post.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['Users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'post_id')
    )
    pass


def downgrade():
    op.drop_table('votes')

    pass
