"""
PolyWhale Bot - Main Entry Point
Track the smartest money in prediction markets
"""
import asyncio
import sys
import os
from loguru import logger
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ChatMemberHandler, ContextTypes
from telegram import Update


from config.settings import settings
from bot.handlers import (
    start, help_command, whales, markets, whale_profile,
    top, track, untrack, mywhales, settings as settings_handler,
    alerts, threshold, about
)
from bot.services.whale_tracker import WhaleTracker
from bot.services.broadcast_service import BroadcastService

# Use asyncpg Postgres (Neon) database
from bot.services.database import Database


# Configure logging
logger.remove()
logger.add(
    sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
    level=settings.LOG_LEVEL
)
# Ensure logs directory exists
os.makedirs("logs", exist_ok=True)
logger.add(
    "logs/bot_{time:YYYY-MM-DD}.log",
    rotation="1 day",
    retention="7 days",
    level=settings.LOG_LEVEL
)


async def on_my_chat_member(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Capture channel id when bot is added as admin/member to a channel."""
    try:
        mc = update.my_chat_member
        if not mc:
            return
        chat = mc.chat
        if chat.type != "channel":
            return
        # Save channel id for broadcasts
        context.application.bot_data["broadcast_channel_id"] = chat.id
        from_title = getattr(chat, "title", None) or "(no title)"
        logger.info(f"✅ Bot added to channel '{from_title}' with id {chat.id}")
        try:
            await context.bot.send_message(chat_id=chat.id, text="🐳 PolyWhale connected! Broadcasting enabled.")
        except Exception as e:
            logger.warning(f"Failed to send welcome message to channel: {e}")
    except Exception as e:
        logger.error(f"on_my_chat_member error: {e}")


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
        # Start whale tracker background loop
        application.create_task(whale_tracker.start())
        logger.info("✓ Whale tracker initialized and started")
    except Exception as e:
        logger.error(f"✗ Whale tracker initialization failed: {e}")
        sys.exit(1)
    # Initialize broadcast service
    try:
        broadcast = BroadcastService(db, application.bot)
        application.bot_data["broadcast_service"] = broadcast
        application.create_task(broadcast.start(application))
        logger.info("\u2713 Broadcast service initialized and started")
    except Exception as e:
        logger.error(f"\u2717 Broadcast service initialization failed: {e}")


    logger.info("🐋 PolyWhale bot started successfully!")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"Whale threshold: ${settings.WHALE_THRESHOLD:,}")
    logger.info(f"Poll interval: {settings.POLL_INTERVAL}s")


async def post_shutdown(application: Application) -> None:

    """Cleanup when bot shuts down"""

    # Stop broadcast service
    if "broadcast_service" in application.bot_data:
        try:
            await application.bot_data["broadcast_service"].stop()
        except Exception:
            pass

    logger.info("Shutting down PolyWhale bot...")

    # Stop whale tracker
    if "whale_tracker" in application.bot_data:
        whale_tracker = application.bot_data["whale_tracker"]
        await whale_tracker.stop()
        logger.info("\u2713 Whale tracker stopped")

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
    # Basic commands
    application.add_handler(CommandHandler("start", start.handle))
    application.add_handler(CommandHandler("help", help_command.handle))
    application.add_handler(CommandHandler("about", about.handle))

    # Whale tracking commands
    application.add_handler(CommandHandler("whales", whales.handle))
    application.add_handler(CommandHandler("whale", whale_profile.handle))
    application.add_handler(CommandHandler("top", top.handle))
    application.add_handler(CommandHandler("track", track.handle))
    application.add_handler(CommandHandler("untrack", untrack.handle))

    # Channel admin/member updates (to capture channel id)
    application.add_handler(ChatMemberHandler(on_my_chat_member, ChatMemberHandler.MY_CHAT_MEMBER))

    application.add_handler(CommandHandler("mywhales", mywhales.handle))

    # Market commands
    application.add_handler(CommandHandler("markets", markets.handle))

    # Settings commands
    application.add_handler(CommandHandler("settings", settings_handler.handle))
    application.add_handler(CommandHandler("alerts", alerts.handle))
    application.add_handler(CommandHandler("threshold", threshold.handle))

    # Register message handlers (for non-command messages)
    # application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start the bot
    logger.info("Bot is ready to receive commands")
    application.run_polling(allowed_updates=["message", "callback_query", "my_chat_member"])


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.exception(f"Fatal error: {e}")
        sys.exit(1)

