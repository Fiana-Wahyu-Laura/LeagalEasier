"""add document processing fields

Revision ID: 20260511_0001
Revises: 
Create Date: 2026-05-11 00:01:00.000000
"""

import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision = "20260511_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("documents", sa.Column("storage_path", sa.String(length=2048), nullable=True))
    op.add_column(
        "documents",
        sa.Column("status", sa.String(length=32), nullable=False, server_default=sa.text("'pending'")),
    )
    op.add_column("documents", sa.Column("extracted_text", sa.Text(), nullable=True))
    op.add_column(
        "documents",
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_documents_owner_id", "documents", ["owner_id"], unique=False)
    op.create_index("ix_documents_status", "documents", ["status"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_documents_status", table_name="documents")
    op.drop_index("ix_documents_owner_id", table_name="documents")
    op.drop_column("documents", "updated_at")
    op.drop_column("documents", "extracted_text")
    op.drop_column("documents", "status")
    op.drop_column("documents", "storage_path")
