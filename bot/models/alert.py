"""
Alert model
"""
from typing import Dict, Any
from pydantic import BaseModel, Field


class Alert(BaseModel):
    """Represents a user alert configuration"""
    
    id: int = Field(..., description="Alert ID")
    user_id: int = Field(..., description="User ID")
    alert_type: str = Field(..., description="Type of alert")
    filters: Dict[str, Any] = Field(default_factory=dict, description="Alert filters")
    is_active: bool = Field(True, description="Is alert active")
    
    def matches_trade(self, trade: Any) -> bool:
        """Check if a trade matches this alert's filters"""
        # Check minimum size
        min_size = self.filters.get("min_size", 10000)
        if trade.size < min_size:
            return False
        
        # Check market category
        categories = self.filters.get("categories", [])
        if categories and hasattr(trade, "category"):
            if trade.category not in categories:
                return False
        
        # Check specific markets
        markets = self.filters.get("markets", [])
        if markets and trade.market_id not in markets:
            return False
        
        # Check specific whales
        whales = self.filters.get("whales", [])
        if whales and trade.trader_address not in whales:
            return False
        
        return True

