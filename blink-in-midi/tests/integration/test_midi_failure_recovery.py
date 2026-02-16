from __future__ import annotations

from datetime import datetime, timezone

import httpx

from blink_midi.models import MidiInputEvent
from blink_midi.sender import process_event



def test_processing_continues_with_bad_url_then_good_url(monkeypatch) -> None:
    event = MidiInputEvent(
        event_type="control_change",
        channel=0,
        key=1,
        value=20,
        state=None,
        timestamp=datetime.now(timezone.utc),
        source_device="demo-device",
    )

    class FakeResponse:
        def __init__(self, status_code: int, body: dict[str, str]):
            self.status_code = status_code
            self._body = body
            self.text = str(body)

        def json(self) -> dict[str, str]:
            return self._body

    class FakeClient:
        def __init__(self, timeout: float):
            self.timeout = timeout

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return None

        def post(self, url: str, json: dict[str, object], headers: dict[str, str]) -> FakeResponse:  # noqa: A002
            if url == "bad-url":
                raise httpx.InvalidURL("Invalid URL")
            return FakeResponse(200, {"status": "ok"})

    monkeypatch.setattr("blink_midi.sender.httpx.Client", FakeClient)

    failed = process_event(event, "bad-url")
    assert failed.failure_reason is not None

    recovered = process_event(event, "http://127.0.0.1:8000/midi/events")
    assert recovered.failure_reason is None
