from __future__ import annotations

# ruff: noqa: D100, D103
from functools import lru_cache

from omnixys_config.settings import AppSettings


@lru_cache(maxsize=1)
def load_settings() -> AppSettings:
    return AppSettings()


def get_settings() -> AppSettings:
    return load_settings()
