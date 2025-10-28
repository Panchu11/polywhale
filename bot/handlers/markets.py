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
        # Fetch active markets from Polymarket API
        from bot.services.polymarket_api import PolymarketAPI
        api = PolymarketAPI()

        markets = await api.fetch_markets(limit=10)

        if not markets:
            await update.message.reply_text(
                "📊 No market data available yet.\n\n"
                "Unable to fetch markets from Polymarket. Try again later!"
            )
            return

        # Format markets message
        message = "🔥 **Top Active Markets on Polymarket**\n\n"

        for i, market in enumerate(markets, 1):
            question = market.question
            volume = market.volume

            # Shorten question if too long
            if len(question) > 60:
                question = question[:57] + "..."

            message += f"{i}. **{question}**\n"
            message += f"   💰 Volume: {market.format_volume()}\n"
            message += "\n"

        message += "_Markets are updated in real-time from Polymarket_"

        await api.close()

        await update.message.reply_text(
            message,
            parse_mode="Markdown"
        )
        
    except Exception as e:
        logger.error(f"Error fetching markets: {e}")
        await update.message.reply_text(
            "⚠️ Error fetching markets. Please try again later."
        )

