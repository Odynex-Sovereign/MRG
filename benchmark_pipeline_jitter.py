import asyncio
import time
import json
import numpy as np
import websockets

async def run_latency_benchmark(runs: int = 50):
    """Benchmarks processing overhead and network jitter for the sub-100ms pipeline."""
    uri = "ws://localhost:8000/ws/simulation"
    latencies = []
    
    print(f"Starting High-Frequency Network Benchmark against {uri} ({runs} samples)...")
    
    try:
        async with websockets.connect(uri) as websocket:
            for i in range(runs):
                packet = {
                    "user_id": "benchmark_node",
                    "session_id": "test_session",
                    "vertical": "Asset-Defense",
                    "vocal_pitch_variance": float(np.random.uniform(5.0, 30.0)),
                    "vocal_energy": float(np.random.uniform(40.0, 95.0)),
                    "response_latency_ms": 45,
                    "user_raw_text": f"Telemetry benchmark sample matrix generation ID: {i}"
                }
                
                start_time = time.perf_counter()
                await websocket.send(json.dumps(packet))
                await websocket.recv()
                end_time = time.perf_counter()
                
                # Convert performance delta into milliseconds
                round_trip_ms = (end_time - start_time) * 1000
                latencies.append(round_trip_ms)
                await asyncio.sleep(0.02) # Simulate human audio frame interval pacing
                
        # Statistical Array Operations
        lat_arr = np.array(latencies)
        p99 = np.percentile(lat_arr, 99)
        p95 = np.percentile(lat_arr, 95)
        mean_lat = np.mean(lat_arr)
        jitter = np.std(lat_arr) # Jitter represented as standard deviation of execution latency
        
        print("\n📊 PIPELINE BENCHMARK RESULTS:")
        print(f"  • Total Packets Transmitted : {runs}")
        print(f"  • Mean Round-Trip Latency   : {mean_lat:.2f} ms")
        print(f"  • 95th Percentile (p95)     : {p95:.2f} ms")
        print(f"  • 99th Percentile (p99)     : {p99:.2f} ms")
        print(f"  • Network Pipeline Jitter   : {jitter:.2f} ms")
        
        if p99 < 100.0:
            print("\n✅ SYSTEM STATUS: CONFORMS TO SOVEREIGN REAL-TIME SPECIFICATION (<100ms Target Window)")
        else:
            print("\n⚠️ SYSTEM STATUS: NETWORK DRIFT DETECTED IN OUTLIERS")
            
    except Exception as e:
        print(f"Benchmark run aborted due to connectivity failure: {e}")

if __name__ == "__main__":
    asyncio.run(run_latency_benchmark(
    ))
