"""Shared pytest fixtures."""

from __future__ import annotations

import os

import pytest
from fastapi.testclient import TestClient

# Force sandbox mode for unit tests
os.environ.setdefault("ENVIRONMENT", "test")
os.environ.setdefault("LOG_FORMAT", "text")
os.environ.setdefault("LOG_LEVEL", "WARNING")
os.environ.pop("DATABASE_URL", None)
os.environ.pop("DEEPSEEK_API_KEY", None)
os.environ.pop("NVIDIA_NIM_API_KEY", None)

from mrg.app import create_app
from mrg.config import get_settings


@pytest.fixture(autouse=True)
def clear_settings_cache():
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()


@pytest.fixture
def settings():
    get_settings.cache_clear()
    return get_settings()


@pytest.fixture
def app(settings):
    return create_app(settings)


@pytest.fixture
def client(app):
    with TestClient(app) as c:
        yield c
