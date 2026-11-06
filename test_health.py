"""Health and readiness endpoints."""

from fastapi.testclient import TestClient

from mrg.main import app

client = TestClient(app)


def test_healthz():
    r = client.get("/healthz")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "ok"
    assert "version" in data


def test_readyz():
    r = client.get("/readyz")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "ready"
    assert "billing_configured" in data


def test_version_api():
    r = client.get("/api/version")
    assert r.status_code == 200
    assert "version" in r.json()
