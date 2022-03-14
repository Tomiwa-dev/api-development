"""add users table

Revision ID: 76c4d0e94535
Revises: 69639758285a
Create Date: 2022-03-13 23:36:39.648445

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '76c4d0e94535'
down_revision = '69639758285a'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('Users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('timestamp', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )
    pass


def downgrade():
    op.drop_table('Users')
    pass
