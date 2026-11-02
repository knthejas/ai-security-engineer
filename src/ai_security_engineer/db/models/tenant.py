from datetime import UTC, datetime
from uuid import UUID, uuid4

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from ai_security_engineer.db.base import Base


def utc_now() -> datetime:
    """Return the current time with an explicit UTC offset."""
    return datetime.now(UTC)


class Tenant(Base):
    """A tenant that owns security events."""

    __tablename__ = "tenants"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(255), unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
