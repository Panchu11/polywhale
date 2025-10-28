"""
Whale tracker service - monitors and detects whale trades
"""
import asyncio
from typing import List, Set
from datetime import datetime, timedelta
from loguru import logger

from config.settings import settings
from bot.models import Trade, Whale
from bot.services.database import Database
from bot.services.polymarket_api import PolymarketAPI


class WhaleTracker:
    """Service to track whale trades"""
    
    def __init__(self, db: Database):
        self.db = db
        self.api = PolymarketAPI()
        self.seen_trade_ids: Set[str] = set()
        self.is_running = False
    
    async def start(self):
        """Start whale tracking loop"""
        self.is_running = True
        logger.info("Whale tracker started")
        
        while self.is_running:
            try:
                await self.check_for_whale_trades()
                await asyncio.sleep(settings.POLL_INTERVAL)
            except Exception as e:
                logger.error(f"Error in whale tracker loop: {e}")
                await asyncio.sleep(settings.POLL_INTERVAL)
    
    async def stop(self):
        """Stop whale tracking loop"""
        self.is_running = False
        await self.api.close()
        logger.info("Whale tracker stopped")
    
    async def check_for_whale_trades(self):
        """Check for new whale trades"""
        try:
            # Fetch recent trades
            trades = await self.api.fetch_recent_trades(limit=100)
            
            new_whale_trades = []
            
            for trade in trades:
                # Skip if already seen
                if trade.id in self.seen_trade_ids:
                    continue
                
                # Check if it's a whale trade
                if trade.is_whale_trade:
                    new_whale_trades.append(trade)
                    self.seen_trade_ids.add(trade.id)
                    
                    # Save trade to database
                    await self.db.save_trade(trade)
                    
                    # Update whale stats
                    await self.update_whale_stats(trade.trader_address)
            
            if new_whale_trades:
                logger.info(f"Detected {len(new_whale_trades)} new whale trades")
                
                # TODO: Send alerts to users
                # await self.send_whale_alerts(new_whale_trades)
            
            # Clean up old trade IDs (keep last 1000)
            if len(self.seen_trade_ids) > 1000:
                self.seen_trade_ids = set(list(self.seen_trade_ids)[-1000:])
            
        except Exception as e:
            logger.error(f"Error checking for whale trades: {e}")
    
    async def update_whale_stats(self, address: str):
        """Update statistics for a whale"""
        try:
            # Get or create whale
            whale = await self.db.get_or_create_whale(address)
            
            # Update stats from database
            await self.db.update_whale_stats(address)
            
            # Recalculate win rate (simplified - would need market outcomes)
            # For now, we'll just update the stats
            
            logger.debug(f"Updated stats for whale {whale.short_address}")
            
        except Exception as e:
            logger.error(f"Error updating whale stats: {e}")
    
    async def get_whale_trades(self, address: str, limit: int = 10) -> List[Trade]:
        """Get recent trades for a specific whale"""
        query = """
            SELECT * FROM trades 
            WHERE trader_address = $1
            ORDER BY timestamp DESC
            LIMIT $2
        """
        async with self.db.pool.acquire() as conn:
            rows = await conn.fetch(query, address, limit)
            return [Trade(**dict(row)) for row in rows]
    
    async def get_whale_consensus(self, market_id: str) -> dict:
        """
        Get whale consensus for a market
        Returns percentage of whales betting YES vs NO
        """
        query = """
            SELECT 
                side,
                COUNT(DISTINCT trader_address) as whale_count,
                SUM(size) as total_volume
            FROM trades
            WHERE market_id = $1 
                AND size >= $2
                AND timestamp > NOW() - INTERVAL '7 days'
            GROUP BY side
        """
        async with self.db.pool.acquire() as conn:
            rows = await conn.fetch(query, market_id, settings.WHALE_THRESHOLD)
            
            consensus = {
                "YES": {"count": 0, "volume": 0},
                "NO": {"count": 0, "volume": 0}
            }
            
            for row in rows:
                side = row["side"]
                if side in consensus:
                    consensus[side]["count"] = row["whale_count"]
                    consensus[side]["volume"] = float(row["total_volume"])
            
            # Calculate percentages
            total_count = consensus["YES"]["count"] + consensus["NO"]["count"]
            total_volume = consensus["YES"]["volume"] + consensus["NO"]["volume"]
            
            if total_count > 0:
                consensus["YES"]["percentage"] = (consensus["YES"]["count"] / total_count) * 100
                consensus["NO"]["percentage"] = (consensus["NO"]["count"] / total_count) * 100
            else:
                consensus["YES"]["percentage"] = 0
                consensus["NO"]["percentage"] = 0
            
            return consensus
    
    async def get_smart_money_flow(self, hours: int = 24) -> dict:
        """
        Get smart money flow (net buying/selling by whales)
        """
        query = """
            SELECT 
                market_id,
                market_name,
                side,
                SUM(size) as volume
            FROM trades
            WHERE timestamp > NOW() - INTERVAL '1 hour' * $1
                AND size >= $2
            GROUP BY market_id, market_name, side
            ORDER BY volume DESC
            LIMIT 20
        """
        async with self.db.pool.acquire() as conn:
            rows = await conn.fetch(query, hours, settings.WHALE_THRESHOLD)
            
            # Group by market and calculate net flow
            markets = {}
            for row in rows:
                market_id = row["market_id"]
                if market_id not in markets:
                    markets[market_id] = {
                        "market_name": row["market_name"],
                        "YES": 0,
                        "NO": 0
                    }
                
                side = row["side"]
                if side in ["YES", "BUY"]:
                    markets[market_id]["YES"] += float(row["volume"])
                elif side in ["NO", "SELL"]:
                    markets[market_id]["NO"] += float(row["volume"])
            
            # Calculate net flow
            flow = []
            for market_id, data in markets.items():
                net_flow = data["YES"] - data["NO"]
                flow.append({
                    "market_id": market_id,
                    "market_name": data["market_name"],
                    "net_flow": net_flow,
                    "yes_volume": data["YES"],
                    "no_volume": data["NO"]
                })
            
            # Sort by absolute net flow
            flow.sort(key=lambda x: abs(x["net_flow"]), reverse=True)
            
            return {
                "buying": [f for f in flow if f["net_flow"] > 0][:5],
                "selling": [f for f in flow if f["net_flow"] < 0][:5]
            }
    
    def is_whale_trade(self, trade: Trade) -> bool:
        """Check if a trade qualifies as a whale trade"""
        return trade.size >= settings.WHALE_THRESHOLD
    
    def get_whale_tier(self, size: float) -> int:
        """Get whale tier based on trade size"""
        if size >= settings.WHALE_TIER_3:
            return 3  # Large whale
        elif size >= settings.WHALE_TIER_2:
            return 2  # Medium whale
        elif size >= settings.WHALE_TIER_1:
            return 1  # Small whale
        return 0  # Not a whale

