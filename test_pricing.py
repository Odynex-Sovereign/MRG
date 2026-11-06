"""Pricing API and plan consistency."""

from fastapi.testclient import TestClient

from mrg.core.pricing import PLANS, list_public_plans
from mrg.main import app

client = TestClient(app)


def test_pricing_api():
    r = client.get("/api/pricing")
    assert r.status_code == 200
    data = r.json()
    assert data["currency"] == "USD"
    assert len(data["plans"]) >= 5
    ids = {p["id"] for p in data["plans"]}
    assert "free" in ids
    assert "personal" in ids
    assert "enterprise" in ids


def test_free_plan_is_zero():
    free = PLANS["free"]
    assert free.monthly_usd == 0
    assert free.entitlements.max_simulations_per_month == 3


def test_personal_affordable():
    p = PLANS["personal"]
    assert p.monthly_usd == 5
    assert p.annual_usd == 50
    assert p.entitlements.black_swan_challenges is True


def test_list_public_plans_serializable():
    plans = list_public_plans()
    assert isinstance(plans, list)
    for p in plans:
        assert "id" in p
        assert "features" in p
        assert "entitlements" in p
