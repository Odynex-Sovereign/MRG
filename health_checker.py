import httpx
import asyncio
import sys

async def check_local_health():
    print("Checking local MRG engine stack binding loop...")
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get("http://127.0.0", timeout=5.0)
            if response.status_code == 200:
                print("SUCCESS: Engine is listening locally on port 8000!")
                sys.exit(0)
            else:
                print(f"WARNING: Got unexpected status code {response.status_code}")
                sys.exit(1)
        except httpx.RequestError as e:
            print(f"ERROR: Cannot communicate with the server engine. Details: {e}")
            sys.exit(1)

if __name__ == "__main__":
    asyncio.run(check_local_health())
