"""
Preview the /top leaderboard directly from the DB for 24h / 7d / 30d.
"""
import os
import sys
import asyncio
from datetime import datetime, timedelta

# Ensure project root on path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from bot.services.database import Database
from config.settings import settings

async def main():
    db = Database()
    await db.connect()
    now = datetime.utcnow()
    for label, delta in [("24h", timedelta(hours=24)), ("7d", timedelta(days=7)), ("30d", timedelta(days=30))]:
        since = now - delta
        rows = await db.get_top_whales_since(since, limit=5)
        count = await db.count_whale_trades_since(since)
        print(f"\n=== {label} ===")
        print(f"whale trades: {count}")
        for i, r in enumerate(rows, 1):
            print(f"{i}. {r['address']} - ${r['total_volume']:.2f} ({r['trade_count']} trades; max ${r['largest_trade']:.2f})")
    await db.close()

if __name__ == "__main__":
    asyncio.run(main())

