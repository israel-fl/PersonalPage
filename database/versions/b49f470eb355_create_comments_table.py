"""create comments table

Revision ID: b49f470eb355
Revises: de74e2254bda
Create Date: 2017-06-02 22:54:32.610332

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b49f470eb355'
down_revision = 'de74e2254bda'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'post_comments',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('post_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('comment', sa.Text(), nullable=False),
        sa.Column('created', sa.String(255), nullable=False),
        sa.Column('modified', sa.String(255), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(["user_id"],
                                ["users.id"]),
        sa.ForeignKeyConstraint(["post_id"],
                                ["posts.id"])
    )


def downgrade():
    op.drop_table("post_comments")
