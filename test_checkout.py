"""Tests for checkout session creation and configuration validation."""

import os
from unittest import mock

import pytest
from fastapi.testclient import TestClient

# Ensure sandbox path is used
os.environ.pop("STRIPE_SECRET_KEY", None)
os.environ.pop("STRIPE_API_KEY", None)


@pytest.fixture
def client():
    from services.streaming.websocket_pipeline import app

    return TestClient(app)


def test_healthz(client):
    r = client.get("/healthz")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "healthy"
    assert "billing_configured" in data


def test_checkout_unknown_tier(client):
    r = client.post(
        "/billing/v1/checkout/create-session",
        json={"session_id": "s1", "tier_id": "tier_nonexistent"},
    )
    assert r.status_code == 400


def test_checkout_sandbox_no_stripe(client):
    r = client.post(
        "/billing/v1/checkout/create-session",
        json={"session_id": "session_abc", "tier_id": "tier_2"},
    )
    assert r.status_code == 200
    data = r.json()
    assert data["mode"] == "sandbox"
    assert data["checkout_url"] is None
    assert data["error"] == "stripe_not_configured"
    assert "not configured" in (data.get("message") or "").lower()


def test_checkout_valid_tier_ids(client):
    for tier in ("tier_1", "tier_2", "tier_3"):
        r = client.post(
            "/billing/v1/checkout/create-session",
            json={"session_id": f"s_{tier}", "tier_id": tier},
        )
        assert r.status_code == 200, tier
        data = r.json()
        assert data["mode"] == "sandbox"
        assert data["checkout_url"] is None


def test_homepage_serves_html(client):
    r = client.get("/")
    assert r.status_code == 200
    assert "Institutional Matrix Allocation" in r.text
    assert "alert(" not in r.text
