from __future__ import annotations

import json
import logging
import os
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional
from uuid import uuid4

import paho.mqtt.client as mqtt
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from control_api.midi_mapping import (
    MIDI_ALL_CHANNELS,
    MIDI_BULB_CHANNELS,
    MIDI_CHANNEL_GROUP_MAP,
    MIDI_CHANNEL_MAX,
    MIDI_CHANNEL_MIN,
    MIDI_NOTE_MAX,
    MIDI_NOTE_MIN,
    midi_channel_to_device_id as mapping_channel_to_device_id,
    midi_channel_to_slot,
    midi_note_to_brightness,
    normalize_midi_bulb_ids,
)

MQTT_HOST = os.getenv("MQTT_HOST", "mosquitto")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
Z2M_DATA_DIR = Path(os.getenv("Z2M_DATA_DIR", "/app/zigbee2mqtt-data"))
GROUPS_FILE = Path(os.getenv("GROUPS_FILE", "/app/data/groups.json"))

app = FastAPI(title="Zigbee Demo Control API")
logger = logging.getLogger("uvicorn.error")


class PairingStartRequest(BaseModel):
    duration_seconds: int = Field(default=180, ge=30, le=600)


class DeviceStateRequest(BaseModel):
    state: Optional[str] = None
    brightness: Optional[int] = Field(default=None, ge=0, le=254)


class GroupCreateRequest(BaseModel):
    name: str
    device_ids: List[str]


class MidiEventRequest(BaseModel):
    event_type: Optional[str] = None
    channel: int = Field(ge=0, le=15)
    key: Optional[int] = Field(default=None, ge=MIDI_NOTE_MIN, le=MIDI_NOTE_MAX)
    timestamp: Optional[str] = None


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class MqttClient:
    def __init__(self) -> None:
        self.client = mqtt.Client()
        self.client.on_message = self._on_message
        self.client.on_connect = self._on_connect
        self.status_map: Dict[str, str] = {}
        self._lock = threading.Lock()

    def connect(self) -> None:
        self.client.connect(MQTT_HOST, MQTT_PORT, keepalive=60)
        self.client.loop_start()

    def _on_connect(self, client, _userdata, _flags, _rc) -> None:
        client.subscribe("zigbee2mqtt/+/availability")
        client.subscribe("zigbee2mqtt/+")

    def _on_message(self, _client, _userdata, msg) -> None:
        topic = msg.topic
        payload = msg.payload.decode("utf-8", errors="ignore")
        parts = topic.split("/")
        if len(parts) < 2 or parts[0] != "zigbee2mqtt":
            return
        device_id = parts[1]
        suffix = parts[2] if len(parts) > 2 else None

        if suffix == "availability":
            status = "available" if payload.lower() == "online" else "unavailable"
            with self._lock:
                self.status_map[device_id] = status
            return

        try:
            data = json.loads(payload)
            if isinstance(data, dict) and "availability" in data:
                status = "available" if str(data["availability"]).lower() == "online" else "unavailable"
                with self._lock:
                    self.status_map[device_id] = status
        except json.JSONDecodeError:
            return

    def publish_json(self, topic: str, payload: Dict[str, Any], source: str = "unknown") -> bool:
        serialized = json.dumps(payload, sort_keys=True, separators=(",", ":"))
        self.client.publish(topic, serialized)
        logger.info(
            "z2m_request source=%s published=%s topic=%s payload=%s",
            source,
            True,
            topic,
            serialized,
        )
        return True

    def get_status(self, device_id: str) -> str:
        with self._lock:
            return self.status_map.get(device_id, "unavailable")


mqtt_client = MqttClient()


@app.on_event("startup")
def startup() -> None:
    mqtt_client.connect()


def read_devices() -> List[Dict[str, Any]]:
    devices_file = Z2M_DATA_DIR / "devices.json"
    if devices_file.exists():
        try:
            return json.loads(devices_file.read_text())
        except json.JSONDecodeError:
            return []
    return []


def to_device(raw: Dict[str, Any]) -> Dict[str, Any]:
    device_id = raw.get("ieee_address") or raw.get("friendly_name") or raw.get("device_id") or "unknown"
    return {
        "device_id": device_id,
        "friendly_name": raw.get("friendly_name") or raw.get("name") or device_id,
        "status": mqtt_client.get_status(device_id),
        "last_seen_at": raw.get("last_seen"),
        "capabilities": raw.get("definition") or {},
    }


def list_devices() -> List[Dict[str, Any]]:
    return [to_device(d) for d in read_devices()]


def get_device(device_id: str) -> Optional[Dict[str, Any]]:
    for d in list_devices():
        if d["device_id"] == device_id:
            return d
    return None


def list_groups() -> List[Dict[str, Any]]:
    if not GROUPS_FILE.exists():
        return []
    try:
        return json.loads(GROUPS_FILE.read_text())
    except json.JSONDecodeError:
        return []


def save_groups(groups: List[Dict[str, Any]]) -> None:
    GROUPS_FILE.parent.mkdir(parents=True, exist_ok=True)
    GROUPS_FILE.write_text(json.dumps(groups, indent=2))


def midi_bulb_ids() -> List[str]:
    return normalize_midi_bulb_ids(os.getenv("MIDI_BULB_IDS"))


def midi_channel_to_device_id(channel: int) -> Optional[str]:
    return mapping_channel_to_device_id(channel, os.getenv("MIDI_BULB_IDS"))


@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok"}


@app.post("/pairing/start")
def pairing_start(body: PairingStartRequest) -> Dict[str, Any]:
    session = {
        "session_id": str(uuid4()),
        "status": "active",
        "started_at": now_iso(),
        "paired_device_ids": [],
    }
    mqtt_client.publish_json(
        "zigbee2mqtt/bridge/request/permit_join",
        {"value": True, "time": body.duration_seconds},
        source="pairing_start",
    )
    return session


@app.post("/pairing/stop")
def pairing_stop() -> Dict[str, Any]:
    mqtt_client.publish_json("zigbee2mqtt/bridge/request/permit_join", {"value": False}, source="pairing_stop")
    return {
        "session_id": "none",
        "status": "completed",
        "started_at": now_iso(),
        "ended_at": now_iso(),
    }


@app.get("/devices")
def devices() -> List[Dict[str, Any]]:
    return list_devices()


@app.get("/devices/{device_id}")
def device_detail(device_id: str) -> Dict[str, Any]:
    device = get_device(device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return device


@app.post("/devices/{device_id}/state")
def device_state(device_id: str, body: DeviceStateRequest) -> Dict[str, Any]:
    mqtt_client.publish_json(
        f"zigbee2mqtt/{device_id}/set",
        {"state": body.state, "brightness": body.brightness},
        source="device_state",
    )
    return get_device(device_id) or {"device_id": device_id}


@app.post("/devices/{device_id}/refresh")
def device_refresh(device_id: str) -> Dict[str, Any]:
    mqtt_client.publish_json("zigbee2mqtt/bridge/request/device/refresh", {"id": device_id}, source="device_refresh")
    return get_device(device_id) or {"device_id": device_id}


@app.get("/groups")
def groups() -> List[Dict[str, Any]]:
    return list_groups()


@app.post("/groups")
def create_group(body: GroupCreateRequest) -> Dict[str, Any]:
    groups = list_groups()
    group_id = body.name.lower().replace(" ", "-")
    if any(g["name"] == body.name or g["group_id"] == group_id for g in groups):
        raise HTTPException(status_code=400, detail="Group already exists")
    group = {"group_id": group_id, "name": body.name, "device_ids": body.device_ids}
    groups.append(group)
    save_groups(groups)
    return group


@app.post("/groups/{group_id}/state")
def group_state(group_id: str, body: DeviceStateRequest) -> Dict[str, Any]:
    mqtt_client.publish_json(
        f"zigbee2mqtt/{group_id}/set",
        {"state": body.state, "brightness": body.brightness},
        source="group_state",
    )
    return {"group_id": group_id, "state": body.state, "brightness": body.brightness}


@app.get("/midi/mapping")
def midi_mapping() -> List[Dict[str, Any]]:
    device_ids = midi_bulb_ids()
    mapping: List[Dict[str, Any]] = []
    for channel in MIDI_ALL_CHANNELS:
        if channel in MIDI_CHANNEL_GROUP_MAP:
            mapping.append(
                {
                    "channel": channel,
                    "slot": channel,
                    "device_id": MIDI_CHANNEL_GROUP_MAP[channel],
                }
            )
            continue

        index = channel
        mapping.append(
            {
                "channel": channel,
                "slot": index,
                "device_id": device_ids[index] if index < len(device_ids) else None,
            }
        )
    return mapping


@app.post("/midi/events")
def midi_event(body: MidiEventRequest) -> Dict[str, Any]:
    if body.channel < MIDI_CHANNEL_MIN or body.channel > MIDI_CHANNEL_MAX:
        raise HTTPException(status_code=400, detail="Channel is outside mapped range 0..11")

    device_id = midi_channel_to_device_id(body.channel)
    if not device_id:
        raise HTTPException(
            status_code=400,
            detail="Channel is not mapped to a real bulb ID. Configure MIDI_BULB_IDS with real IDs.",
        )

    # Turn OFF when note ends (note_off) or when there is no note value.
    # Otherwise use the note to drive intensity.
    if body.event_type == "note_off" or body.key is None:
        brightness = 0
    else:
        brightness = midi_note_to_brightness(body.key)

    payload = {"brightness": brightness}
    mqtt_client.publish_json(f"zigbee2mqtt/{device_id}/set", payload, source="midi_event")

    return {
        "device_id": device_id,
        "slot": midi_channel_to_slot(body.channel),
        "key": body.key,
        "event_type": body.event_type,
        "channel": body.channel,
        "brightness": brightness,
        "timestamp": body.timestamp,
        "mqtt_topic": f"zigbee2mqtt/{device_id}/set",
        "mqtt_payload": payload,
    }


def run() -> None:
    import uvicorn

    port = int(os.getenv("CONTROL_API_PORT", "8080"))
    uvicorn.run(app, host="0.0.0.0", port=port)
