"""Debug whale trade detection"""
import asyncio
import sys
sys.path.insert(0, '.')

from bot.services.polymarket_api import PolymarketAPI

async def main():
    api = PolymarketAPI()
    
    print("Fetching 500 recent trades from Polymarket...")
    trades = await api.fetch_recent_trades(limit=500)
    
    print(f"\nTotal trades fetched: {len(trades)}")
    
    # Analyze trade sizes
    sizes = [t.size for t in trades]
    sizes.sort(reverse=True)
    
    print(f"\nTop 20 trade sizes:")
    for i, size in enumerate(sizes[:20], 1):
        print(f"{i}. ${size:,.2f}")
    
    print(f"\nTrades above $10,000:")
    whale_trades = [t for t in trades if t.size >= 10000]
    print(f"Count: {len(whale_trades)}")
    
    if whale_trades:
        print("\nTop 5 whale trades:")
        for i, trade in enumerate(whale_trades[:5], 1):
            print(f"\n{i}. ${trade.size:,.2f}")
            print(f"   Market: {trade.market_name}")
            print(f"   Trader: {trade.trader_address[:10]}...")
            print(f"   Side: {trade.side}")
            print(f"   Time: {trade.timestamp}")
    
    print(f"\nTrades above $5,000:")
    medium_trades = [t for t in trades if t.size >= 5000]
    print(f"Count: {len(medium_trades)}")
    
    print(f"\nTrades above $1,000:")
    small_trades = [t for t in trades if t.size >= 1000]
    print(f"Count: {len(small_trades)}")
    
    # Show sample trade data
    if trades:
        print(f"\n\nSample trade (first one):")
        t = trades[0]
        print(f"ID: {t.id}")
        print(f"Trader: {t.trader_address}")
        print(f"Market: {t.market_name}")
        print(f"Side: {t.side}")
        print(f"Size: ${t.size:,.2f}")
        print(f"Price: {t.price}")
        print(f"Timestamp: {t.timestamp}")
    
    await api.close()

if __name__ == "__main__":
    asyncio.run(main())

