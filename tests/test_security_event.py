from datetime import UTC, datetime, timedelta, timezone
from uuid import UUID

import pytest
from pydantic import ValidationError

from ai_security_engineer.schemas.security_event import (
    EventActor,
    EventOutcome,
    EventResource,
    SecurityEvent,
)


def test_security_event_normalizes_synthetic_event_data() -> None:
    event = SecurityEvent(
        tenant_id="3fa85f64-5717-4562-b3fc-2c963f66afa6",
        source=" synthetic-lab ",
        source_event_id="event-001",
        event_type=" identity.user.created ",
        action=" CreateUser ",
        outcome=EventOutcome.SUCCESS,
        occurred_at=datetime(2026, 1, 15, 10, 0, tzinfo=timezone(timedelta(hours=5, minutes=30))),
        ingested_at=datetime(2026, 1, 15, 4, 35, tzinfo=UTC),
        actor=EventActor(kind="user", identifier="user-123", display_name="Synthetic User"),
        resources=[EventResource(kind="identity", identifier="user-456")],
        source_ip="203.0.113.10",
    )

    assert isinstance(event.event_id, UUID)
    assert event.source == "synthetic-lab"
    assert event.event_type == "identity.user.created"
    assert event.action == "CreateUser"
    assert event.occurred_at == datetime(2026, 1, 15, 4, 30, tzinfo=UTC)
    assert event.resources[0].identifier == "user-456"
    assert event.model_dump(mode="json")["source_ip"] == "203.0.113.10"


def test_security_event_rejects_naive_timestamp() -> None:
    with pytest.raises(ValidationError, match="timestamp must include a timezone"):
        SecurityEvent(
            tenant_id="3fa85f64-5717-4562-b3fc-2c963f66afa6",
            source="synthetic-lab",
            event_type="identity.user.created",
            outcome="success",
            occurred_at=datetime(2026, 1, 15, 4, 30),
            ingested_at=datetime(2026, 1, 15, 4, 35, tzinfo=UTC),
        )


def test_security_event_rejects_unknown_fields() -> None:
    with pytest.raises(ValidationError, match="Extra inputs are not permitted"):
        SecurityEvent(
            tenant_id="3fa85f64-5717-4562-b3fc-2c963f66afa6",
            source="synthetic-lab",
            event_type="identity.user.created",
            outcome="success",
            occurred_at=datetime(2026, 1, 15, 4, 30, tzinfo=UTC),
            ingested_at=datetime(2026, 1, 15, 4, 35, tzinfo=UTC),
            raw_payload={"not": "accepted"},
        )
