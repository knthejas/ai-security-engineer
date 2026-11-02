from datetime import UTC, datetime
from uuid import UUID, uuid4

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from ai_security_engineer.db.base import Base
from ai_security_engineer.db.models import Tenant
from ai_security_engineer.schemas.security_event import EventOutcome, SecurityEvent
from ai_security_engineer.services.security_event_repository import (
    EventTenantMismatchError,
    SecurityEventRepository,
    TenantNotFoundError,
)


@pytest.fixture
def session() -> Session:
    engine = create_engine("sqlite+pysqlite:///:memory:")
    Base.metadata.create_all(engine)
    with Session(engine) as database_session:
        yield database_session
    Base.metadata.drop_all(engine)
    engine.dispose()


def make_event(tenant_id: UUID) -> SecurityEvent:
    return SecurityEvent(
        tenant_id=tenant_id,
        source="synthetic-lab",
        source_event_id="event-001",
        event_type="identity.user.created",
        outcome=EventOutcome.SUCCESS,
        occurred_at=datetime(2026, 1, 15, 4, 30, tzinfo=UTC),
        ingested_at=datetime(2026, 1, 15, 4, 35, tzinfo=UTC),
    )


def test_repository_creates_and_retrieves_event_for_its_tenant(session: Session) -> None:
    tenant = Tenant(name="Synthetic Tenant")
    session.add(tenant)
    session.flush()
    event = make_event(tenant.id)
    repository = SecurityEventRepository(session)

    created_event = repository.create(tenant.id, event)
    session.commit()

    retrieved_event = repository.get_for_tenant(tenant.id, event.event_id)

    assert created_event == event
    assert retrieved_event == event


def test_repository_does_not_return_event_to_a_different_tenant(session: Session) -> None:
    owner = Tenant(name="Synthetic Owner")
    other_tenant = Tenant(name="Synthetic Other Tenant")
    session.add_all([owner, other_tenant])
    session.flush()
    event = make_event(owner.id)
    repository = SecurityEventRepository(session)
    repository.create(owner.id, event)
    session.commit()

    assert repository.get_for_tenant(other_tenant.id, event.event_id) is None


def test_repository_rejects_nonexistent_or_mismatched_tenant(session: Session) -> None:
    tenant = Tenant(name="Synthetic Tenant")
    session.add(tenant)
    session.flush()
    repository = SecurityEventRepository(session)

    missing_tenant_id = uuid4()
    with pytest.raises(TenantNotFoundError):
        repository.create(missing_tenant_id, make_event(missing_tenant_id))

    with pytest.raises(EventTenantMismatchError):
        repository.create(tenant.id, make_event(uuid4()))
