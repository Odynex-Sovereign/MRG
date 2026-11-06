"""Key HTML pages load."""

from fastapi.testclient import TestClient

from mrg.main import app

client = TestClient(app)

PAGES = [
    "/",
    "/pricing",
    "/institutions",
    "/demo",
    "/onboarding",
    "/dashboard",
    "/faq",
    "/security",
    "/accessibility",
    "/contact",
    "/legal/terms",
    "/legal/privacy",
]


def test_pages_ok():
    for path in PAGES:
        r = client.get(path)
        assert r.status_code == 200, path
        assert "text/html" in r.headers.get("content-type", "")


def test_home_has_value_prop():
    r = client.get("/")
    assert b"composure" in r.content.lower() or b"simulation" in r.content.lower()


def test_feedback_requires_message():
    r = client.post("/api/feedback", json={})
    assert r.status_code == 400


def test_feedback_accepts_message():
    r = client.post("/api/feedback", json={"message": "Great product", "category": "general"})
    assert r.status_code == 200
    assert r.json()["status"] == "received"
