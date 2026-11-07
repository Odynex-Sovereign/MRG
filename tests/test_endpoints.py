from fastapi.testclient import TestClient
from mrg.main import app

client = TestClient(app)

def test_liveness():
    res = client.get("/healthz")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"

def test_metrics_probe():
    res = client.get("/metrics")
    assert res.status_code == 200
