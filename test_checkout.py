"""Tests for the deployed checkout route and configuration behavior."""

from types import SimpleNamespace

import pytest
from fastapi.testclient import TestClient


@pytest.fixture

def client():
    from services.streaming.websocket_pipeline import app

    return TestClient(app)


def test_healthz_reports_billing_configuration(client, monkeypatch):
    monkeypatch.delenv("STRIPE_SECRET_KEY", raising=False)
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    assert response.json()["billing_configured"] is False


def test_checkout_unknown_tier_is_rejected(client):
    response = client.post(
        "/billing/v1/checkout/create-session",
        json={"session_id": "s1", "tier_id": "tier_nonexistent"},
    )
    assert response.status_code == 400


def test_checkout_without_stripe_is_sandbox_only(client, monkeypatch):
    monkeypatch.delenv("STRIPE_SECRET_KEY", raising=False)
    response = client.post(
        "/billing/v1/checkout/create-session",
        json={"session_id": "session_abc", "tier_id": "tier_2"},
    )
    assert response.status_code == 200
    assert response.json()["mode"] == "sandbox"
    assert response.json()["checkout_url"] is None
    assert response.json()["error"] == "stripe_not_configured"


@pytest.mark.parametrize(
    ("tier_id", "amount"),
    [("tier_1", 1_500_000), ("tier_2", 3_500_000), ("tier_3", 16_000_000)],
)
def test_checkout_creates_stripe_hosted_session(client, monkeypatch, tier_id, amount):
    import stripe

    monkeypatch.setenv("STRIPE_SECRET_KEY", "sk_test_unit_test_only")
    expected = {"url": "https://checkout.stripe.com/test-session", "id": "cs_test_123"}
    captured = {}

    def create_session(**kwargs):
        captured.update(kwargs)
        return SimpleNamespace(**expected)

    monkeypatch.setattr(stripe.checkout.Session, "create", create_session)
    response = client.post(
        "/billing/v1/checkout/create-session",
        json={"session_id": "session_test", "tier_id": tier_id},
    )

    assert response.status_code == 200
    assert response.json() == {
        "mode": "live",
        "checkout_url": expected["url"],
        "session_id": expected["id"],
    }
    assert captured["mode"] == "subscription"
    assert captured["line_items"][0]["price_data"]["unit_amount"] == amount
    assert captured["line_items"][0]["price_data"]["recurring"]["interval"] == "month"
    assert captured["client_reference_id"] == "session_test"
    assert "{CHECKOUT_SESSION_ID}" in captured["success_url"]


def test_homepage_serves_checkout_ui(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "Institutional Matrix Allocation" in response.text
    assert "/billing/v1/checkout/create-session" in response.text
