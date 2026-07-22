"""Smoke test - verifies omnixys-config can be imported."""

from __future__ import annotations

import importlib
from importlib.metadata import version as pkg_version


def test_package_importable() -> None:
    mod = importlib.import_module("config")
    assert hasattr(mod, "__version__")
    assert mod.__version__ == pkg_version("omnixys-config")


def test_public_api() -> None:
    from config import factories

    assert factories is not None
