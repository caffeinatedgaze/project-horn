from __future__ import annotations

from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from blink_midi.models import MidiInputEvent, OutboundRequestIntent, REQUIRED_PAYLOAD_FIELDS



def test_midi_input_event_validates_ranges() -> None:
    with pytest.raises(ValidationError):
        MidiInputEvent(
            event_type="note_on",
            channel=17,
            key=60,
            value=1,
            state="on",
            timestamp=datetime.now(timezone.utc),
            source_device="demo-device",
        )



def test_request_intent_requires_http_url() -> None:
    with pytest.raises(ValidationError):
        OutboundRequestIntent(
            url="ftp://bad",
            headers={"Content-Type": "application/json"},
            payload={
                "event_type": "note_on",
                "channel": 0,
                "key": 60,
                "value": 90,
                "state": "on",
                "timestamp": "now",
            },
        )



def test_required_payload_fields_constant_is_complete() -> None:
    assert REQUIRED_PAYLOAD_FIELDS == ["event_type", "channel", "key", "value", "state", "timestamp"]
