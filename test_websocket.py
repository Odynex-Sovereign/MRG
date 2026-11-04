"""WebSocket simulation tests."""

import json


def test_ws_telemetry_flow(client):
    with client.websocket_connect("/ws/simulation") as ws:
        status = ws.receive_json()
        assert status["type"] == "SYSTEM_STATUS"

        packet = {
            "user_id": "usr_test",
            "session_id": "ses_test",
            "vertical": "Higher-Ed",
            "vocal_pitch_variance": 24.5,
            "vocal_energy": 68.2,
            "response_latency_ms": 320,
            "user_raw_text": "Research methodology critique response.",
        }
        ws.send_text(json.dumps(packet))
        macro = ws.receive_json()
        assert macro["type"] == "MACRO_COGNITIVE_UPDATE"
        assert "analysis" in macro["payload"]

        sensory = ws.receive_json()
        assert sensory["type"] == "SENSORY_STREAM_INFO"
        assert sensory["payload"]["audio_chunk_size"] > 0


def test_ws_crisis_action(client):
    with client.websocket_connect("/ws/simulation") as ws:
        ws.receive_json()  # status
        ws.send_text(json.dumps({"action": "TRIGGER_CRISIS", "prompt": "Oil shock"}))
        macro = ws.receive_json()
        assert macro["type"] == "MACRO_COGNITIVE_UPDATE"


def test_ws_invalid_json(client):
    with client.websocket_connect("/ws/simulation") as ws:
        ws.receive_json()
        ws.send_text("not-json")
        err = ws.receive_json()
        assert err["type"] == "SYSTEM_ERROR"


def test_ws_missing_prompt(client):
    with client.websocket_connect("/ws/simulation") as ws:
        ws.receive_json()
        ws.send_text(json.dumps({"vertical": "MIL"}))
        err = ws.receive_json()
        assert err["type"] == "SYSTEM_ERROR"
