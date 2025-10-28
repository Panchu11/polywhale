"""
Whale model
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class Whale(BaseModel):
    """Represents a whale trader on Polymarket"""
    
    address: str = Field(..., description="Ethereum wallet address")
    nickname: Optional[str] = Field(None, description="Optional nickname")
    total_volume: float = Field(0, description="Total trading volume in USDC")
    total_trades: int = Field(0, description="Total number of trades")
    wins: int = Field(0, description="Number of winning trades")
    losses: int = Field(0, description="Number of losing trades")
    win_rate: float = Field(0, description="Win rate percentage")
    last_trade_at: Optional[datetime] = Field(None, description="Last trade timestamp")
    first_seen_at: datetime = Field(default_factory=datetime.now, description="First seen timestamp")
    is_tracked: bool = Field(False, description="Is this a featured whale")
    
    @property
    def short_address(self) -> str:
        """Get shortened address (0x1234...5678)"""
        if len(self.address) < 10:
            return self.address
        return f"{self.address[:6]}...{self.address[-4:]}"
    
    @property
    def display_name(self) -> str:
        """Get display name (nickname or short address)"""
        return self.nickname if self.nickname else self.short_address
    
    def calculate_win_rate(self) -> float:
        """Calculate win rate from wins and losses"""
        total = self.wins + self.losses
        if total == 0:
            return 0.0
        return (self.wins / total) * 100
    
    def format_volume(self) -> str:
        """Format total volume for display"""
        if self.total_volume >= 1_000_000:
            return f"${self.total_volume / 1_000_000:.2f}M"
        elif self.total_volume >= 1_000:
            return f"${self.total_volume / 1_000:.1f}k"
        return f"${self.total_volume:.2f}"
    
    def format_win_rate(self) -> str:
        """Format win rate as percentage"""
        return f"{self.win_rate:.1f}%"
    
    def get_rank_emoji(self, rank: int) -> str:
        """Get emoji based on leaderboard rank"""
        if rank == 1:
            return "🥇"
        elif rank == 2:
            return "🥈"
        elif rank == 3:
            return "🥉"
        return f"{rank}."
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }

