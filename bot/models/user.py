"""
User model
"""
from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field


class User(BaseModel):
    """Represents a Telegram user"""
    
    user_id: int = Field(..., description="Telegram user ID")
    username: Optional[str] = Field(None, description="Telegram username")
    first_name: Optional[str] = Field(None, description="User's first name")
    created_at: datetime = Field(default_factory=datetime.now, description="Registration date")
    last_active: datetime = Field(default_factory=datetime.now, description="Last activity")
    is_active: bool = Field(True, description="Is user active")
    referrer_id: Optional[int] = Field(None, description="Referrer user ID")
    referral_count: int = Field(0, description="Number of referrals")
    settings: Dict[str, Any] = Field(default_factory=dict, description="User preferences")
    
    @property
    def display_name(self) -> str:
        """Get display name"""
        if self.first_name:
            return self.first_name
        elif self.username:
            return f"@{self.username}"
        return f"User {self.user_id}"
    
    def get_setting(self, key: str, default: Any = None) -> Any:
        """Get a user setting"""
        return self.settings.get(key, default)
    
    def set_setting(self, key: str, value: Any) -> None:
        """Set a user setting"""
        self.settings[key] = value
    
    def get_whale_threshold(self) -> int:
        """Get user's whale threshold setting"""
        return self.get_setting("whale_threshold", 500)

    def get_quiet_hours(self) -> tuple:
        """Get user's quiet hours (start, end)"""
        return self.get_setting("quiet_hours", (23, 7))
    
    def is_quiet_time(self) -> bool:
        """Check if current time is in quiet hours"""
        start, end = self.get_quiet_hours()
        current_hour = datetime.now().hour
        
        if start < end:
            return start <= current_hour < end
        else:  # Quiet hours span midnight
            return current_hour >= start or current_hour < end
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

