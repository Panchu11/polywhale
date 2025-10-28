"""
/mywhales command handler - Show user's tracked whales
"""
from telegram import Update
from telegram.ext import ContextTypes
from loguru import logger


async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /mywhales command"""
    user = update.effective_user
    logger.info(f"User {user.id} requested tracked whales")
    
    # Get database from context
    if "db" not in context.bot_data:
        await update.message.reply_text("⚠️ Database not available. Please try again later.")
        return
    
    db = context.bot_data["db"]
    
    try:
        # Get user's tracked whales
        tracked = await db.get_tracked_whales(user.id)
        
        if not tracked:
            await update.message.reply_text(
                "📋 **You're not tracking any whales yet!**\n\n"
                "Start tracking whales to get notified of their trades:\n"
                "• Use `/top` to see the leaderboard\n"
                "• Use `/track <address>` to track a whale\n\n"
                "Example: `/track 0x742d35Cc6634C0532925a3b844Bc9e7595f3f8a`",
                parse_mode="Markdown"
            )
            return
        
        # Format tracked whales message
        message = f"🐋 **Your Tracked Whales** ({len(tracked)})\n\n"
        
        for i, whale_addr in enumerate(tracked, 1):
            short_addr = f"{whale_addr[:6]}...{whale_addr[-4:]}"
            message += f"{i}. `{short_addr}`\n"
            message += f"   Use `/whale {whale_addr}` to view profile\n"
            message += f"   Use `/untrack {whale_addr}` to stop tracking\n"
            message += "\n"
        
        message += "_You'll receive notifications when these whales trade_"
        
        await update.message.reply_text(
            message,
            parse_mode="Markdown"
        )
        
    except Exception as e:
        logger.error(f"Error fetching tracked whales: {e}")
        await update.message.reply_text(
            "⚠️ Error fetching tracked whales. Please try again later."
        )

