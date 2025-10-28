"""
/top command handler - Show whale leaderboard with time filters
"""
from telegram import Update
from telegram.ext import ContextTypes
from loguru import logger
from datetime import datetime, timedelta


def get_whale_emoji(volume: float) -> str:
    """Get emoji based on volume"""
    if volume >= 10000:
        return "🐋"
    elif volume >= 5000:
        return "🐳"
    elif volume >= 1000:
        return "🐬"
    else:
        return "🐟"


def aggregate_whales(trades, threshold=500):
    """Aggregate trades by trader"""
    whale_stats = {}
    for trade in trades:
        if trade.size >= threshold:
            addr = trade.trader_address
            if addr not in whale_stats:
                whale_stats[addr] = {
                    'total_volume': 0,
                    'trade_count': 0,
                    'largest_trade': 0,
                    'trader_name': trade.trader_name or '',
                    'trader_pseudonym': trade.trader_pseudonym or '',
                    'profile_url': trade.get_profile_url()
                }
            whale_stats[addr]['total_volume'] += trade.size
            whale_stats[addr]['trade_count'] += 1
            whale_stats[addr]['largest_trade'] = max(whale_stats[addr]['largest_trade'], trade.size)

    return sorted(whale_stats.items(), key=lambda x: x[1]['total_volume'], reverse=True)


def format_whale_entry(rank: int, address: str, stats: dict, compact=False) -> str:
    """Format a single whale entry"""
    emoji = get_whale_emoji(stats['total_volume'])

    # Get trader display name
    if stats['trader_pseudonym']:
        trader_name = stats['trader_pseudonym']
    elif stats['trader_name']:
        trader_name = stats['trader_name']
    else:
        trader_name = f"{address[:6]}...{address[-4:]}"

    profile_url = stats['profile_url']

    if compact:
        return f"{rank}. {emoji} [{trader_name}]({profile_url}) - ${stats['total_volume']:,.0f}"
    else:
        entry = f"{rank}. {emoji} [{trader_name}]({profile_url})\n"
        entry += f"   💰 ${stats['total_volume']:,.0f} | 📊 {stats['trade_count']} trades | 🎯 ${stats['largest_trade']:,.0f} largest\n"
        return entry


async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /top command - Show top whales by volume with time filters"""
    user = update.effective_user
    logger.info(f"User {user.id} requested whale leaderboard")

    # Get database from context
    if "db" not in context.bot_data:
        await update.message.reply_text("⚠️ Database not available. Please try again later.")
        return

    db = context.bot_data["db"]

    try:
        # Fetch trades from Polymarket API
        from bot.services.polymarket_api import PolymarketAPI
        api = PolymarketAPI()

        # Fetch more trades to cover 30 days
        trades = await api.fetch_recent_trades(limit=1000)
        await api.close()

        if not trades:
            await update.message.reply_text(
                "📊 No whale data available yet.\n\n"
                "Check back soon!"
            )
            return

        # Calculate time thresholds
        now = datetime.now()
        time_24h = now - timedelta(hours=24)
        time_7d = now - timedelta(days=7)
        time_30d = now - timedelta(days=30)

        # Filter trades by time periods
        trades_24h = [t for t in trades if t.timestamp.replace(tzinfo=None) >= time_24h]
        trades_7d = [t for t in trades if t.timestamp.replace(tzinfo=None) >= time_7d]
        trades_30d = [t for t in trades if t.timestamp.replace(tzinfo=None) >= time_30d]

        # Aggregate whales for each period
        whales_24h = aggregate_whales(trades_24h)[:5]
        whales_7d = aggregate_whales(trades_7d)[:5]
        whales_30d = aggregate_whales(trades_30d)[:5]

        # Build message
        message = "🏆 **Top Whales Leaderboard**\n\n"

        # 24 Hours
        message += "⏰ **Last 24 Hours**\n"
        if whales_24h:
            for i, (addr, stats) in enumerate(whales_24h, 1):
                message += format_whale_entry(i, addr, stats, compact=True) + "\n"
        else:
            message += "_No whale activity in last 24h_\n"

        message += "\n"

        # 7 Days
        message += "📅 **Last 7 Days**\n"
        if whales_7d:
            for i, (addr, stats) in enumerate(whales_7d, 1):
                message += format_whale_entry(i, addr, stats, compact=True) + "\n"
        else:
            message += "_No whale activity in last 7 days_\n"

        message += "\n"

        # 30 Days
        message += "📆 **Last 30 Days**\n"
        if whales_30d:
            for i, (addr, stats) in enumerate(whales_30d, 1):
                message += format_whale_entry(i, addr, stats, compact=True) + "\n"
        else:
            message += "_No whale activity in last 30 days_\n"

        message += f"\n_Threshold: $500+ | Total trades analyzed: {len(trades)}_"

        await update.message.reply_text(
            message,
            parse_mode="Markdown"
        )

    except Exception as e:
        logger.error(f"Error fetching whale leaderboard: {e}")
        await update.message.reply_text(
            "⚠️ Error fetching leaderboard. Please try again later."
        )

