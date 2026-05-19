"""add document analysis fields to documents table

Revision ID: 20260519_0003
Revises: 20260519_0002
Create Date: 2026-05-19 00:00:00.000000
"""

import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision = "20260519_0003"
down_revision = "20260519_0002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add analysis fields to documents table
    op.add_column("documents", sa.Column("summary", sa.Text(), nullable=True))
    op.add_column("documents", sa.Column("risk_score", sa.Integer(), nullable=True))
    op.add_column(
        "documents",
        sa.Column("risk_clauses_json", sa.Text(), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("documents", "risk_clauses_json")
    op.drop_column("documents", "risk_score")
    op.drop_column("documents", "summary")

