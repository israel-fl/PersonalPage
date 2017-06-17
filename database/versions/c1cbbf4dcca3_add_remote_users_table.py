"""Add remote users table

Revision ID: c1cbbf4dcca3
Revises: b49f470eb355
Create Date: 2017-06-11 16:19:49.583822

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c1cbbf4dcca3'
down_revision = 'b49f470eb355'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'remote_source_users',
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column('google_user_id', sa.String(255), nullable=True),
        sa.Column('fb_user_id', sa.String(255), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(["user_id"],
                                ["users.id"])
    )


def downgrade():
    op.drop_table('remote_source_users')
