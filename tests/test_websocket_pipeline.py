import pytest
from fastapi.testclient import TestClient

from services.streaming.websocket_pipeline import app


client = TestClient(app)


def test_health_check():
    response = client.get("/healthz")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["engine"] == "ODYNEX_AXIS_LOGISTICS"


def test_websocket_accepts_valid_telemetry_packet():
    with client.websocket_connect("/ws/simulation") as websocket:
        payload = {
            "user_id": "user-123",
            "session_id": "session-abc",
            "vertical": "Higher-Ed",
            "vocal_pitch_variance": 24.5,
            "vocal_energy": 68.2,
            "response_latency_ms": 320,
            "user_raw_text": "I believe my research methodology stands on solid data points despite the critique.",
        }

        websocket.send_json(payload)
        response = websocket.receive_json()

        assert response["session"]["user_id"] == "user-123"
        assert response["session"]["session_id"] == "session-abc"
        assert response["telemetry"]["vocal_stress_index"] >= 0
        assert response["nvidia_audio2face_trigger"]["expression_profile"] in {
            "skeptical_brow_raise",
            "calculated_neutral",
        }


def test_websocket_rejects_invalid_packet():
    with client.websocket_connect("/ws/simulation") as websocket:
        websocket.send_json({"user_id": "user-123"})
        response = websocket.receive_json()

        assert response["error"] == "invalid_packet"
        assert "detail" in response
