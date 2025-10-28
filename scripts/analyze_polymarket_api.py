"""Deep analysis of Polymarket API responses"""
import asyncio
import aiohttp
import json
from datetime import datetime

async def analyze_trades_api():
    """Analyze the actual trades API response"""
    print("=" * 80)
    print("ANALYZING POLYMARKET TRADES API")
    print("=" * 80)
    
    async with aiohttp.ClientSession() as session:
        url = "https://data-api.polymarket.com/trades?limit=10"
        
        async with session.get(url) as response:
            data = await response.json()
            
            print(f"\nResponse type: {type(data)}")
            print(f"Number of trades: {len(data) if isinstance(data, list) else 'N/A'}")
            
            if isinstance(data, list) and len(data) > 0:
                print("\n" + "=" * 80)
                print("FIRST TRADE - COMPLETE RAW DATA:")
                print("=" * 80)
                print(json.dumps(data[0], indent=2))
                
                print("\n" + "=" * 80)
                print("ALL AVAILABLE FIELDS IN FIRST TRADE:")
                print("=" * 80)
                for key, value in data[0].items():
                    print(f"{key:25} = {value} (type: {type(value).__name__})")
                
                # Analyze all trades for size distribution
                print("\n" + "=" * 80)
                print("TRADE SIZE ANALYSIS:")
                print("=" * 80)
                
                for i, trade in enumerate(data[:10], 1):
                    size = float(trade.get('size', 0))
                    price = float(trade.get('price', 0))
                    value = size * price
                    
                    print(f"\nTrade {i}:")
                    print(f"  Size: {size}")
                    print(f"  Price: {price}")
                    print(f"  Calculated Value: ${value:,.2f}")
                    print(f"  Side: {trade.get('side')}")
                    print(f"  Asset: {trade.get('asset', 'N/A')}")
                    print(f"  Market: {trade.get('market', trade.get('title', 'N/A'))[:60]}")
                    print(f"  Trader: {trade.get('trader', trade.get('proxyWallet', 'N/A'))}")

async def analyze_markets_api():
    """Analyze the markets API response"""
    print("\n\n" + "=" * 80)
    print("ANALYZING POLYMARKET MARKETS API")
    print("=" * 80)
    
    async with aiohttp.ClientSession() as session:
        url = "https://gamma-api.polymarket.com/markets?limit=5&closed=false"
        
        async with session.get(url, headers={"Accept": "application/json"}) as response:
            data = await response.json()
            
            print(f"\nResponse type: {type(data)}")
            
            if isinstance(data, list) and len(data) > 0:
                print("\n" + "=" * 80)
                print("FIRST MARKET - COMPLETE RAW DATA:")
                print("=" * 80)
                print(json.dumps(data[0], indent=2))
                
                print("\n" + "=" * 80)
                print("ALL AVAILABLE FIELDS IN FIRST MARKET:")
                print("=" * 80)
                for key, value in data[0].items():
                    if isinstance(value, (dict, list)):
                        print(f"{key:25} = {type(value).__name__} with {len(value)} items")
                    else:
                        print(f"{key:25} = {value} (type: {type(value).__name__})")

async def check_clob_api():
    """Check CLOB API for more detailed trade data"""
    print("\n\n" + "=" * 80)
    print("ANALYZING POLYMARKET CLOB API")
    print("=" * 80)
    
    async with aiohttp.ClientSession() as session:
        url = "https://clob.polymarket.com/trades?limit=10"
        
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"\nCLOB API Response type: {type(data)}")
                    
                    if isinstance(data, list) and len(data) > 0:
                        print("\nFirst CLOB trade:")
                        print(json.dumps(data[0], indent=2))
                else:
                    print(f"\nCLOB API returned status: {response.status}")
        except Exception as e:
            print(f"\nCLOB API error: {e}")

async def main():
    await analyze_trades_api()
    await analyze_markets_api()
    await check_clob_api()
    
    print("\n\n" + "=" * 80)
    print("ANALYSIS COMPLETE")
    print("=" * 80)

if __name__ == "__main__":
    asyncio.run(main())

