from __future__ import annotations

from datetime import datetime, timezone
from unittest.mock import MagicMock

from blink_midi.models import MidiInputEvent
from blink_midi.sender import build_request_intent, process_intent



def make_event() -> MidiInputEvent:
    return MidiInputEvent(
        event_type="note_on",
        channel=0,
        key=60,
        value=100,
        state="on",
        timestamp=datetime.now(timezone.utc),
        source_device="demo-device",
    )



def test_build_request_intent_has_expected_shape() -> None:
    intent = build_request_intent(make_event(), "http://127.0.0.1:8000/midi/events")
    assert intent.method == "POST"
    assert intent.url == "http://127.0.0.1:8000/midi/events"
    assert intent.payload.event_type == "note_on"
    assert intent.payload.key == 60
    assert intent.payload.state == "on"
    assert intent.headers["Accept"] == "application/json"
    assert intent.simulated_sent is True



def test_process_intent_logs_and_returns_success(monkeypatch) -> None:
    response = MagicMock()
    response.status_code = 200
    response.json.return_value = {"status": "ok"}

    client = MagicMock()
    client.__enter__.return_value = client
    client.__exit__.return_value = None
    client.post.return_value = response

    monkeypatch.setattr("blink_midi.sender.httpx.Client", lambda timeout: client)

    intent = build_request_intent(make_event(), "http://127.0.0.1:8000/midi/events")
    result = process_intent(intent)
    assert result.failure_reason is None
    assert result.simulated_sent is True



def test_process_intent_marks_failure_on_error() -> None:
    intent = build_request_intent(make_event(), "http://127.0.0.1:8000/midi/events")
    broken = intent.model_copy(update={"payload": None})  # type: ignore[arg-type]
    result = process_intent(broken)
    assert result.simulated_sent is False
    assert result.failure_reason is not None
