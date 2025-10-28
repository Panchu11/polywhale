"""
Test Telegram bot connectivity
"""
import asyncio
import sys
from pathlib import Path
from loguru import logger
from telegram import Bot

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config.settings import settings


async def test_bot():
    """Test Telegram bot"""
    logger.info("Testing Telegram bot...")
    
    try:
        # Validate settings
        settings.validate()
        logger.info("✓ Settings validated")
        
        # Create bot instance
        bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
        
        # Get bot info
        me = await bot.get_me()
        logger.info(f"✓ Bot connected: @{me.username}")
        logger.info(f"  Name: {me.first_name}")
        logger.info(f"  ID: {me.id}")
        
        logger.info("\n✓ Bot test complete!")
        logger.info(f"\nYou can find your bot at: https://t.me/{me.username}")
        
    except ValueError as e:
        logger.error(f"✗ Settings validation failed: {e}")
        logger.error("\nMake sure you have:")
        logger.error("1. Created a .env file (copy from .env.example)")
        logger.error("2. Added your TELEGRAM_BOT_TOKEN from @BotFather")
        sys.exit(1)
    except Exception as e:
        logger.error(f"✗ Bot test failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(test_bot())

