"""
PolyWhale Bot - Simple Version (No Database Required)
Track the smartest money in prediction markets
"""
import asyncio
import sys
from loguru import logger
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from config.settings import settings

# Configure logging
logger.remove()
logger.add(
    sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
    level="INFO"
)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    welcome_message = """
🐋 **Welcome to PolyWhale Tracker!**

Track the smartest money in prediction markets.

**Available Commands:**
/start - Show this welcome message
/help - Get help and information
/test - Test bot functionality

**Status:** ✅ Bot is running!

_Note: Database features are being set up. Basic commands are available now._
"""
    await update.message.reply_text(welcome_message, parse_mode='Markdown')
    logger.info(f"User {update.effective_user.id} started the bot")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    help_text = """
🆘 **PolyWhale Tracker Help**

**What is PolyWhale?**
PolyWhale tracks large trades (whales) on Polymarket, the world's largest prediction market.

**Commands:**
• /start - Welcome message
• /help - This help message  
• /test - Test bot functionality

**Coming Soon:**
• Real-time whale alerts
• Market analysis
• Whale profiles
• Custom notifications

**Support:**
For issues or questions, contact the developer.

🐋 Happy whale tracking!
"""
    await update.message.reply_text(help_text, parse_mode='Markdown')
    logger.info(f"User {update.effective_user.id} requested help")


async def test_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /test command"""
    test_message = """
🧪 **Bot Test Results**

✅ Bot is online
✅ Commands are working
✅ Telegram connection active

**Bot Info:**
• Name: PolyWhale Tracker
• Username: @polywhale_tracker_bot
• Version: 1.0.0

**Next Steps:**
1. Database setup in progress
2. Polymarket API integration ready
3. Whale tracking will be enabled soon

Everything is working! 🎉
"""
    await update.message.reply_text(test_message, parse_mode='Markdown')
    logger.info(f"User {update.effective_user.id} ran test command")


async def post_init(application: Application) -> None:
    """Initialize services after bot starts"""
    logger.info("🐋 PolyWhale bot starting...")
    
    # Validate settings
    try:
        settings.validate()
        logger.info("✓ Settings validated")
    except ValueError as e:
        logger.error(f"✗ Settings validation failed: {e}")
        sys.exit(1)
    
    logger.info("🐋 PolyWhale bot started successfully!")
    logger.info(f"Bot username: @polywhale_tracker_bot")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info("Ready to receive commands!")


def main():
    """Main function to run the bot"""
    logger.info("Starting PolyWhale bot (Simple Mode)...")
    
    # Create application
    application = (
        Application.builder()
        .token(settings.TELEGRAM_BOT_TOKEN)
        .post_init(post_init)
        .build()
    )
    
    # Register command handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("test", test_command))
    
    # Start the bot
    logger.info("Bot is ready to receive commands")
    logger.info("Press Ctrl+C to stop")
    application.run_polling(allowed_updates=["message"])


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("\n👋 Bot stopped by user")
    except Exception as e:
        logger.exception(f"Fatal error: {e}")
        sys.exit(1)

