"""Health and info endpoint tests."""


def test_liveness(client):
    r = client.get("/healthz")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "healthy"
    assert "version" in body


def test_readiness_sandbox(client):
    r = client.get("/readyz")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "ready"
    assert body["checks"]["database"] == "not_configured"


def test_info(client):
    r = client.get("/info")
    assert r.status_code == 200
    body = r.json()
    assert body["name"]
    assert body["version"]
    assert body["sandbox_mode"] is True


def test_homepage(client):
    r = client.get("/")
    assert r.status_code == 200
    # HTML UI or JSON fallback
    assert r.headers["content-type"].startswith(("text/html", "application/json"))


def test_security_headers(client):
    r = client.get("/healthz")
    assert r.headers.get("X-Content-Type-Options") == "nosniff"
    assert r.headers.get("X-Frame-Options") == "DENY"
    assert "X-Process-Time-Ms" in r.headers
