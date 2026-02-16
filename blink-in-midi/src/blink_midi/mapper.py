from __future__ import annotations

from datetime import datetime, timezone

from mido.messages.messages import Message

from .models import MidiInputEvent

SUPPORTED_TYPES = {"note_on", "note_off", "control_change"}



def map_message(message: Message, source_device: str) -> MidiInputEvent | None:
    event_type = message.type
    if event_type not in SUPPORTED_TYPES:
        return None

    # MIDI convention: note_on velocity 0 is equivalent to note_off.
    if event_type == "note_on" and message.velocity == 0:
        return None
    if event_type == "note_off":
        return None

    key = message.note if event_type == "note_on" else message.control
    if event_type == "note_on":
        value = message.velocity
        state = "on"
    else:
        value = message.value
        state = None

    return MidiInputEvent(
        event_type=event_type,
        channel=message.channel,
        key=key,
        value=value,
        state=state,
        timestamp=datetime.now(timezone.utc),
        source_device=source_device,
    )
