#!/usr/bin/env python3
import os
import json
import httpx
import sys

def test_mrg_headless_gateway():
    config_path = os.path.join(os.path.dirname(__file__), "..", "config", "mrg_developer_profile.json")
    
    if not os.path.exists(config_path):
        print(f"❌ Configuration profile not found at: {config_path}")
        sys.exit(1)
        
    with open(config_path, "r") as f:
        config_data = json.load(f)
        
    api_config = config_data.get("mrg_api_configuration", {})
    base_url = api_config.get("base_url", "https://fly.dev")
    secret_key = api_config.get("developer_credentials", {}).get("developer_secret_key")
    
    print(f"📡 Synchronizing pipeline handshake with cluster endpoint: {base_url}...")
    
    # Target endpoint for headless B2B compute token tracking verification
    target_url = f"{base_url}/api/marketplace/consume-api-telemetry"
    
    payload = {
        "developer_secret_key": secret_key,
        "data_packets_processed": 100 # Initial packet test frame
    }
    
    try:
        with httpx.Client(timeout=15.0) as client:
            response = client.post(target_url, json=payload)
            
            if response.status_code == 200:
                print("✅ Handshake Success! 10-Node Mesh Connected.")
                print(json.dumps(response.json(), indent=2))
            elif response.status_code == 402:
                print("❌ Connection Blocked: Insufficient pre-funded API wallet balance.")
                print(response.text)
            else:
                print(f"❌ Handshake Refused: Status Code {response.status_code}")
                print(response.text)
                
    except httpx.RequestError as exc:
        print(f"❌ Network Gateway Error: Unable to establish transport loop. Details: {exc}")

if __name__ == "__main__":
    test_mrg_headless_gateway()
