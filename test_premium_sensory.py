from fastapi.testclient import TestClient

from services.streaming import websocket_pipeline

client = TestClient(websocket_pipeline.app)


def test_sensory_response_works_in_sandbox(monkeypatch):
    async def fake_macro_ripple(prompt: str) -> str:
        return f"sandbox analysis: {prompt}"

    async def fake_synthesize_speech(text: str) -> bytes:
        return b"sandbox-audio"

    monkeypatch.setattr(websocket_pipeline, "generate_macro_ripple", fake_macro_ripple)
    monkeypatch.setattr(websocket_pipeline, "synthesize_speech_stream", fake_synthesize_speech)

    with client.websocket_connect("/ws/simulation") as websocket:
        assert websocket.receive_json()["type"] == "SYSTEM_STATUS"
        websocket.send_json({"action": "TRIGGER_CRISIS", "prompt": "sensory fallback"})
        analysis = websocket.receive_json()
        audio = websocket.receive_json()

    assert analysis["payload"]["analysis"] == "sandbox analysis: sensory fallback"
    assert audio["type"] == "SENSORY_STREAM_INFO"
    assert audio["payload"]["audio_chunk_size"] == len(b"sandbox-audio")
