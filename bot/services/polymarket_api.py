"""
Polymarket API client
"""
import aiohttp
from typing import List, Dict, Any, Optional
from datetime import datetime
from loguru import logger

from config.settings import settings
from bot.models import Trade, Market


class PolymarketAPI:
    """Client for Polymarket APIs"""
    
    def __init__(self):
        self.data_api_url = settings.POLYMARKET_DATA_API
        self.gamma_api_url = settings.POLYMARKET_GAMMA_API
        self.session: Optional[aiohttp.ClientSession] = None
    
    async def __aenter__(self):
        """Async context manager entry"""
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()
    
    async def get_session(self) -> aiohttp.ClientSession:
        """Get or create session"""
        if not self.session:
            self.session = aiohttp.ClientSession()
        return self.session
    
    async def fetch_recent_trades(self, limit: int = 100) -> List[Trade]:
        """
        Fetch recent trades from Polymarket
        
        Args:
            limit: Maximum number of trades to fetch
            
        Returns:
            List of Trade objects
        """
        url = f"{self.data_api_url}/trades?limit={limit}"
        
        try:
            session = await self.get_session()
            async with session.get(url) as response:
                if response.status != 200:
                    logger.error(f"API error: {response.status}")
                    return []
                
                data = await response.json()
                
                trades = []
                for item in data:
                    try:
                        # Parse timestamp - can be Unix timestamp (int) or ISO string
                        timestamp = item.get("timestamp")
                        if isinstance(timestamp, int):
                            timestamp = datetime.fromtimestamp(timestamp)
                        elif isinstance(timestamp, str):
                            timestamp = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
                        else:
                            timestamp = datetime.now()

                        # Calculate trade size in USD
                        size = float(item.get("size", 0))
                        price = float(item.get("price", 0))
                        trade_value = size * price  # Approximate USD value

                        trade = Trade(
                            id=item.get("transactionHash", item.get("transaction_hash", "")),
                            trader_address=item.get("proxyWallet", item.get("trader_address", "")),
                            trader_name=item.get("name", ""),
                            trader_pseudonym=item.get("pseudonym", ""),
                            market_id=item.get("conditionId", item.get("asset", "")),
                            market_name=item.get("title", item.get("market", "Unknown Market")),
                            market_slug=item.get("slug", ""),
                            event_slug=item.get("eventSlug", ""),
                            outcome=item.get("outcome", ""),
                            side=item.get("side", "BUY"),
                            size=trade_value,  # Use calculated USD value
                            price=price,
                            timestamp=timestamp,
                            transaction_hash=item.get("transactionHash", item.get("transaction_hash", ""))
                        )
                        trades.append(trade)
                    except Exception as e:
                        logger.warning(f"Failed to parse trade: {e}")
                        continue
                
                logger.info(f"Fetched {len(trades)} trades from Polymarket")
                return trades
                
        except Exception as e:
            logger.error(f"Error fetching trades: {e}")
            return []
    
    async def fetch_markets(self, limit: int = 50, active: bool = True) -> List[Market]:
        """
        Fetch markets from Polymarket
        
        Args:
            limit: Maximum number of markets to fetch
            active: Only fetch active markets
            
        Returns:
            List of Market objects
        """
        closed = "false" if active else "true"
        url = f"{self.gamma_api_url}/markets?limit={limit}&closed={closed}"
        
        try:
            session = await self.get_session()
            async with session.get(url) as response:
                if response.status != 200:
                    logger.error(f"API error: {response.status}")
                    return []
                
                data = await response.json()
                
                markets = []
                for item in data:
                    try:
                        # Parse end date
                        end_date = None
                        if item.get("end_date_iso"):
                            end_date = datetime.fromisoformat(item["end_date_iso"].replace("Z", "+00:00"))
                        
                        market = Market(
                            market_id=item.get("id", item.get("condition_id", "")),
                            question=item.get("question", "Unknown Question"),
                            description=item.get("description", ""),
                            category=item.get("category", "Other"),
                            end_date=end_date,
                            volume=float(item.get("volume", 0)),
                            liquidity=float(item.get("liquidity", 0)),
                            active=item.get("active", True)
                        )
                        markets.append(market)
                    except Exception as e:
                        logger.warning(f"Failed to parse market: {e}")
                        continue
                
                logger.info(f"Fetched {len(markets)} markets from Polymarket")
                return markets
                
        except Exception as e:
            logger.error(f"Error fetching markets: {e}")
            return []
    
    async def fetch_whale_positions(self, address: str) -> List[Dict[str, Any]]:
        """
        Fetch positions for a specific whale
        
        Args:
            address: Ethereum address
            
        Returns:
            List of positions
        """
        url = f"{self.data_api_url}/positions?user={address}"
        
        try:
            session = await self.get_session()
            async with session.get(url) as response:
                if response.status != 200:
                    logger.error(f"API error: {response.status}")
                    return []
                
                data = await response.json()
                logger.info(f"Fetched {len(data)} positions for whale {address}")
                return data
                
        except Exception as e:
            logger.error(f"Error fetching whale positions: {e}")
            return []
    
    async def fetch_market_holders(self, market_id: str) -> List[Dict[str, Any]]:
        """
        Fetch top holders for a market
        
        Args:
            market_id: Market identifier
            
        Returns:
            List of holders
        """
        url = f"{self.data_api_url}/holders?id={market_id}"
        
        try:
            session = await self.get_session()
            async with session.get(url) as response:
                if response.status != 200:
                    logger.error(f"API error: {response.status}")
                    return []
                
                data = await response.json()
                logger.info(f"Fetched {len(data)} holders for market {market_id}")
                return data
                
        except Exception as e:
            logger.error(f"Error fetching market holders: {e}")
            return []
    
    async def close(self):
        """Close the session"""
        if self.session:
            await self.session.close()
            self.session = None

