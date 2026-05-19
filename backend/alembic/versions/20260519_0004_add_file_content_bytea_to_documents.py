"""add file_content bytea column to documents table

Revision ID: 20260519_0004
Revises: 20260519_0003
Create Date: 2026-05-19 00:00:00.000000
"""

import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision = "20260519_0004"
down_revision = "20260519_0003"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add file_content column to documents table to store file data in PostgreSQL
    op.add_column(
        "documents",
        sa.Column("file_content", sa.LargeBinary(), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("documents", "file_content")
