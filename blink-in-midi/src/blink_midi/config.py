from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class RuntimeConfig:
    api_url: str
    log_level: str = "INFO"



def load_config(api_url: str | None = None, log_level: str | None = None) -> RuntimeConfig:
    resolved_api_url = api_url or os.getenv("API_URL", "http://127.0.0.1:8000/midi/events")
    resolved_log_level = (log_level or os.getenv("LOG_LEVEL", "INFO")).upper()
    return RuntimeConfig(api_url=resolved_api_url, log_level=resolved_log_level)
