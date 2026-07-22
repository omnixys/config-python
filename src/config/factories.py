from __future__ import annotations

# ruff: noqa: D100, D103
from typing import TYPE_CHECKING

from config.settings import AppSettings

if TYPE_CHECKING:
    from pathlib import Path


def load_settings(env_file: str | Path | None = None) -> AppSettings:
    if env_file is not None:
        return AppSettings(_env_file=str(env_file))
    return AppSettings()


def get_settings(env_file: str | Path | None = None) -> AppSettings:
    return load_settings(env_file)
