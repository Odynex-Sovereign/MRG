import struct
import datetime
from typing import Dict, Any

class NasdaqDataMeshAdapter:
    """
    Implements a structural variant of the high-frequency NASDAQ ITCH/OUCH streaming 
    protocol layer to serialize simulation updates into ultra-low footprint byte streams.
    """
    def __init__(self):
        # Format specifier: ! (Network/Big-Endian), Q (Timestamp), 4s (Stock/Grid Identifier), d (Value)
        self.message_format = "!Q4sd"

    def serialize_metric_frame(self, metric_id: str, value: float) -> bytes:
        """Encodes telemetry points into compact, immutable binary frames for direct network transport."""
        timestamp = int(datetime.datetime.utcnow().timestamp() * 1000)
        # Ensure identifier conforms strictly to 4-character ticker frames
        safe_id = metric_id[:4].ljust(4).encode('utf-8')
        return struct.pack(self.message_format, timestamp, safe_id, value)

    def deserialize_metric_frame(self, frame_bytes: bytes) -> Dict[str, Any]:
        """Parses incoming high-frequency financial simulation updates."""
        try:
            timestamp, raw_id, value = struct.unpack(self.message_format, frame_bytes)
            return {
                "timestamp": timestamp,
                "metric_id": raw_id.decode('utf-8').strip(),
                "value": round(value, 4)
            }
        except struct.error:
            return {"error": "Malformed protocol data frame transmission Intercepted."}

nasdaq_mesh = NasdaqDataMeshAdapter()
