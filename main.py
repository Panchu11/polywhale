"""
PolyWhale Bot - Main Entry Point
Track the smartest money in prediction markets
"""
import asyncio
import sys
from loguru import logger
from telegram.ext import Application, CommandHandler, MessageHandler, filters

from config.settings import settings
from bot.handlers import start, help_command, whales, markets, whale_profile
from bot.services.whale_tracker import WhaleTracker
from bot.services.database import Database


# Configure logging
logger.remove()
logger.add(
    sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
    level=settings.LOG_LEVEL
)
logger.add(
    "logs/bot_{time:YYYY-MM-DD}.log",
    rotation="1 day",
    retention="7 days",
    level=settings.LOG_LEVEL
)


async def post_init(application: Application) -> None:
    """Initialize services after bot starts"""
    logger.info("Initializing PolyWhale bot...")
    
    # Validate settings
    try:
        settings.validate()
        logger.info("✓ Settings validated")
    except ValueError as e:
        logger.error(f"✗ Settings validation failed: {e}")
        sys.exit(1)
    
    # Initialize database
    try:
        db = Database()
        await db.connect()
        logger.info("✓ Database connected")
        application.bot_data["db"] = db
    except Exception as e:
        logger.error(f"✗ Database connection failed: {e}")
        sys.exit(1)
    
    # Initialize whale tracker
    try:
        whale_tracker = WhaleTracker(db)
        application.bot_data["whale_tracker"] = whale_tracker
        logger.info("✓ Whale tracker initialized")
    except Exception as e:
        logger.error(f"✗ Whale tracker initialization failed: {e}")
        sys.exit(1)
    
    logger.info("🐋 PolyWhale bot started successfully!")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"Whale threshold: ${settings.WHALE_THRESHOLD:,}")
    logger.info(f"Poll interval: {settings.POLL_INTERVAL}s")


async def post_shutdown(application: Application) -> None:
    """Cleanup when bot shuts down"""
    logger.info("Shutting down PolyWhale bot...")
    
    # Close database connection
    if "db" in application.bot_data:
        db = application.bot_data["db"]
        await db.close()
        logger.info("✓ Database connection closed")
    
    logger.info("👋 PolyWhale bot stopped")


def main():
    """Main function to run the bot"""
    logger.info("Starting PolyWhale bot...")
    
    # Create application
    application = (
        Application.builder()
        .token(settings.TELEGRAM_BOT_TOKEN)
        .post_init(post_init)
        .post_shutdown(post_shutdown)
        .build()
    )
    
    # Register command handlers
    application.add_handler(CommandHandler("start", start.handle))
    application.add_handler(CommandHandler("help", help_command.handle))
    application.add_handler(CommandHandler("whales", whales.handle))
    application.add_handler(CommandHandler("markets", markets.handle))
    application.add_handler(CommandHandler("whale", whale_profile.handle))
    
    # Register message handlers (for non-command messages)
    # application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Start the bot
    logger.info("Bot is ready to receive commands")
    application.run_polling(allowed_updates=["message", "callback_query"])


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.exception(f"Fatal error: {e}")
        sys.exit(1)

