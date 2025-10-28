"""
Test Polymarket API connectivity
"""
import asyncio
import sys
from pathlib import Path
from loguru import logger

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from bot.services.polymarket_api import PolymarketAPI


async def test_api():
    """Test Polymarket API"""
    logger.info("Testing Polymarket API...")
    
    api = PolymarketAPI()
    
    try:
        # Test fetching trades
        logger.info("Fetching recent trades...")
        trades = await api.fetch_recent_trades(limit=5)
        
        if trades:
            logger.info(f"✓ Fetched {len(trades)} trades")
            for i, trade in enumerate(trades[:3], 1):
                logger.info(f"  {i}. {trade.whale_emoji} ${trade.size:,.0f} - {trade.market_name[:50]}")
        else:
            logger.warning("⚠ No trades fetched")
        
        # Test fetching markets
        logger.info("\nFetching markets...")
        markets = await api.fetch_markets(limit=5)
        
        if markets:
            logger.info(f"✓ Fetched {len(markets)} markets")
            for i, market in enumerate(markets[:3], 1):
                logger.info(f"  {i}. {market.question[:60]}")
        else:
            logger.warning("⚠ No markets fetched")
        
        logger.info("\n✓ API test complete!")
        
    except Exception as e:
        logger.error(f"✗ API test failed: {e}")
        sys.exit(1)
    finally:
        await api.close()


if __name__ == "__main__":
    asyncio.run(test_api())

