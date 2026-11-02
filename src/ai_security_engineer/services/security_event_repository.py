from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from ai_security_engineer.db.models import SecurityEventModel, Tenant
from ai_security_engineer.schemas.security_event import EventActor, EventResource, SecurityEvent


class TenantNotFoundError(ValueError):
    """Raised when an operation references a tenant that does not exist."""


class EventTenantMismatchError(ValueError):
    """Raised when an event is written through a different tenant scope."""


class SecurityEventRepository:
    """Persistence operations that keep every security-event query tenant-scoped."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def create(self, tenant_id: UUID, event: SecurityEvent) -> SecurityEvent:
        """Store an event after verifying the tenant scope and ownership."""
        if event.tenant_id != tenant_id:
            raise EventTenantMismatchError(
                "event tenant_id does not match the repository tenant scope"
            )
        if self._session.get(Tenant, tenant_id) is None:
            raise TenantNotFoundError("tenant does not exist")

        event_model = SecurityEventModel(
            id=event.event_id,
            tenant_id=event.tenant_id,
            schema_version=event.schema_version,
            source=event.source,
            source_event_id=event.source_event_id,
            event_type=event.event_type,
            action=event.action,
            outcome=event.outcome.value,
            occurred_at=event.occurred_at,
            ingested_at=event.ingested_at,
            actor=event.actor.model_dump(mode="json") if event.actor is not None else None,
            resources=[resource.model_dump(mode="json") for resource in event.resources],
            source_ip=str(event.source_ip) if event.source_ip is not None else None,
        )
        self._session.add(event_model)
        self._session.flush()
        return self._to_schema(event_model)

    def get_for_tenant(self, tenant_id: UUID, event_id: UUID) -> SecurityEvent | None:
        """Retrieve one event only when it belongs to the requested tenant."""
        statement = select(SecurityEventModel).where(
            SecurityEventModel.id == event_id,
            SecurityEventModel.tenant_id == tenant_id,
        )
        event_model = self._session.scalar(statement)
        return self._to_schema(event_model) if event_model is not None else None

    @staticmethod
    def _to_schema(event_model: SecurityEventModel) -> SecurityEvent:
        """Convert a persisted event back to the shared Pydantic contract."""
        return SecurityEvent(
            schema_version=event_model.schema_version,
            event_id=event_model.id,
            tenant_id=event_model.tenant_id,
            source=event_model.source,
            source_event_id=event_model.source_event_id,
            event_type=event_model.event_type,
            action=event_model.action,
            outcome=event_model.outcome,
            occurred_at=_as_utc(event_model.occurred_at),
            ingested_at=_as_utc(event_model.ingested_at),
            actor=EventActor.model_validate(event_model.actor)
            if event_model.actor is not None
            else None,
            resources=tuple(
                EventResource.model_validate(resource) for resource in event_model.resources
            ),
            source_ip=event_model.source_ip,
        )


def _as_utc(value: datetime) -> datetime:
    """Accommodate SQLite test timestamps while PostgreSQL preserves timezone data."""
    if value.tzinfo is None or value.utcoffset() is None:
        return value.replace(tzinfo=UTC)
    return value.astimezone(UTC)
