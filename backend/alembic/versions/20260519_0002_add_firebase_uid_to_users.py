"""add firebase_uid to users table

Revision ID: 20260519_0002
Revises: 20260511_0001
Create Date: 2026-05-19 00:00:00.000000
"""

import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision = "20260519_0002"
down_revision = "20260511_0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add firebase_uid column to users table
    # Make it nullable initially to avoid blocking existing users, then set NOT NULL later
    op.add_column(
        "users",
        sa.Column("firebase_uid", sa.String(length=255), nullable=True),
    )
    # Create unique index on firebase_uid
    op.create_index("ix_users_firebase_uid", "users", ["firebase_uid"], unique=True)


def downgrade() -> None:
    op.drop_index("ix_users_firebase_uid", table_name="users")
    op.drop_column("users", "firebase_uid")

