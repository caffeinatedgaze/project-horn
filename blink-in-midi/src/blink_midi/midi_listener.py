from __future__ import annotations

from collections.abc import Iterator

import mido



def list_input_devices() -> list[str]:
    return list(mido.get_input_names())



def iter_midi_messages(device_name: str, demo_once: bool = False) -> Iterator[object]:
    if demo_once:
        yield mido.Message("note_on", note=60, velocity=100, channel=0)
        return

    with mido.open_input(device_name) as port:
        for message in port:
            yield message
