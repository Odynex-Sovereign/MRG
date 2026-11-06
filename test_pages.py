from fastapi.testclient import TestClient
from mrg.main import app

client = TestClient(app)
PAGES = ["/", "/pricing", "/institutions", "/demo", "/onboarding", "/dashboard", "/faq", "/security", "/accessibility", "/contact", "/legal/terms", "/legal/privacy"]

def test_pages_ok():
    for path in PAGES:
        r = client.get(path)
        assert r.status_code == 200, path
        assert "text/html" in r.headers.get("content-type", "")
        assert "{% extends" not in r.text, path
        assert "{% for" not in r.text, path
        assert "{{ " not in r.text, path

def test_home_has_value_prop():
    r = client.get("/")
    assert "Train for the day" in r.text
    assert "/static/css/main.css" in r.text

def test_css_served():
    r = client.get("/static/css/main.css")
    assert r.status_code == 200
    assert "--mrg-orange" in r.text

def test_feedback_requires_message():
    assert client.post("/api/feedback", json={}).status_code == 400

def test_feedback_accepts_message():
    r = client.post("/api/feedback", json={"message": "Great", "category": "general"})
    assert r.status_code == 200
    assert r.json()["status"] == "received"
