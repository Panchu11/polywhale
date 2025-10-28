"""
/markets command handler - Show top markets by whale activity (last 24h)
"""
from datetime import datetime, timedelta
from telegram import Update
from telegram.ext import ContextTypes
from loguru import logger
from bot.utils.formatters import format_time_ago


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
        since = datetime.utcnow() - timedelta(hours=24)
        markets = await db.get_top_markets_from_trades_since(since, limit=10)

        if not markets:
            await update.message.reply_text(
                "📊 No whale activity recorded in the last 24h yet.\n\n"
                "Try again later after new whale trades occur."
            )
            return

        # Format markets message
        message = "🔥 **Top Markets by Whale Activity (24h)**\n\n"

        for i, m in enumerate(markets, 1):
            question = m.get("market_name") or "Unknown Market"
            event_slug = m.get("event_slug") or ""
            market_slug = m.get("market_slug") or ""
            if event_slug:
                market_url = f"https://polymarket.com/event/{event_slug}"
            elif market_slug:
                market_url = f"https://polymarket.com/market/{market_slug}"
            else:
                market_url = "https://polymarket.com"

            # Shorten question if too long
            if len(question) > 60:
                question = question[:57] + "..."

            whale_volume = float(m.get("whale_volume") or 0)
            whale_trades = int(m.get("whale_trades") or 0)
            last_trade = m.get("last_whale_trade")
            last_txt = format_time_ago(last_trade) if last_trade else "n/a"

            message += f"{i}. [{question}]({market_url})\n"
            message += f"   🐋 Whale Volume: ${whale_volume:,.0f} | {whale_trades} trades | last: {last_txt}\n"
            message += "\n"

        message += "_Based on whale (≥$500) trades recorded in the last 24 hours_"

        await update.message.reply_text(
            message,
            parse_mode="Markdown"
        )

    except Exception as e:
        logger.error(f"Error fetching markets: {e}")
        await update.message.reply_text(
            "⚠️ Error fetching markets. Please try again later."
        )

