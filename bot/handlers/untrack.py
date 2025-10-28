"""
/untrack command handler - Stop tracking a whale
"""
from telegram import Update
from telegram.ext import ContextTypes
from loguru import logger


async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /untrack <address> command"""
    user = update.effective_user
    
    # Check if address was provided
    if not context.args:
        await update.message.reply_text(
            "⚠️ Please provide a whale address to untrack.\n\n"
            "Usage: `/untrack <address>`\n"
            "Example: `/untrack 0x742d35Cc6634C0532925a3b844Bc9e7595f3f8a`",
            parse_mode="Markdown"
        )
        return
    
    address = context.args[0].lower()
    logger.info(f"User {user.id} wants to untrack whale {address}")
    
    # Get database from context
    if "db" not in context.bot_data:
        await update.message.reply_text("⚠️ Database not available. Please try again later.")
        return
    
    db = context.bot_data["db"]
    
    try:
        # Untrack the whale
        result = await db.untrack_whale(user.id, address)
        
        short_addr = f"{address[:6]}...{address[-4:]}"
        
        if result:
            await update.message.reply_text(
                f"✅ **Whale Untracked!**\n\n"
                f"You're no longer tracking: `{short_addr}`\n\n"
                f"You won't receive notifications for this whale anymore.\n\n"
                f"Use `/mywhales` to see remaining tracked whales",
                parse_mode="Markdown"
            )
            logger.info(f"User {user.id} stopped tracking whale {address}")
        else:
            await update.message.reply_text(
                f"⚠️ You're not tracking `{short_addr}`\n\n"
                f"Use `/mywhales` to see your tracked whales",
                parse_mode="Markdown"
            )
        
    except Exception as e:
        logger.error(f"Error untracking whale: {e}")
        await update.message.reply_text(
            "⚠️ Error untracking whale. Please try again later."
        )

