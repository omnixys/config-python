from __future__ import annotations

from typing import TYPE_CHECKING

from config.settings import AppSettings

if TYPE_CHECKING:
    from pathlib import Path


def load_settings(env_file: str | Path | None = None) -> AppSettings:
    if env_file is not None:
        return AppSettings(_env_file=str(env_file))  # type: ignore[call-arg]
    return AppSettings()


def get_settings(env_file: str | Path | None = None) -> AppSettings:
    return load_settings(env_file)
