"""Create tenants and security events tables.

Revision ID: 0001
Revises:
Create Date: 2026-10-31
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0001"
down_revision: str | None = None
branch_labels: Sequence[str] | None = None
depends_on: Sequence[str] | None = None


def upgrade() -> None:
    """Create the initial tenant-scoped persistence schema."""
    op.create_table(
        "tenants",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "security_events",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("tenant_id", sa.Uuid(), nullable=False),
        sa.Column("schema_version", sa.String(length=16), nullable=False),
        sa.Column("source", sa.String(length=100), nullable=False),
        sa.Column("source_event_id", sa.String(length=512), nullable=True),
        sa.Column("event_type", sa.String(length=255), nullable=False),
        sa.Column("action", sa.String(length=255), nullable=True),
        sa.Column("outcome", sa.String(length=32), nullable=False),
        sa.Column("occurred_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("ingested_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("actor", sa.JSON(), nullable=True),
        sa.Column("resources", sa.JSON(), nullable=False),
        sa.Column("source_ip", sa.String(length=45), nullable=True),
        sa.ForeignKeyConstraint(["tenant_id"], ["tenants.id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_security_events_tenant_occurred_at", "security_events", ["tenant_id", "occurred_at"]
    )


def downgrade() -> None:
    """Drop the initial tenant-scoped persistence schema."""
    op.drop_index("ix_security_events_tenant_occurred_at", table_name="security_events")
    op.drop_table("security_events")
    op.drop_table("tenants")
