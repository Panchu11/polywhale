"""
/whale command handler - Show whale profile
"""
from telegram import Update
from telegram.ext import ContextTypes
from loguru import logger


async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /whale <address> command"""
    user = update.effective_user
    
    # Check if address was provided
    if not context.args:
        await update.message.reply_text(
            "⚠️ Please provide a whale address.\n\n"
            "Usage: `/whale <address>`\n"
            "Example: `/whale 0x742d...3f8a`",
            parse_mode="Markdown"
        )
        return
    
    address = context.args[0]
    logger.info(f"User {user.id} requested whale profile for {address}")
    
    # Get database from context
    if "db" not in context.bot_data:
        await update.message.reply_text("⚠️ Database not available. Please try again later.")
        return
    
    db = context.bot_data["db"]
    
    try:
        # Fetch whale data
        whale = await db.get_whale(address)
        
        if not whale:
            await update.message.reply_text(
                f"🐋 Whale `{address}` not found.\n\n"
                "This address might not have made any whale trades yet.",
                parse_mode="Markdown"
            )
            return
        
        # Format whale profile message
        message = f"🐋 **Whale Profile**\n\n"
        message += f"Address: `{whale.short_address}`\n"
        
        if whale.nickname:
            message += f"Nickname: {whale.nickname}\n"
        
        message += f"\n📊 **Statistics**\n"
        message += f"Total Volume: {whale.format_volume()}\n"
        message += f"Total Trades: {whale.total_trades}\n"
        message += f"Wins: {whale.wins} | Losses: {whale.losses}\n"
        message += f"Win Rate: {whale.format_win_rate()}\n"
        
        if whale.last_trade_at:
            message += f"Last Trade: {whale.last_trade_at.strftime('%Y-%m-%d %H:%M')}\n"
        
        message += f"\n_Use /track {whale.short_address} to follow this whale_"
        
        await update.message.reply_text(
            message,
            parse_mode="Markdown"
        )
        
    except Exception as e:
        logger.error(f"Error fetching whale profile: {e}")
        await update.message.reply_text(
            "⚠️ Error fetching whale profile. Please try again later."
        )

