# Insert within the telemetry parsing logic block of the WebSocket server:
if data_json.get("vertical") == "Higher-Ed":
    # Extrapolate youth-centric pressure models
    payload_out["telemetry"].update({
        "peer_pressure_resistance": max(0, 100 - int(stress_index * 1.1)),
        "rhetorical_defense_rating": min(100, int((packet.response_latency_ms / 40) + (energy * 0.9)))
    })
    # Switch the Audio2Face profile to mimic elite academic condescension or aggressive peer scrutiny
    payload_out["nvidia_audio2face_trigger"]["expression_profile"] = "skeptical_brow_raise" if stress_index > 50 else "calculated_neutral"
