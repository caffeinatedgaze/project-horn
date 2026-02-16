from __future__ import annotations

from pathlib import Path

from blink_midi.models import REQUIRED_PAYLOAD_FIELDS



def test_openapi_contains_required_payload_fields() -> None:
    contract_path = Path("specs/001-midi-http-bridge/contracts/openapi.yaml")
    content = contract_path.read_text(encoding="utf-8")
    for field in REQUIRED_PAYLOAD_FIELDS:
        assert f"- {field}" in content or f"{field}:" in content



def test_openapi_supports_mapped_event_types() -> None:
    content = Path("specs/001-midi-http-bridge/contracts/openapi.yaml").read_text(encoding="utf-8")
    for event_type in ["note_on", "note_off", "control_change"]:
        assert event_type in content
