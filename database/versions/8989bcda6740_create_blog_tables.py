"""create blog tables

Revision ID: 8989bcda6740
Revises: 65e2e1b04065
Create Date: 2017-05-17 14:58:45.408800

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8989bcda6740'
down_revision = '65e2e1b04065'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'entry',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('author', sa.String(255), nullable=False),
        sa.Column('subtitle', sa.String(255), nullable=False),
        sa.Column('image', sa.String(255), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('slug', sa.String(255), nullable=False),
        sa.Column('created', sa.String(255), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )


def downgrade():
    op.drop_table('entry')

