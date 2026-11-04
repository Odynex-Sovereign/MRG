# tests/test_premium_sensory.py
import pytest
from fastapi.testclient import TestClient
from services.streaming.websocket_pipeline import app

def test_seamless_premium_sensory_degradation():
    client = TestClient(app)
    
    # Test Standard Tier connection: Ensure it loads normally and ignores extra sensory threads
    with client.websocket_connect("/ws/simulation/test_session_std?user_tier=Standard") as websocket:
        websocket.send_json({"action": "ping"})
        # No sensory worker spawned, handles pipeline gracefully

    # Test Premium Tier connection: Ensure non-blocking serialization works
    with client.websocket_connect("/ws/simulation/test_session_prem?user_tier=Premium_Research") as websocket:
        websocket.send_json({
            "action": "trigger_crisis_event",
            "scent_trigger": "AGRI_CROP_ROT_FUNGAL_04"
        })
        
        # Pull the emitted event frame
        response = websocket.receive_json()
        assert response["event"] == "SENSORY_TELEMETRY"
        assert response["data"]["scent_profile_id"] == "AGRI_CROP_ROT_FUNGAL_04"
        assert response["data"]["haptic_intensity"] == 0.85
