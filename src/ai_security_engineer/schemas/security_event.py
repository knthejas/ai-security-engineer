"""Source-agnostic contracts for normalized security events."""

from datetime import UTC, datetime
from enum import StrEnum
from ipaddress import IPv4Address, IPv6Address
from typing import Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field, field_validator


class EventOutcome(StrEnum):
    """The known result of a security-relevant action."""

    SUCCESS = "success"
    FAILURE = "failure"
    UNKNOWN = "unknown"


class EventActor(BaseModel):
    """The principal that initiated an event, when known."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    kind: str = Field(min_length=1, max_length=100)
    identifier: str = Field(min_length=1, max_length=512)
    display_name: str | None = Field(default=None, max_length=512)


class EventResource(BaseModel):
    """A resource affected by an event."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    kind: str = Field(min_length=1, max_length=100)
    identifier: str = Field(min_length=1, max_length=1_024)
    display_name: str | None = Field(default=None, max_length=512)


class SecurityEvent(BaseModel):
    """A validated, source-agnostic representation of one security event.

    This is an in-memory normalization contract only. Persistence, deduplication,
    and raw-event retention are intentionally outside this milestone.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    schema_version: Literal["1.0"] = "1.0"
    event_id: UUID = Field(default_factory=uuid4)
    tenant_id: UUID
    source: str = Field(min_length=1, max_length=100)
    source_event_id: str | None = Field(default=None, max_length=512)
    event_type: str = Field(min_length=1, max_length=255)
    action: str | None = Field(default=None, max_length=255)
    outcome: EventOutcome
    occurred_at: datetime
    ingested_at: datetime
    actor: EventActor | None = None
    resources: tuple[EventResource, ...] = Field(default_factory=tuple)
    source_ip: IPv4Address | IPv6Address | None = None

    @field_validator("source", "event_type", "action", mode="before")
    @classmethod
    def strip_non_empty_strings(cls, value: str | None) -> str | None:
        """Reject blank identifiers while accepting an omitted optional action."""
        if value is None:
            return None
        normalized_value = value.strip()
        if not normalized_value:
            raise ValueError("value must not be blank")
        return normalized_value

    @field_validator("occurred_at", "ingested_at")
    @classmethod
    def normalize_timestamp_to_utc(cls, value: datetime) -> datetime:
        """Require an explicit timezone and store timestamps in UTC."""
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("timestamp must include a timezone")
        return value.astimezone(UTC)
