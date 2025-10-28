"""
/track command handler - Track a whale
"""
from telegram import Update
from telegram.ext import ContextTypes
from loguru import logger


async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /track <address> command"""
    user = update.effective_user
    
    # Check if address was provided
    if not context.args:
        await update.message.reply_text(
            "⚠️ Please provide a whale address to track.\n\n"
            "Usage: `/track <address>`\n"
            "Example: `/track 0x742d35Cc6634C0532925a3b844Bc9e7595f3f8a`",
            parse_mode="Markdown"
        )
        return
    
    address = context.args[0].lower()
    logger.info(f"User {user.id} wants to track whale {address}")
    
    # Get database from context
    if "db" not in context.bot_data:
        await update.message.reply_text("⚠️ Database not available. Please try again later.")
        return
    
    db = context.bot_data["db"]
    
    try:
        # Track the whale
        await db.track_whale(user.id, address)
        
        short_addr = f"{address[:6]}...{address[-4:]}"
        
        await update.message.reply_text(
            f"✅ **Whale Tracked!**\n\n"
            f"You're now tracking: `{short_addr}`\n\n"
            f"You'll receive notifications when this whale makes trades.\n\n"
            f"Use `/mywhales` to see all tracked whales\n"
            f"Use `/untrack {address}` to stop tracking",
            parse_mode="Markdown"
        )
        
        logger.info(f"User {user.id} is now tracking whale {address}")
        
    except Exception as e:
        logger.error(f"Error tracking whale: {e}")
        await update.message.reply_text(
            "⚠️ Error tracking whale. Please try again later."
        )

