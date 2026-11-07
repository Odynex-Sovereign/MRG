from fastapi.testclient import TestClient

import mrg.main as mrg_main

client = TestClient(mrg_main.app)


def test_fly_app_health_and_api_routes():
    assert client.get("/healthz").status_code == 200
    assert client.get("/readyz").status_code == 200
    assert client.get("/api/version").status_code == 200
    assert client.get("/api/pricing").status_code == 200
    assert client.post("/api/feedback", json={"message": "Works"}).status_code == 200


def test_demo_websocket_start_protocol(monkeypatch):
    async def fake_simulation(session, scenario_id):
        yield {"type": "scenario_start", "scenario": scenario_id}
        yield {"type": "scenario_complete", "metrics": {"composure_score": 80}, "debrief": "Done"}

    monkeypatch.setattr(mrg_main, "run_sandbox_simulation", fake_simulation)

    with client.websocket_connect("/ws/simulation") as websocket:
        assert websocket.receive_json()["type"] == "SYSTEM_STATUS"
        websocket.send_json({"action": "start", "scenario": "macro_shock"})
        assert websocket.receive_json() == {"type": "scenario_start", "scenario": "macro_shock"}
        assert websocket.receive_json()["type"] == "scenario_complete"


def test_crisis_websocket_protocol_still_works():
    with client.websocket_connect("/ws/simulation") as websocket:
        assert websocket.receive_json()["type"] == "SYSTEM_STATUS"
        websocket.send_json({"action": "TRIGGER_CRISIS", "prompt": "test incident"})
        assert websocket.receive_json()["type"] == "MACRO_COGNITIVE_UPDATE"
        assert websocket.receive_json()["type"] == "SENSORY_STREAM_INFO"
