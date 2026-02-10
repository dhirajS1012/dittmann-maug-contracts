from __future__ import annotations

from datetime import datetime, timezone


def ts() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def info(msg: str) -> None:
    print(f"[{ts()}] {msg}")
