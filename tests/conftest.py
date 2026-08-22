# @license GPL-3.0-or-later
# Copyright (C) 2025 Caleb Gyamfi - Omnixys Technologies
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# For more information, visit <https://www.gnu.org/licenses/>.

"""Shared fixtures: deterministic environment isolation for settings tests."""

from __future__ import annotations

import os

import pytest

_FLAT_KEYS = {
    "service_name",
    "environment",
    "log_level",
    "host",
    "port",
    "debug",
    "internal_api_key",
    "hot_reload",
}

_PREFIXES = (
    "database_",
    "keycloak_",
    "jwk_",
    "session_",
    "rate_limit_",
    "security_",
    "topic_",
    "kafka_",
    "cache_",
    "otel_",
    "storage_",
)


@pytest.fixture(autouse=True)
def clean_env(monkeypatch: pytest.MonkeyPatch) -> None:
    for key in list(os.environ):
        lower = key.lower()
        if lower in _FLAT_KEYS or lower.startswith(_PREFIXES):
            monkeypatch.delenv(key, raising=False)
