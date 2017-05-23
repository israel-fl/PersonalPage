"""update posts table

Revision ID: 6dc3b1a199ab
Revises: 65e2e1b04065
Create Date: 2017-05-23 00:11:43.796777

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6dc3b1a199ab'
down_revision = '65e2e1b04065'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('post', sa.Column('subtitle', sa.String(255)))
    op.add_column('post', sa.Column('slug', sa.String(255)))
    op.add_column('post', sa.Column('featured_image_url', sa.String(255)))
    op.add_column('post', sa.Column('published', sa.Boolean(), default=False))

def downgrade():
    op.drop_column('post', 'subtitle')
    op.drop_column('post', 'slug')
    op.drop_column('post', 'featured_image_url')
    op.drop_column('post', 'published')
