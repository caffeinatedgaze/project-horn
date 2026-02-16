from __future__ import annotations

from typing import Dict, List, Optional

MIDI_BULB_CHANNELS: List[int] = list(range(10))
MIDI_GROUP_CHANNEL = 10
MIDI_EXCEPT_CEILING_CHANNEL = 11
MIDI_CHANNEL_GROUP_MAP: Dict[int, str] = {
    MIDI_GROUP_CHANNEL: "all_bulbs",
    MIDI_EXCEPT_CEILING_CHANNEL: "except_ceiling",
}
MIDI_ALL_CHANNELS: List[int] = MIDI_BULB_CHANNELS + list(MIDI_CHANNEL_GROUP_MAP.keys())
MIDI_CHANNEL_MAX = MIDI_ALL_CHANNELS[-1]
MIDI_CHANNEL_MIN = MIDI_BULB_CHANNELS[0]
MIDI_NOTE_MAX = 17
MIDI_NOTE_MIN = 0
MIDI_NOTE_STEP_COUNT = MIDI_NOTE_MAX - MIDI_NOTE_MIN + 1
UNMAPPED_DEVICE_ID = "NONE"

# Shared source of truth for channel->bulb defaults.
DEFAULT_MIDI_BULB_ID_MAP: Dict[int, str] = {
    0: "0x3ccfb435d8988b8d",
    1: "0x3ccfb43613a08b93",
    2: "0x3ccfb43607d98b92",
    3: "0x3ccfb437793f8c4d",
    4: "0x3ccfb436f84e8c37",
    5: "0x3ccfb4362d078b96",
    6: "0x3ccfb4334dcc8ab1",
    7: "0x3ccfb43542b08b75",
}


def normalize_midi_bulb_ids(raw_ids: Optional[str]) -> List[str]:
    configured = [item.strip() for item in (raw_ids or "").split(",") if item.strip()]
    if not configured:
        return [DEFAULT_MIDI_BULB_ID_MAP.get(channel, UNMAPPED_DEVICE_ID) for channel in MIDI_BULB_CHANNELS]
    mapped = configured[: len(MIDI_BULB_CHANNELS)]
    while len(mapped) < len(MIDI_BULB_CHANNELS):
        mapped.append(UNMAPPED_DEVICE_ID)
    return mapped


def midi_channel_to_slot(channel: int) -> int:
    return channel


def midi_channel_to_device_id(channel: int, raw_ids: Optional[str]) -> Optional[str]:
    if channel in MIDI_CHANNEL_GROUP_MAP:
        return MIDI_CHANNEL_GROUP_MAP[channel]

    ids = normalize_midi_bulb_ids(raw_ids)
    slot = midi_channel_to_slot(channel)
    if slot < 0 or slot >= len(ids):
        return None
    device_id = ids[slot]
    return None if device_id == UNMAPPED_DEVICE_ID else device_id


def midi_note_to_brightness(note: int) -> int:
    # Step mapping: notes 0..17 map to discrete intensities 1..254.
    step = note - MIDI_NOTE_MIN
    return 1 + round(step * (253 / (MIDI_NOTE_STEP_COUNT - 1)))


def is_real_device_id(device_id: str) -> bool:
    return bool(device_id) and device_id != UNMAPPED_DEVICE_ID
