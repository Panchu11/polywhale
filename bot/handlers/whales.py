"""
/whales command handler - Show recent whale trades
"""
from telegram import Update
from telegram.ext import ContextTypes
from loguru import logger
from datetime import datetime, timedelta
from config.settings import settings


async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /whales command"""
    user = update.effective_user
    logger.info(f"User {user.id} requested whale trades")
    
    # Get database from context
    if "db" not in context.bot_data:
        await update.message.reply_text("⚠️ Database not available. Please try again later.")
        return
    
    db = context.bot_data["db"]
    
    try:
        # Fetch recent whale trades from database (use UTC to match stored timestamps)
        since = datetime.utcnow() - timedelta(minutes=10)
        trades = await db.get_recent_whale_trades(since, limit=10)

        if not trades:
            # No trades in database yet - fetch live from Polymarket
            from bot.services.polymarket_api import PolymarketAPI
            api = PolymarketAPI()

            live_trades = await api.fetch_recent_trades(limit=500)  # Increased from 50 to 500
            await api.close()

            # Filter for whale trades using configured threshold
            whale_trades = [t for t in live_trades if t.is_whale_trade]

            if not whale_trades:
                await update.message.reply_text(
                    "🐋 No whale trades detected recently.\n\n"
                    "Whales might be sleeping! 😴\n"
                    "Try again later or use /markets to see active markets."
                )
                return

            # Show live whale trades
            message = "🐋 **Live Whale Trades** (from Polymarket)\n\n"

            for trade in whale_trades[:10]:
                whale_emoji = get_whale_emoji(trade.size)
                trader_name = trade.get_trader_display_name()
                profile_url = trade.get_profile_url()
                market_url = trade.get_market_url()

                message += f"{whale_emoji} **{format_size(trade.size)}** Trade\n"
                message += f"Market: [{trade.market_name[:50]}]({market_url})\n"
                message += f"Side: {trade.side} {trade.outcome if trade.outcome else ''}\n"
                message += f"Trader: [{trader_name}]({profile_url})\n"
                message += "\n"

            message += f"_Showing {len(whale_trades[:10])} live whale trades_\n"
            message += f"_Threshold: ${settings.WHALE_THRESHOLD}+_"

            await update.message.reply_text(message, parse_mode="Markdown")
            return
        
        # Format trades message
        message = "🐋 **Recent Whale Trades** (Last 10 Minutes)\n\n"
        
        for trade in trades:
            whale_emoji = get_whale_emoji(trade.size)
            message += f"{whale_emoji} **{format_size(trade.size)}** Trade\n"
            market_name = (trade.market_name or "Unknown")
            message += f"Market: {market_name[:50]}...\n" if len(market_name) > 50 else f"Market: {market_name}\n"
            message += f"Side: {trade.side} @ {format_price(trade.price)}\n"
            profile_url = f"https://polymarket.com/profile/{trade.trader_address}"
            short_addr = shorten_address(trade.trader_address)
            message += f"Trader: [{short_addr}]({profile_url})\n"
            message += f"Time: {format_time_ago(trade.timestamp)}\n"
            message += "\n"

        message += f"_Showing {len(trades)} whale trades_\n"
        message += f"_Threshold: ${settings.WHALE_THRESHOLD:,}_"

        await update.message.reply_text(
            message,
            parse_mode="Markdown"
        )
        
    except Exception as e:
        logger.error(f"Error fetching whale trades: {e}")
        await update.message.reply_text(
            "⚠️ Error fetching whale trades. Please try again later."
        )


def get_whale_emoji(size: float) -> str:
    """Get emoji based on trade size"""
    if size >= 10000:
        return "🐋"  # Mega whale
    elif size >= 5000:
        return "🐳"  # Large whale
    elif size >= 1000:
        return "🐬"  # Medium whale
    else:
        return "🐟"  # Small whale


def format_size(size: float) -> str:
    """Format trade size"""
    if size >= 1_000_000:
        return f"${size / 1_000_000:.2f}M"
    elif size >= 1_000:
        return f"${size / 1_000:.1f}k"
    return f"${size:.2f}"


def format_price(price: float) -> str:
    """Format price as percentage"""
    return f"{price * 100:.1f}%"


def shorten_address(address: str) -> str:
    """Shorten Ethereum address"""
    if len(address) < 10:
        return address
    return f"{address[:6]}...{address[-4:]}"


def format_time_ago(timestamp: datetime) -> str:
    """Format timestamp as time ago (assumes naive UTC timestamps)."""
    now = datetime.utcnow()
    # If timestamp is timezone-aware, convert to UTC then drop tz
    if getattr(timestamp, "tzinfo", None) is not None:
        from datetime import timezone
        timestamp = timestamp.astimezone(timezone.utc).replace(tzinfo=None)
    delta = now - timestamp
    total_seconds = int(delta.total_seconds())

    if total_seconds < 60:
        return "just now"
    elif total_seconds < 3600:
        minutes = total_seconds // 60
        return f"{minutes}m ago"
    elif total_seconds < 86400:
        hours = total_seconds // 3600
        return f"{hours}h ago"
    elif delta.days == 1:
        return "yesterday"
    elif delta.days < 7:
        return f"{delta.days}d ago"
    else:
        return timestamp.strftime("%Y-%m-%d %H:%M")

