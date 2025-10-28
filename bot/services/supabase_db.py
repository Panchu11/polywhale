"""
Supabase Database Service
Works with Supabase REST API (IPv4 compatible - Free Plan)
"""
import os
from typing import List, Optional, Dict, Any
from datetime import datetime
from loguru import logger
from supabase import create_client, Client

from config.settings import settings


class SupabaseDatabase:
    """Database service using Supabase REST API"""
    
    def __init__(self):
        self.client: Optional[Client] = None
        self.supabase_url = os.getenv("SUPABASE_URL")
        self.supabase_key = os.getenv("SUPABASE_KEY")
    
    async def connect(self):
        """Connect to Supabase"""
        try:
            self.client = create_client(self.supabase_url, self.supabase_key)
            logger.info("Connected to Supabase")
        except Exception as e:
            logger.error(f"Failed to connect to Supabase: {e}")
            raise
    
    async def close(self):
        """Close connection (not needed for REST API but kept for compatibility)"""
        logger.info("Supabase connection closed")
    
    # User operations
    async def create_user(self, telegram_id: int, username: str = None, first_name: str = None) -> Dict[str, Any]:
        """Create or update a user"""
        try:
            user_data = {
                "user_id": telegram_id,  # Changed from telegram_id to user_id
                "username": username,
                "first_name": first_name,
                "created_at": datetime.utcnow().isoformat()
            }

            # Upsert user (insert or update if exists)
            result = self.client.table("users").upsert(
                user_data,
                on_conflict="user_id"  # Changed from telegram_id to user_id
            ).execute()
            
            logger.info(f"User created/updated: {telegram_id}")
            return result.data[0] if result.data else user_data
        except Exception as e:
            logger.error(f"Failed to create user: {e}")
            raise
    
    async def get_user(self, telegram_id: int) -> Optional[Dict[str, Any]]:
        """Get user by telegram ID"""
        try:
            result = self.client.table("users").select("*").eq("user_id", telegram_id).execute()  # Changed to user_id
            return result.data[0] if result.data else None
        except Exception as e:
            logger.error(f"Failed to get user: {e}")
            return None
    
    # Trade operations
    async def save_trade(self, trade_data: Dict[str, Any]) -> Dict[str, Any]:
        """Save a trade to database"""
        try:
            # Convert datetime to ISO string if present
            if "timestamp" in trade_data and isinstance(trade_data["timestamp"], datetime):
                trade_data["timestamp"] = trade_data["timestamp"].isoformat()

            # Rename 'trade_id' to 'id' if present (to match schema)
            if "trade_id" in trade_data:
                trade_data["id"] = trade_data.pop("trade_id")

            result = self.client.table("trades").insert(trade_data).execute()
            logger.debug(f"Trade saved: {trade_data.get('id')}")
            return result.data[0] if result.data else trade_data
        except Exception as e:
            logger.error(f"Failed to save trade: {e}")
            raise
    
    async def get_recent_whale_trades(self, since=None, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent whale trades"""
        try:
            query = self.client.table("trades")\
                .select("*")\
                .gte("size", settings.WHALE_THRESHOLD)  # Changed from amount_usd to size

            # Add time filter if provided
            if since:
                query = query.gte("timestamp", since.isoformat())

            result = query.order("timestamp", desc=True)\
                .limit(limit)\
                .execute()

            return result.data if result.data else []
        except Exception as e:
            logger.error(f"Failed to get recent whale trades: {e}")
            return []
    
    # Market operations
    async def save_market(self, market_data: Dict[str, Any]) -> Dict[str, Any]:
        """Save or update a market"""
        try:
            result = self.client.table("markets").upsert(
                market_data,
                on_conflict="market_id"
            ).execute()
            
            logger.debug(f"Market saved: {market_data.get('market_id')}")
            return result.data[0] if result.data else market_data
        except Exception as e:
            logger.error(f"Failed to save market: {e}")
            raise
    
    async def get_active_markets(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get active markets"""
        try:
            result = self.client.table("markets")\
                .select("*")\
                .eq("active", True)\
                .order("volume_usd", desc=True)\
                .limit(limit)\
                .execute()
            
            return result.data if result.data else []
        except Exception as e:
            logger.error(f"Failed to get active markets: {e}")
            return []
    
    # Whale operations
    async def save_whale(self, whale_data: Dict[str, Any]) -> Dict[str, Any]:
        """Save or update a whale"""
        try:
            result = self.client.table("whales").upsert(
                whale_data,
                on_conflict="address"
            ).execute()
            
            logger.debug(f"Whale saved: {whale_data.get('address')}")
            return result.data[0] if result.data else whale_data
        except Exception as e:
            logger.error(f"Failed to save whale: {e}")
            raise
    
    async def get_top_whales(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get top whales by total volume"""
        try:
            result = self.client.table("whales")\
                .select("*")\
                .order("total_volume_usd", desc=True)\
                .limit(limit)\
                .execute()
            
            return result.data if result.data else []
        except Exception as e:
            logger.error(f"Failed to get top whales: {e}")
            return []
    
    async def get_whale_by_address(self, address: str) -> Optional[Dict[str, Any]]:
        """Get whale by address"""
        try:
            result = self.client.table("whales").select("*").eq("address", address).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            logger.error(f"Failed to get whale: {e}")
            return None
    
    # Alert operations
    async def create_alert(self, user_id: int, alert_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create an alert for a user"""
        try:
            alert_data["user_id"] = user_id
            alert_data["created_at"] = datetime.utcnow().isoformat()
            
            result = self.client.table("alerts").insert(alert_data).execute()
            logger.info(f"Alert created for user {user_id}")
            return result.data[0] if result.data else alert_data
        except Exception as e:
            logger.error(f"Failed to create alert: {e}")
            raise
    
    async def get_user_alerts(self, user_id: int) -> List[Dict[str, Any]]:
        """Get all alerts for a user"""
        try:
            result = self.client.table("alerts")\
                .select("*")\
                .eq("user_id", user_id)\
                .eq("active", True)\
                .execute()
            
            return result.data if result.data else []
        except Exception as e:
            logger.error(f"Failed to get user alerts: {e}")
            return []
    
    # Tracked whales operations
    async def track_whale(self, user_id: int, whale_address: str) -> Dict[str, Any]:
        """Track a whale for a user"""
        try:
            track_data = {
                "user_id": user_id,
                "whale_address": whale_address,
                "created_at": datetime.utcnow().isoformat()
            }
            
            result = self.client.table("tracked_whales").insert(track_data).execute()
            logger.info(f"User {user_id} now tracking whale {whale_address}")
            return result.data[0] if result.data else track_data
        except Exception as e:
            logger.error(f"Failed to track whale: {e}")
            raise
    
    async def get_tracked_whales(self, user_id: int) -> List[str]:
        """Get all whales tracked by a user"""
        try:
            result = self.client.table("tracked_whales")\
                .select("whale_address")\
                .eq("user_id", user_id)\
                .execute()

            return [row["whale_address"] for row in result.data] if result.data else []
        except Exception as e:
            logger.error(f"Failed to get tracked whales: {e}")
            return []

    async def untrack_whale(self, user_id: int, whale_address: str) -> bool:
        """Stop tracking a whale"""
        try:
            result = self.client.table("tracked_whales")\
                .delete()\
                .eq("user_id", user_id)\
                .eq("whale_address", whale_address)\
                .execute()

            logger.info(f"User {user_id} stopped tracking whale {whale_address}")
            return True
        except Exception as e:
            logger.error(f"Failed to untrack whale: {e}")
            return False

    async def get_user(self, telegram_id: int) -> Optional[Dict[str, Any]]:
        """Get user by telegram ID"""
        try:
            result = self.client.table("users")\
                .select("*")\
                .eq("telegram_id", telegram_id)\
                .execute()

            return result.data[0] if result.data else None
        except Exception as e:
            logger.error(f"Failed to get user: {e}")
            return None

    async def update_user_settings(self, telegram_id: int, **kwargs) -> bool:
        """Update user settings"""
        try:
            # First ensure user exists
            user = await self.get_user(telegram_id)
            if not user:
                # Create user if doesn't exist
                await self.create_user(telegram_id)
                user = await self.get_user(telegram_id)
                if not user:
                    return False

            # Get current settings
            current_settings = user.get('settings', {})

            # Merge new settings with existing
            updated_settings = {**current_settings, **kwargs}

            # Update settings JSONB column
            result = self.client.table("users")\
                .update({"settings": updated_settings})\
                .eq("user_id", telegram_id)\
                .execute()

            logger.info(f"Updated settings for user {telegram_id}: {kwargs}")
            return True
        except Exception as e:
            logger.error(f"Failed to update user settings: {e}")
            return False
    
    # Notification operations
    async def save_notification(self, notification_data: Dict[str, Any]) -> Dict[str, Any]:
        """Save a sent notification"""
        try:
            notification_data["sent_at"] = datetime.utcnow().isoformat()
            
            result = self.client.table("notifications").insert(notification_data).execute()
            logger.debug(f"Notification saved")
            return result.data[0] if result.data else notification_data
        except Exception as e:
            logger.error(f"Failed to save notification: {e}")
            raise
    
    # Stats operations
    async def get_stats(self) -> Dict[str, Any]:
        """Get overall statistics"""
        try:
            # Get counts from different tables
            users_count = len(self.client.table("users").select("id", count="exact").execute().data)
            whales_count = len(self.client.table("whales").select("id", count="exact").execute().data)
            trades_count = len(self.client.table("trades").select("id", count="exact").execute().data)
            
            return {
                "total_users": users_count,
                "total_whales": whales_count,
                "total_trades": trades_count
            }
        except Exception as e:
            logger.error(f"Failed to get stats: {e}")
            return {
                "total_users": 0,
                "total_whales": 0,
                "total_trades": 0
            }

