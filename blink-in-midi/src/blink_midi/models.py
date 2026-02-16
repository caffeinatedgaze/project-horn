from __future__ import annotations

from datetime import datetime, timezone
from typing import Literal
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field, field_validator

EventType = Literal["note_on", "note_off", "control_change"]
NoteState = Literal["on", "off"]


class MidiInputEvent(BaseModel):
    model_config = ConfigDict(extra="forbid")

    event_type: EventType
    channel: int = Field(ge=0, le=15)
    key: int = Field(ge=0, le=127)
    value: int = Field(ge=0, le=127)
    state: NoteState | None
    timestamp: datetime
    source_device: str

    @field_validator("timestamp", mode="before")
    @classmethod
    def normalize_timestamp(cls, value: datetime | str) -> datetime:
        if isinstance(value, str):
            parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        else:
            parsed = value
        if parsed.tzinfo is None:
            return parsed.replace(tzinfo=timezone.utc)
        return parsed.astimezone(timezone.utc)


class MidiEventPayload(BaseModel):
    model_config = ConfigDict(extra="forbid")

    event_type: EventType
    channel: int = Field(ge=0, le=15)
    key: int = Field(ge=0, le=127)
    value: int = Field(ge=0, le=127)
    state: NoteState | None
    timestamp: datetime

    @field_validator("timestamp", mode="before")
    @classmethod
    def normalize_timestamp(cls, value: datetime | str) -> datetime:
        if isinstance(value, str):
            parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        else:
            parsed = value
        if parsed.tzinfo is None:
            return parsed.replace(tzinfo=timezone.utc)
        return parsed.astimezone(timezone.utc)


class OutboundRequestIntent(BaseModel):
    model_config = ConfigDict(extra="forbid")

    method: Literal["POST"] = "POST"
    url: str
    headers: dict[str, str]
    payload: MidiEventPayload
    simulated_sent: bool = True
    failure_reason: str | None = None

    @field_validator("url")
    @classmethod
    def validate_url(cls, value: str) -> str:
        if not value.startswith("http://") and not value.startswith("https://"):
            raise ValueError("url must start with http:// or https://")
        return value


class BridgeSession(BaseModel):
    model_config = ConfigDict(extra="forbid")

    session_id: str = Field(default_factory=lambda: str(uuid4()))
    started_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    selected_device: str
    api_url: str
    processed_events: int = 0
    ignored_events: int = 0
    intent_failures: int = 0


REQUIRED_PAYLOAD_FIELDS = ["event_type", "channel", "key", "value", "state", "timestamp"]
