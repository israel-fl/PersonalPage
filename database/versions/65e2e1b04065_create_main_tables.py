"""create main tables

Revision ID: 65e2e1b04065
Revises:
Create Date: 2017-05-16 22:22:04.651362

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
from datetime import datetime
import json
from werkzeug.security import generate_password_hash
from sqlalchemy import Integer, String, DateTime, Boolean


# revision identifiers, used by Alembic.
revision = "65e2e1b04065"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("display_name", sa.String(255), nullable=False),
        sa.Column("email", sa.String(255), nullable=False),
        sa.Column("password", sa.String(255), nullable=False),
        sa.Column("level", sa.Integer(), nullable=False),
        sa.Column("verified", sa.Boolean(),
                  nullable=False, default=False),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("modified", sa.DateTime(), nullable=True),
        sa.Column("profile_image_url", sa.String(255), nullable=True),
        sa.Column("description", sa.String(255), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_unique_constraint("uq_user_name", "users", ["display_name", "email"])
    op.create_table(
        "password_reset_requests",
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("token", sa.String(255), nullable=False),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("token"),
        sa.ForeignKeyConstraint(["user_id"],
                                ["users.id"])
    )
    op.create_table(
        "verify_email_requests",
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("token", sa.String(255), nullable=False),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("completed", sa.Boolean, nullable=False, default=False),
        sa.PrimaryKeyConstraint("token"),
        sa.ForeignKeyConstraint(["user_id"],
                                ["users.id"])
    )

    seed_user_table()


def downgrade():
    op.drop_table("password_reset_requests")
    op.drop_table("verify_email_requests")
    op.drop_table("users")


# Seed the user database with an administrator
def seed_user_table():

    users_table = table("users",
                        column("id", Integer),
                        column("name", String),
                        column("display_name", String),
                        column("email", String),
                        column("password", String),
                        column("level", Integer),
                        column("verified", Boolean),
                        column("created", DateTime),
                        column("modified", String)
                        )

    with open("config.json") as config_file:
        keys = json.load(config_file)
        email = keys.get("ADMIN_EMAIL")
        password = generate_password_hash(keys.get("ADMIN_PASSWORD"))
        op.bulk_insert(users_table,
                       [
                           {
                               "id": 1,
                               "name": "Administrator",
                               "display_name": "admin",
                               "email": email,
                               "password": password,
                               "level": 3,
                               "verified": True,
                               "created": datetime.now(),
                               "modified": datetime.now()
                           },
                       ]
                       )
