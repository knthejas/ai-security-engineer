from datetime import datetime
from typing import Any
from uuid import UUID

from sqlalchemy import JSON, DateTime, ForeignKey, Index, String
from sqlalchemy.orm import Mapped, mapped_column

from ai_security_engineer.db.base import Base


class SecurityEventModel(Base):
    """Database representation of a normalized tenant-scoped security event."""

    __tablename__ = "security_events"
    __table_args__ = (Index("ix_security_events_tenant_occurred_at", "tenant_id", "occurred_at"),)

    id: Mapped[UUID] = mapped_column(primary_key=True)
    tenant_id: Mapped[UUID] = mapped_column(ForeignKey("tenants.id", ondelete="RESTRICT"))
    schema_version: Mapped[str] = mapped_column(String(16))
    source: Mapped[str] = mapped_column(String(100))
    source_event_id: Mapped[str | None] = mapped_column(String(512))
    event_type: Mapped[str] = mapped_column(String(255))
    action: Mapped[str | None] = mapped_column(String(255))
    outcome: Mapped[str] = mapped_column(String(32))
    occurred_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    ingested_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    actor: Mapped[dict[str, Any] | None] = mapped_column(JSON)
    resources: Mapped[list[dict[str, Any]]] = mapped_column(JSON, default=list)
    source_ip: Mapped[str | None] = mapped_column(String(45))
