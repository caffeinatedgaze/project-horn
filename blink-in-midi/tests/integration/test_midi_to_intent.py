from __future__ import annotations

from unittest.mock import MagicMock

from typer.testing import CliRunner

from blink_midi.cli import app



def test_demo_once_produces_session_summary(monkeypatch) -> None:
    response = MagicMock()
    response.status_code = 200
    response.json.return_value = {"status": "ok"}

    client = MagicMock()
    client.__enter__.return_value = client
    client.__exit__.return_value = None
    client.post.return_value = response

    monkeypatch.setattr("blink_midi.sender.httpx.Client", lambda timeout: client)

    runner = CliRunner()
    result = runner.invoke(
        app,
        [
            "run",
            "--device",
            "demo-device",
            "--api-url",
            "http://127.0.0.1:8000/midi/events",
            "--demo-once",
        ],
    )
    assert result.exit_code == 0
    assert "processed=1" in result.stdout
    assert "failures=0" in result.stdout
