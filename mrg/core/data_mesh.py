import struct
import datetime

class NasdaqDataMeshAdapter:
    def __init__(self):
        self.message_format = "!Q4sd"

    def serialize_metric_frame(self, metric_id: str, value: float) -> bytes:
        timestamp = int(datetime.datetime.utcnow().timestamp() * 1000)
        safe_id = metric_id[:4].ljust(4).encode('utf-8')
        return struct.pack(self.message_format, timestamp, safe_id, value)

nasdaq_mesh = NasdaqDataMeshAdapter()
