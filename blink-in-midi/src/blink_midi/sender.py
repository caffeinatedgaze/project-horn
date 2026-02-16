from __future__ import annotations

import json
import logging

import httpx

from .models import MidiEventPayload, MidiInputEvent, OutboundRequestIntent

logger = logging.getLogger(__name__)



def event_to_payload(event: MidiInputEvent) -> MidiEventPayload:
    return MidiEventPayload(
        event_type=event.event_type,
        channel=event.channel,
        key=event.key,
        value=event.value,
        state=event.state,
        timestamp=event.timestamp,
    )



def build_request_intent(event: MidiInputEvent, api_url: str) -> OutboundRequestIntent:
    payload = event_to_payload(event)
    return OutboundRequestIntent(
        method="POST",
        url=api_url,
        headers={"Content-Type": "application/json", "Accept": "application/json"},
        payload=payload,
        simulated_sent=True,
    )



def process_intent(intent: OutboundRequestIntent) -> OutboundRequestIntent:
    try:
        payload = MidiEventPayload.model_validate(intent.payload)
        payload_json = payload.model_dump(mode="json")

        with httpx.Client(timeout=2.0) as client:
            response = client.post(intent.url, json=payload_json, headers=intent.headers)

        if response.status_code != 200:
            try:
                error_body = response.json()
            except ValueError:
                error_body = {}
            message = error_body.get("message", response.text)
            raise ValueError(f"api returned {response.status_code}: {message}")

        response_body = response.json()
        if response_body.get("status") != "ok":
            raise ValueError(f"unexpected api response status: {response_body!r}")

        logger.info(
            "outbound_request_sent %s",
            json.dumps(
                {
                    "method": intent.method,
                    "url": intent.url,
                    "payload": payload_json,
                    "status_code": 200,
                }
            ),
        )

        return intent
    except Exception as exc:  # pragma: no cover - defensive for runtime
        failed = intent.model_copy(update={"failure_reason": str(exc), "simulated_sent": False})
        logger.error("outbound_intent_failure event=%s reason=%s", failed.payload, failed.failure_reason)
        return failed



def process_event(event: MidiInputEvent, api_url: str) -> OutboundRequestIntent:
    try:
        intent = build_request_intent(event, api_url)
    except Exception as exc:
        return OutboundRequestIntent(
            method="POST",
            url="http://invalid.local",
            headers={"Content-Type": "application/json"},
            payload=MidiEventPayload(
                event_type=event.event_type,
                channel=event.channel,
                key=event.key,
                value=event.value,
                state=event.state,
                timestamp=event.timestamp,
            ),
            simulated_sent=False,
            failure_reason=str(exc),
        )
    return process_intent(intent)
