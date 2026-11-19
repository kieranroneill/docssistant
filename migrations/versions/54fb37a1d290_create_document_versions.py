"""Create document versions for atomic publication of indexed chunks.

Revision ID: 54fb37a1d290
Revises: 229e3133b85a
"""

import sqlalchemy as sa
from alembic import op

revision = "54fb37a1d290"
down_revision = "229e3133b85a"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "document_versions",
        sa.Column("id", sa.UUID(), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("document_id", sa.UUID(), nullable=False),
        sa.Column("source", sa.String(), nullable=False),
        sa.Column("version", sa.String(64), nullable=False),
        sa.Column("active", sa.Boolean(), server_default=sa.text("false"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("document_id", "version", name="uq_document_versions_document_version"),
    )
    op.create_index(
        "uq_document_versions_active",
        "document_versions",
        ["document_id"],
        unique=True,
        postgresql_where=sa.text("active = true"),
    )


def downgrade() -> None:
    op.drop_index("uq_document_versions_active", table_name="document_versions")
    op.drop_table("document_versions")
