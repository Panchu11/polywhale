"""Test live Polymarket API to see actual response format"""
import asyncio
import aiohttp
import json

async def test_polymarket():
    print("Testing Polymarket API...")
    
    # Test trades endpoint
    async with aiohttp.ClientSession() as session:
        print("\n=== TESTING TRADES ENDPOINT ===")
        url = "https://data-api.polymarket.com/trades?limit=5"
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                print(f"Got {len(data)} trades")
                if data:
                    print("\nFirst trade structure:")
                    print(json.dumps(data[0], indent=2))
            else:
                print(f"Error: {response.status}")
        
        print("\n=== TESTING MARKETS ENDPOINT ===")
        url = "https://gamma-api.polymarket.com/markets?limit=3&closed=false"
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                print(f"Got {len(data)} markets")
                if data:
                    print("\nFirst market structure:")
                    print(json.dumps(data[0], indent=2))
            else:
                print(f"Error: {response.status}")

if __name__ == "__main__":
    asyncio.run(test_polymarket())

