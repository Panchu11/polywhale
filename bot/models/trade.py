"""
Trade model
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class Trade(BaseModel):
    """Represents a trade on Polymarket"""
    
    id: str = Field(..., description="Transaction hash")
    trader_address: str = Field(..., description="Trader wallet address")
    market_id: str = Field(..., description="Market identifier")
    market_name: Optional[str] = Field(None, description="Market question")
    side: str = Field(..., description="BUY/SELL or YES/NO")
    size: float = Field(..., description="Position size in USDC")
    price: float = Field(..., description="Trade price (0-1)")
    timestamp: datetime = Field(..., description="Trade timestamp")
    transaction_hash: Optional[str] = Field(None, description="Blockchain tx hash")
    
    @property
    def is_whale_trade(self) -> bool:
        """Check if this is a whale trade (>$10k)"""
        return self.size >= 10000
    
    @property
    def whale_tier(self) -> int:
        """Get whale tier (1=small, 2=medium, 3=large)"""
        if self.size >= 100000:
            return 3
        elif self.size >= 50000:
            return 2
        elif self.size >= 10000:
            return 1
        return 0
    
    @property
    def whale_emoji(self) -> str:
        """Get emoji based on whale tier"""
        tier = self.whale_tier
        if tier == 3:
            return "🐋"  # Large whale
        elif tier == 2:
            return "🐳"  # Medium whale
        elif tier == 1:
            return "🐬"  # Small whale
        return "🐟"  # Not a whale
    
    def format_size(self) -> str:
        """Format trade size for display"""
        if self.size >= 1_000_000:
            return f"${self.size / 1_000_000:.2f}M"
        elif self.size >= 1_000:
            return f"${self.size / 1_000:.1f}k"
        return f"${self.size:.2f}"
    
    def format_price(self) -> str:
        """Format price as percentage"""
        return f"{self.price * 100:.1f}%"
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

