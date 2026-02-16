#!/usr/bin/env python3
import os
import json
import time
from pathlib import Path
import sys
import paho.mqtt.client as mqtt

CONTROL_API_DIR = Path(__file__).resolve().parents[1] / "infra" / "control-api"
if str(CONTROL_API_DIR) not in sys.path:
    sys.path.insert(0, str(CONTROL_API_DIR))

from control_api.midi_mapping import is_real_device_id, normalize_midi_bulb_ids

DEVICE_IDS = [
    device_id
    for device_id in normalize_midi_bulb_ids(os.getenv("MIDI_BULB_IDS"))
    if is_real_device_id(device_id)
]

MQTT_HOST = os.getenv("MQTT_HOST", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))

BRIGHTNESS_VALUES = [2, 200]
INTERVAL_SEC = 0.2


def main() -> None:
    client = mqtt.Client()
    client.connect(MQTT_HOST, MQTT_PORT, keepalive=60)
    client.loop_start()

    brightness = BRIGHTNESS_VALUES[0]
    index = 0
    try:
        while True:
            index = 1 - index
            brightness = BRIGHTNESS_VALUES[index]
            payload = {"state": "ON", "brightness": brightness}
            for device_id in DEVICE_IDS:
                topic = f"zigbee2mqtt/{device_id}/set"
                client.publish(topic, json.dumps(payload))
            time.sleep(INTERVAL_SEC)
    except KeyboardInterrupt:
        pass
    finally:
        client.loop_stop()
        client.disconnect()


if __name__ == "__main__":
    main()
