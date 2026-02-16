from __future__ import annotations

import mido

from blink_midi.mapper import map_message


def test_maps_note_on_message() -> None:
    msg = mido.Message("note_on", note=64, velocity=112, channel=2)
    event = map_message(msg, "demo-device")
    assert event is not None
    assert event.event_type == "note_on"
    assert event.channel == 2
    assert event.key == 64
    assert event.value == 112
    assert event.state == "on"
    assert event.source_device == "demo-device"


def test_maps_control_change_message() -> None:
    msg = mido.Message("control_change", control=7, value=99, channel=1)
    event = map_message(msg, "demo-device")
    assert event is not None
    assert event.event_type == "control_change"
    assert event.key == 7
    assert event.value == 99
    assert event.state is None


def test_ignores_note_off_message() -> None:
    msg = mido.Message("note_off", note=60, velocity=20, channel=0)
    assert map_message(msg, "demo-device") is None


def test_ignores_note_on_zero_velocity() -> None:
    msg = mido.Message("note_on", note=60, velocity=0, channel=0)
    assert map_message(msg, "demo-device") is None


def test_ignores_unsupported_message() -> None:
    msg = mido.Message("pitchwheel", pitch=123, channel=0)
    assert map_message(msg, "demo-device") is None


def test_same_message_shape_is_deterministic() -> None:
    msg1 = mido.Message("note_on", note=60, velocity=20, channel=0)
    msg2 = mido.Message("note_on", note=60, velocity=20, channel=0)
    event1 = map_message(msg1, "demo-device")
    event2 = map_message(msg2, "demo-device")
    assert event1 is not None and event2 is not None
    assert event1.event_type == event2.event_type
    assert event1.channel == event2.channel
    assert event1.key == event2.key
    assert event1.value == event2.value
