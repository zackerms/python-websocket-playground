import asyncio
import websockets
from websockets.exceptions import ConnectionClosedError
import argparse
import time

async def connect_websocket(index, url, duration, delay):
    await asyncio.sleep(delay)
    try:
        async with websockets.connect(url) as websocket:
            await websocket.ping()
            await asyncio.sleep(duration)
    except ConnectionClosedError as e:
        print(f"Connection {index} closed unexpectedly: {e}")

async def run_benchmark(url, num_connections, duration, delay):
    tasks = [connect_websocket(i, url, duration, delay*i) for i in range(num_connections)]
    start_time = time.time()
    await asyncio.gather(*tasks)
    end_time = time.time()
    return end_time - start_time

# /ws/benchmark に対して、指定された数のWebSocket接続を確立する
# python3 benchmark.py --n 1000
def main():
    parser = argparse.ArgumentParser(description="WebSocket Benchmark")
    parser.add_argument("--n", type=int, default=5, help="Number of WebSocket connections")
    parser.add_argument("--url", type=str, default="ws://localhost:8000/ws/benchmark", help="WebSocket URL")
    parser.add_argument("--duration", type=float, default=5, help="Duration to keep each connection open (in seconds)")
    parser.add_argument("--delay", type=float, default=0, help="Delay between each connection (in seconds)")
    args = parser.parse_args()

    print(f"Establishing {args.n} WebSocket connections to {args.url}")
    
    total_time = asyncio.run(run_benchmark(args.url, args.n, args.duration, args.delay))
    
    print(f"Benchmark completed in {total_time:.2f} seconds")
    print(f"Average time per connection: {(total_time / args.n) * 1000:.2f} ms")


if __name__ == "__main__":
    main()