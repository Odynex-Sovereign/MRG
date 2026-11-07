import json
import uuid
import datetime

class SiemensTwinBridgeManager:
    def compile_opc_ua_node_payload(self, asset_id: str, telemetry_matrix: dict) -> str:
        return json.dumps({
            "MessageId": str(uuid.uuid4()),
            "Timestamp": datetime.datetime.utcnow().isoformat() + "Z",
            "Payload": {
                f"Node_{asset_id}_GridStability": {"Value": telemetry_matrix.get("grid_stability_index", 100.0)}
            }
        })

siemens_bridge = SiemensTwinBridgeManager()
