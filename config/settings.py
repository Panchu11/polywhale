"""
Configuration settings for PolyWhale bot
"""
import os
from typing import List
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Settings:
    """Application settings"""
    
    # Telegram Configuration
    TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
    
    # Database Configuration
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")

    # Supabase Configuration (Alternative to direct PostgreSQL)
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY", "")

    # Redis Configuration
    REDIS_URL: str = os.getenv("REDIS_URL", "")
    
    # Polymarket API Configuration
    POLYMARKET_DATA_API: str = os.getenv(
        "POLYMARKET_DATA_API", 
        "https://data-api.polymarket.com"
    )
    POLYMARKET_GAMMA_API: str = os.getenv(
        "POLYMARKET_GAMMA_API",
        "https://gamma-api.polymarket.com"
    )
    
    # Bot Configuration
    WHALE_THRESHOLD: int = int(os.getenv("WHALE_THRESHOLD", "10000"))
    POLL_INTERVAL: int = int(os.getenv("POLL_INTERVAL", "60"))
    MAX_ALERTS_PER_USER: int = int(os.getenv("MAX_ALERTS_PER_USER", "50"))
    
    # Environment
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Monitoring
    SENTRY_DSN: str = os.getenv("SENTRY_DSN", "")
    
    # Admin Configuration
    ADMIN_USER_IDS: List[int] = [
        int(uid) for uid in os.getenv("ADMIN_USER_IDS", "").split(",") 
        if uid.strip()
    ]
    
    # Whale Thresholds
    WHALE_TIER_1: int = 10000   # Small whale
    WHALE_TIER_2: int = 50000   # Medium whale
    WHALE_TIER_3: int = 100000  # Large whale
    
    # Cache TTL (seconds)
    CACHE_TTL_MARKETS: int = 300      # 5 minutes
    CACHE_TTL_WHALE_STATS: int = 600  # 10 minutes
    CACHE_TTL_LEADERBOARD: int = 1800 # 30 minutes
    
    # API Rate Limiting
    API_RATE_LIMIT: int = 1  # requests per second
    
    @classmethod
    def validate(cls) -> bool:
        """Validate required settings"""
        # Check Telegram token
        if not cls.TELEGRAM_BOT_TOKEN:
            raise ValueError("Missing required setting: TELEGRAM_BOT_TOKEN")

        # Check database configuration (either DATABASE_URL or Supabase)
        has_postgres = bool(cls.DATABASE_URL)
        has_supabase = bool(cls.SUPABASE_URL and cls.SUPABASE_KEY)

        if not (has_postgres or has_supabase):
            raise ValueError("Missing database configuration: Need either DATABASE_URL or (SUPABASE_URL + SUPABASE_KEY)")

        return True


# Create settings instance
settings = Settings()

