"""create posts table

Revision ID: de74e2254bda
Revises: 6dc3b1a199ab
Create Date: 2017-05-31 18:15:38.070075

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'de74e2254bda'
down_revision = '65e2e1b04065'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'posts',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('author', sa.String(255), nullable=False),
        sa.Column('subtitle', sa.String(255), nullable=False),
        sa.Column('featured_image_url', sa.String(255), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('tags', sa.String(255), nullable=True),
        sa.Column('slug', sa.String(255), nullable=False),
        sa.Column('published', sa.Boolean(), nullable=False, default=False),
        sa.Column('created', sa.DateTime(), nullable=False),
        sa.Column('modified', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
    )


def downgrade():
    op.drop_table('posts')
