"""
/markets command handler - Show top markets by whale activity
"""
from telegram import Update
from telegram.ext import ContextTypes
from loguru import logger


async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /markets command"""
    user = update.effective_user
    logger.info(f"User {user.id} requested markets")
    
    # Get database from context
    if "db" not in context.bot_data:
        await update.message.reply_text("⚠️ Database not available. Please try again later.")
        return
    
    db = context.bot_data["db"]
    
    try:
        # Fetch top markets by whale activity
        markets = await db.get_top_markets_by_whale_activity(limit=10)
        
        if not markets:
            await update.message.reply_text(
                "📊 No market data available yet.\n\n"
                "The bot is still collecting data. Check back soon!"
            )
            return
        
        # Format markets message
        message = "🔥 **Top Markets by Whale Activity** (24h)\n\n"
        
        for i, market in enumerate(markets, 1):
            whale_trades = market.get("whale_trades_24h", 0)
            whale_volume = market.get("whale_volume_24h", 0)
            question = market.get("question", "Unknown market")
            
            # Shorten question if too long
            if len(question) > 60:
                question = question[:57] + "..."
            
            message += f"{i}. **{question}**\n"
            message += f"   🐋 {whale_trades} whale trades\n"
            message += f"   💰 ${whale_volume:,.0f} whale volume\n"
            message += "\n"
        
        message += "_Use /whale <address> to view whale profiles_"
        
        await update.message.reply_text(
            message,
            parse_mode="Markdown"
        )
        
    except Exception as e:
        logger.error(f"Error fetching markets: {e}")
        await update.message.reply_text(
            "⚠️ Error fetching markets. Please try again later."
        )

