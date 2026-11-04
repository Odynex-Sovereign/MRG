"""Pricing and demo checkout API tests."""

from mrg.pricing import get_plan, get_public_plans


def test_public_plans_structure():
    plans = get_public_plans()
    assert len(plans) >= 4
    ids = {p["id"] for p in plans}
    assert "free" in ids and "enterprise" in ids


def test_get_plan():
    assert get_plan("starter")["price_monthly"] == 49
    assert get_plan("missing") is None


def test_pricing_api(client):
    r = client.get("/api/pricing")
    assert r.status_code == 200
    body = r.json()
    assert "plans" in body and body["meta"]["currency"] == "USD"


def test_demo_checkout(client):
    r = client.post(
        "/api/checkout/demo",
        json={
            "plan_id": "starter",
            "billing_interval": "month",
            "email": "user@example.com",
            "accept_terms": True,
        },
    )
    assert r.status_code == 200
    assert r.json()["status"] == "demo_success"


def test_demo_checkout_requires_terms(client):
    r = client.post(
        "/api/checkout/demo",
        json={
            "plan_id": "starter",
            "billing_interval": "month",
            "email": "user@example.com",
            "accept_terms": False,
        },
    )
    assert r.status_code == 400


def test_metrics_demo(client):
    r = client.get("/api/metrics/demo")
    assert r.status_code == 200
    assert "DEMO" in r.json()["label"]


def test_pricing_page(client):
    r = client.get("/pricing")
    assert r.status_code == 200
    assert "text/html" in r.headers["content-type"]
