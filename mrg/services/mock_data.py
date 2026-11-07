import asyncio
import random
from mrg.core.data_mesh import nasdaq_mesh
from mrg.core.twin_bridge import siemens_bridge

LATEST_NASDAQ_MARKET_STREAM: bytes = b""
LATEST_SIEMENS_TWIN_NODE: str = "{}"

async def generate_continuous_validation_metrics():
    global LATEST_NASDAQ_MARKET_STREAM, LATEST_SIEMENS_TWIN_NODE
    while True:
        oil_price = random.uniform(80.0, 85.0)
        stability = random.uniform(94.0, 99.0)
        LATEST_NASDAQ_MARKET_STREAM = nasdaq_mesh.serialize_metric_frame("OILB", oil_price)
        LATEST_SIEMENS_TWIN_NODE = siemens_bridge.compile_opc_ua_node_payload("PLANT_01", {"grid_stability_index": stability})
        await asyncio.sleep(0.5)
