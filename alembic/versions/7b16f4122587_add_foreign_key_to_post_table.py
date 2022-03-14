"""add foreign key to post table

Revision ID: 7b16f4122587
Revises: 76c4d0e94535
Create Date: 2022-03-13 23:41:22.630280

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7b16f4122587'
down_revision = '76c4d0e94535'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('Post', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table="Post", referent_table="Users", local_cols=[
        'owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint('post_users_fk', table_name="Post")
    op.drop_column('Post', 'owner_id')
    pass
