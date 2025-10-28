"""
Database service for PolyWhale bot
"""
import asyncpg
import json
from typing import List, Optional, Dict, Any, Union
from datetime import datetime
from loguru import logger

from config.settings import settings
from bot.models import Trade, Whale, Market, User


class Database:
    """Database service using asyncpg"""

    def __init__(self):
        self.pool: Optional[asyncpg.Pool] = None

    async def connect(self):
        """Create database connection pool"""
        try:
            self.pool = await asyncpg.create_pool(
                settings.DATABASE_URL,
                min_size=2,
                max_size=10,
                command_timeout=60
            )
            logger.info("Database connection pool created")
        except Exception as e:
            logger.error(f"Failed to create database pool: {e}")
            raise

    async def close(self):
        """Close database connection pool"""
        if self.pool:
            await self.pool.close()
            logger.info("Database connection pool closed")

    # User operations
    async def create_user(self, user_id: int, username: Optional[str] = None,
                         first_name: Optional[str] = None) -> None:
        """Create or update user"""
        query = """
            INSERT INTO users (user_id, username, first_name, created_at, last_active)
            VALUES ($1, $2, $3, NOW(), NOW())
            ON CONFLICT (user_id)
            DO UPDATE SET
                username = EXCLUDED.username,
                first_name = EXCLUDED.first_name,
                last_active = NOW()
        """
        async with self.pool.acquire() as conn:
            await conn.execute(query, user_id, username, first_name)

    async def get_user(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        query = "SELECT * FROM users WHERE user_id = $1"
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(query, user_id)
            if row:
                return User(**dict(row))
            return None
    async def update_user_settings(self, user_id: int, **kwargs) -> None:
        """Merge and update settings JSONB for a user"""
        query = """
            UPDATE users
            SET settings = COALESCE(settings, '{}'::jsonb) || $2::jsonb,
                last_active = NOW()
            WHERE user_id = $1
        """
        async with self.pool.acquire() as conn:
            await conn.execute(query, user_id, json.dumps(kwargs))



    # Trade operations
    async def save_trade(self, trade: Trade) -> None:
        """Save a trade to database"""
        query = """
            INSERT INTO trades (id, trader_address, market_id, market_name, side, size, price, timestamp, transaction_hash)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
            ON CONFLICT (id) DO NOTHING
        """
        async with self.pool.acquire() as conn:
            await conn.execute(
                query,
                trade.id,
                trade.trader_address,
                trade.market_id,
                trade.market_name,
                trade.side,
                trade.size,
                trade.price,
                trade.timestamp,
                trade.transaction_hash
            )

    async def get_recent_whale_trades(self, since: datetime, limit: int = 10) -> List[Trade]:
        """Get recent whale trades"""
        query = """
            SELECT * FROM trades
            WHERE timestamp >= $1 AND size >= $2
            ORDER BY timestamp DESC
            LIMIT $3
        """
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(query, since, settings.WHALE_THRESHOLD, limit)
            return [Trade(**dict(row)) for row in rows]

    async def get_largest_whale_trade_since(self, since: datetime, min_size: Optional[Union[int, float]] = None) -> Optional[Trade]:
        """Return the largest whale trade since timestamp (by size)."""
        min_amt = float(min_size) if min_size is not None else float(settings.WHALE_THRESHOLD)
        query = """
            SELECT * FROM trades
            WHERE timestamp >= $1 AND size >= $2
            ORDER BY size DESC, timestamp DESC
            LIMIT 1
        """
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(query, since, min_amt)
            return Trade(**dict(row)) if row else None

    async def get_trader_aggregate(self, address: str) -> Dict[str, Any]:
        """Aggregate lifetime stats for a trader from trades table."""
        query = """
            SELECT COUNT(*) AS total_trades, COALESCE(SUM(size), 0) AS total_volume
            FROM trades
            WHERE trader_address = $1
        """
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(query, address)
            return {
                "total_trades": int(row["total_trades"]) if row else 0,
                "total_volume": float(row["total_volume"]) if row else 0.0,
            }

    async def get_top_whales_since(self, since: datetime, limit: int = 5) -> List[Dict[str, Any]]:
        """Aggregate top whales by total volume since a timestamp"""
        query = """
            SELECT
                trader_address AS address,
                SUM(size) AS total_volume,
                COUNT(*) AS trade_count,
                MAX(size) AS largest_trade
            FROM trades
            WHERE timestamp >= $1 AND size >= $2
            GROUP BY trader_address
            ORDER BY total_volume DESC
            LIMIT $3
        """
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(query, since, settings.WHALE_THRESHOLD, limit)
            results: List[Dict[str, Any]] = []
            for row in rows:
                results.append({
                    "address": row["address"],
                    "total_volume": float(row["total_volume"]) if row["total_volume"] is not None else 0.0,
                    "trade_count": int(row["trade_count"]) if row["trade_count"] is not None else 0,
                    "largest_trade": float(row["largest_trade"]) if row["largest_trade"] is not None else 0.0,
                })
            return results

    async def count_whale_trades_since(self, since: datetime) -> int:
        """Count whale trades (>= threshold) since a timestamp"""
        query = """
            SELECT COUNT(*) AS cnt
            FROM trades
            WHERE timestamp >= $1 AND size >= $2
        """
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(query, since, settings.WHALE_THRESHOLD)
            return int(row["cnt"]) if row and "cnt" in row else 0

    # Whale operations
    async def save_whale(self, whale: Whale) -> None:
        """Save or update whale"""
        query = """
            INSERT INTO whales (address, nickname, total_volume, total_trades, wins, losses, win_rate, last_trade_at, first_seen_at)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
            ON CONFLICT (address)
            DO UPDATE SET
                total_volume = EXCLUDED.total_volume,
                total_trades = EXCLUDED.total_trades,
                wins = EXCLUDED.wins,
                losses = EXCLUDED.losses,
                win_rate = EXCLUDED.win_rate,
                last_trade_at = EXCLUDED.last_trade_at
        """
        async with self.pool.acquire() as conn:
            await conn.execute(
                query,
                whale.address,
                whale.nickname,
                whale.total_volume,
                whale.total_trades,
                whale.wins,
                whale.losses,
                whale.win_rate,
                whale.last_trade_at,
                whale.first_seen_at
            )

    async def get_whale(self, address: str) -> Optional[Whale]:
        """Get whale by address"""
        query = "SELECT * FROM whales WHERE address = $1"
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(query, address)
            if row:
                return Whale(**dict(row))
            return None

    async def get_or_create_whale(self, address: str) -> Whale:
        """Get whale or create if doesn't exist"""
        whale = await self.get_whale(address)
        if not whale:
            whale = Whale(address=address)
            await self.save_whale(whale)
        return whale

    async def get_top_whales(self, limit: int = 10, order_by: str = "win_rate") -> List[Whale]:
        """Get top whales by specified metric"""
        valid_orders = ["win_rate", "total_volume", "total_trades"]
        if order_by not in valid_orders:
            order_by = "win_rate"

        query = f"""
            SELECT * FROM whales
            WHERE total_trades >= 10
            ORDER BY {order_by} DESC
            LIMIT $1
        """
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(query, limit)
            return [Whale(**dict(row)) for row in rows]

    async def update_whale_stats(self, address: str) -> None:
        """Recalculate whale statistics from trades"""
        query = """
            UPDATE whales SET
                total_volume = (SELECT COALESCE(SUM(size), 0) FROM trades WHERE trader_address = $1),
                total_trades = (SELECT COUNT(*) FROM trades WHERE trader_address = $1),
                last_trade_at = (SELECT MAX(timestamp) FROM trades WHERE trader_address = $1)
            WHERE address = $1
        """
        async with self.pool.acquire() as conn:
            await conn.execute(query, address)

    # Market operations
    async def save_market(self, market: Market) -> None:
        """Save or update market"""
        query = """
            INSERT INTO markets (market_id, question, description, category, end_date, volume, liquidity, active)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
            ON CONFLICT (market_id)
            DO UPDATE SET
                question = EXCLUDED.question,
                description = EXCLUDED.description,
                category = EXCLUDED.category,
                end_date = EXCLUDED.end_date,
                volume = EXCLUDED.volume,
                liquidity = EXCLUDED.liquidity,
                active = EXCLUDED.active,
                last_updated = NOW()
        """
        async with self.pool.acquire() as conn:
            await conn.execute(
                query,
                market.market_id,
                market.question,
                market.description,
                market.category,
                market.end_date,
                market.volume,
                market.liquidity,
                market.active
            )

    async def get_top_markets_by_whale_activity(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get top markets by whale activity"""
        query = """
            SELECT
                m.market_id,
                m.question,
                m.category,
                m.end_date,
                COUNT(t.id) as whale_trades_24h,
                COALESCE(SUM(t.size), 0) as whale_volume_24h,
                m.volume as total_volume
            FROM markets m
            LEFT JOIN trades t ON m.market_id = t.market_id
                AND t.timestamp > NOW() - INTERVAL '24 hours'
                AND t.size >= $1
            WHERE m.active = TRUE
            GROUP BY m.market_id, m.question, m.category, m.end_date, m.volume
            ORDER BY whale_volume_24h DESC
            LIMIT $2
        """
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(query, settings.WHALE_THRESHOLD, limit)
            return [dict(row) for row in rows]

    # Tracked whales operations
    async def track_whale(self, user_id: int, whale_address: str) -> None:
        """Add whale to user's tracked list"""
        query = """
            INSERT INTO tracked_whales (user_id, whale_address)
            VALUES ($1, $2)
            ON CONFLICT (user_id, whale_address) DO NOTHING
        """
        async with self.pool.acquire() as conn:
            await conn.execute(query, user_id, whale_address)

    async def untrack_whale(self, user_id: int, whale_address: str) -> None:
        """Remove whale from user's tracked list"""
        query = "DELETE FROM tracked_whales WHERE user_id = $1 AND whale_address = $2"
        async with self.pool.acquire() as conn:
            await conn.execute(query, user_id, whale_address)

    async def get_tracked_whales(self, user_id: int) -> List[Whale]:
        """Get user's tracked whales"""
        query = """
            SELECT w.* FROM whales w
            JOIN tracked_whales tw ON w.address = tw.whale_address
            WHERE tw.user_id = $1
            ORDER BY w.last_trade_at DESC
        """
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(query, user_id)
            return [Whale(**dict(row)) for row in rows]

