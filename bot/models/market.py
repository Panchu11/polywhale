"""
Market model
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class Market(BaseModel):
    """Represents a prediction market on Polymarket"""

    market_id: str = Field(..., description="Market identifier")
    question: str = Field(..., description="Market question")
    slug: Optional[str] = Field(None, description="Market slug for URL")
    description: Optional[str] = Field(None, description="Market description")
    category: Optional[str] = Field(None, description="Market category")
    end_date: Optional[datetime] = Field(None, description="Market end date")
    volume: float = Field(0, description="Total volume in USDC")
    liquidity: float = Field(0, description="Available liquidity")
    active: bool = Field(True, description="Is market active")
    
    def format_volume(self) -> str:
        """Format volume for display"""
        if self.volume >= 1_000_000:
            return f"${self.volume / 1_000_000:.2f}M"
        elif self.volume >= 1_000:
            return f"${self.volume / 1_000:.1f}k"
        return f"${self.volume:.2f}"
    
    def format_end_date(self) -> str:
        """Format end date for display"""
        if not self.end_date:
            return "No end date"

        now = datetime.now()
        delta = self.end_date - now

        if delta.days > 365:
            return f"Ends in {delta.days // 365} years"
        elif delta.days > 30:
            return f"Ends in {delta.days // 30} months"
        elif delta.days > 0:
            return f"Ends in {delta.days} days"
        elif delta.seconds > 3600:
            return f"Ends in {delta.seconds // 3600} hours"
        else:
            return "Ending soon"

    def get_market_url(self) -> str:
        """Get Polymarket market URL"""
        if self.slug:
            return f"https://polymarket.com/market/{self.slug}"
        return "https://polymarket.com"

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }

