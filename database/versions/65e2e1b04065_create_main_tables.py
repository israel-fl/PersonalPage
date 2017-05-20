"""create main tables

Revision ID: 65e2e1b04065
Revises:
Create Date: 2017-05-16 22:22:04.651362

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '65e2e1b04065'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('display_name', sa.String(255), nullable=False),
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('password', sa.String(255), nullable=False),
        sa.Column('level', sa.Integer(), nullable=False),
        sa.Column('verified', sa.String(15), nullable=False, default="false"),
        sa.Column('created', sa.String(255), nullable=False),
        sa.Column('modified', sa.String(255), nullable=True),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_table(
        'password_reset_requests',
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('token', sa.String(255), nullable=False),
        sa.Column('created', sa.String(255), nullable=False),
        sa.PrimaryKeyConstraint('token'),
        sa.ForeignKeyConstraint(['user_id'],
                                ['users.id'])
    )
    op.create_table(
        'verify_email_requests',
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('token', sa.String(255), nullable=False),
        sa.Column('created', sa.String(255), nullable=False,),
        sa.PrimaryKeyConstraint('token'),
        sa.ForeignKeyConstraint(['user_id'],
                                ['users.id'])
    )


def downgrade():
    op.drop_table('password_reset_requests')
    op.drop_table('verify_email_requests')
    op.drop_table('users')
