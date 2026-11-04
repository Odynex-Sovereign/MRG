from fastapi.testclient import TestClient

from services.streaming import websocket_pipeline

client = TestClient(websocket_pipeline.app)


def test_homepage_serves_browser_ui():
    response = client.get("/")

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "MRG Simulation Grid" in response.text


def test_health_check():
    response = client.get("/healthz")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["engine"] == "MRG Planet-Scale Grid"


def test_websocket_crisis_action_works_without_external_services(monkeypatch):
    async def fake_macro_ripple(prompt: str) -> str:
        return f"sandbox analysis: {prompt}"

    async def fake_synthesize_speech(text: str) -> bytes:
        return b"test-audio"

    monkeypatch.setattr(websocket_pipeline, "generate_macro_ripple", fake_macro_ripple)
    monkeypatch.setattr(websocket_pipeline, "synthesize_speech_stream", fake_synthesize_speech)

    with client.websocket_connect("/ws/simulation") as websocket:
        assert websocket.receive_json()["type"] == "SYSTEM_STATUS"
        websocket.send_json({"action": "TRIGGER_CRISIS", "prompt": "test incident"})
        analysis = websocket.receive_json()
        audio = websocket.receive_json()

    assert analysis["type"] == "MACRO_COGNITIVE_UPDATE"
    assert analysis["payload"]["analysis"] == "sandbox analysis: test incident"
    assert audio["type"] == "SENSORY_STREAM_INFO"
    assert audio["payload"]["audio_chunk_size"] == len(b"test-audio")
