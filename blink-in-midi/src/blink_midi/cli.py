from __future__ import annotations

import logging

import typer

from .config import load_config
from .midi_listener import iter_midi_messages, list_input_devices
from .mapper import map_message
from .models import BridgeSession
from .sender import process_event

app = typer.Typer(help="MIDI input bridge for local API request intents")



def configure_logging(level: str) -> None:
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )


@app.command()
def devices() -> None:
    """List available MIDI input devices."""
    for name in list_input_devices():
        typer.echo(name)


@app.command()
def run(
    device: str = typer.Option(..., help="MIDI input device name"),
    api_url: str | None = typer.Option(None, help="Local API endpoint URL"),
    log_level: str | None = typer.Option(None, help="Logging level"),
    demo_once: bool = typer.Option(False, help="Run once with a simulated MIDI event"),
) -> None:
    """Process MIDI events and emit outbound request intents."""
    cfg = load_config(api_url=api_url, log_level=log_level)
    configure_logging(cfg.log_level)

    session = BridgeSession(selected_device=device, api_url=cfg.api_url)

    for message in iter_midi_messages(device, demo_once=demo_once):
        event = map_message(message, source_device=device)
        if event is None:
            session.ignored_events += 1
            continue

        intent = process_event(event, cfg.api_url)
        if intent.failure_reason:
            session.intent_failures += 1
        else:
            session.processed_events += 1

        if demo_once:
            break

    typer.echo(
        f"session={session.session_id} processed={session.processed_events} "
        f"ignored={session.ignored_events} failures={session.intent_failures}"
    )



def main() -> None:
    app()


if __name__ == "__main__":
    main()
