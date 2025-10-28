"""
/whales command handler - Show recent whale trades
"""
from telegram import Update
from telegram.ext import ContextTypes
from loguru import logger
from datetime import datetime, timedelta


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
        # Fetch recent whale trades (last hour)
        since = datetime.now() - timedelta(hours=1)
        trades = await db.get_recent_whale_trades(since=since, limit=10)
        
        if not trades:
            await update.message.reply_text(
                "🐋 No whale trades in the last hour.\n\n"
                "Whales might be sleeping! 😴\n"
                "Try again later or use /markets to see active markets."
            )
            return
        
        # Format trades message
        message = "🐋 **Recent Whale Trades** (Last Hour)\n\n"
        
        for trade in trades:
            whale_emoji = get_whale_emoji(trade.size)
            message += f"{whale_emoji} **{format_size(trade.size)}** Trade\n"
            message += f"Market: {trade.market_name[:50]}...\n" if len(trade.market_name) > 50 else f"Market: {trade.market_name}\n"
            message += f"Side: {trade.side} @ {format_price(trade.price)}\n"
            message += f"Whale: `{shorten_address(trade.trader_address)}`\n"
            message += f"Time: {format_time_ago(trade.timestamp)}\n"
            message += "\n"
        
        message += f"_Showing {len(trades)} whale trades_\n"
        message += f"_Threshold: ${context.bot_data.get('whale_threshold', 10000):,}_"
        
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
    if size >= 100000:
        return "🐋"  # Large whale
    elif size >= 50000:
        return "🐳"  # Medium whale
    else:
        return "🐬"  # Small whale


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
    """Format timestamp as time ago"""
    now = datetime.now()
    delta = now - timestamp
    
    if delta.seconds < 60:
        return "just now"
    elif delta.seconds < 3600:
        minutes = delta.seconds // 60
        return f"{minutes}m ago"
    elif delta.seconds < 86400:
        hours = delta.seconds // 3600
        return f"{hours}h ago"
    else:
        return timestamp.strftime("%Y-%m-%d %H:%M")

