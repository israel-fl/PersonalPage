"""Create offsite backups table

Revision ID: b756c2ec57a7
Revises:
Create Date: 2016-12-15 16:30:42.398459

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b756c2ec57a7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():

    op.create_table(
        'organization_offsite_credentials',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('groupName', sa.String(255), nullable=False),
        sa.Column('accessKey', sa.String(255), nullable=False),
        sa.Column('secretKey', sa.String(255), nullable=False),
        sa.Column('accountId', sa.String(255), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_table(
        'managed_offsite_backups',
        sa.Column('agentGuid', sa.String(255), nullable=False, unique=True),
        sa.Column('machName', sa.String(255), nullable=False),
        sa.Column('groupId', sa.Integer(), nullable=False),
        sa.Column('groupName', sa.String(255), nullable=False),
        sa.Column('vault', sa.String(255), nullable=False),
        sa.Column('archiveLocation', sa.String(255), nullable=False),
        sa.Column('archiveId', sa.Integer(), nullable=True),
        sa.Column('token', sa.String(255), nullable=True),
        sa.PrimaryKeyConstraint('agentGuid'),
        sa.ForeignKeyConstraint(['groupId'],
                                ['organization_offsite_credentials.id'])
    )
    op.create_table(
        'offsite_backup_requests',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('agentGuid', sa.String(255), nullable=False),
        sa.Column('created', sa.DateTime(), nullable=False),
        sa.Column('archiveId', sa.String(255), nullable=True),
        sa.Column('fileName', sa.String(255), nullable=True),
        sa.Column('token', sa.String(255), nullable=False),
        sa.Column('status', sa.String(255), nullable=True),
        sa.Column('success',
                  sa.String(),
                  default="",
                  nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['agentGuid'],
                                ['managed_offsite_backups.agentGuid'])
    )
    op.create_table(
        'offsite_retrieval_requests',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('agentGuid', sa.String(255), nullable=False),
        sa.Column('created', sa.DateTime(), nullable=False),
        sa.Column('archiveId', sa.String(255), nullable=True),
        sa.Column('token', sa.String(255), nullable=False),
        sa.Column('status', sa.String(255), nullable=True),
        sa.Column('success',
                  sa.Boolean(),
                  default="",
                  nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['agentGuid'],
                                ['managed_offsite_backups.agentGuid'])
    )


def downgrade():
    op.drop_table('offsite_retrieval_requests')
    op.drop_table('offsite_backup_requests')
    op.drop_table('managed_offsite_backups')
    op.drop_table('organization_offsite_credentials')

