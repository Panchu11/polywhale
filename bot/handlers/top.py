"""
/top command handler - Show whale leaderboard with time filters
"""
from telegram import Update
from telegram.ext import ContextTypes
from loguru import logger
from datetime import datetime, timedelta
from config.settings import settings


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


def aggregate_whales(trades, threshold: int = settings.WHALE_THRESHOLD):
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
        # Use Markdown inline link format for Telegram
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
        # Optional window argument: /top [24h|7d|30d|all]; default 24h
        text = (update.message.text or "").strip().lower()
        parts = text.split()
        arg = parts[1] if len(parts) > 1 else "24h"

        now = datetime.now()
        label = "last 24h"
        if arg in ("24h", "1d", "day"):
            since = now - timedelta(hours=24)
            label = "last 24h"
        elif arg in ("7d", "week", "1w"):
            since = now - timedelta(days=7)
            label = "last 7d"
        elif arg in ("30d", "month", "1m"):
            since = now - timedelta(days=30)
            label = "last 30d"
        elif arg in ("all", "alltime", "lifetime"):
            # Effectively all-time (DB contains last N days)
            since = datetime(1970, 1, 1)
            label = "all time"
        else:
            # Fallback
            since = now - timedelta(hours=24)
            label = "last 24h"

        rows = await db.get_top_whales_since(since, limit=10)
        total_analyzed = await db.count_whale_trades_since(since)

        message = f"🏆 **Top 10 Whales — {label}**\n\n"
        if rows:
            for i, row in enumerate(rows, 1):
                stats = {
                    'total_volume': row['total_volume'],
                    'trade_count': row['trade_count'],
                    'largest_trade': row['largest_trade'],
                    'trader_name': '',
                    'trader_pseudonym': '',
                    'profile_url': f"https://polymarket.com/profile/{row['address']}"
                }
                message += format_whale_entry(i, row['address'], stats, compact=True) + "\n"
        else:
            message += f"_No whale activity in {label}_\n"

        message += f"\n_Threshold: ${settings.WHALE_THRESHOLD}+ | Whale trades analyzed: {total_analyzed} ({label})_"

        await update.message.reply_text(
            message,
            parse_mode="Markdown"
        )

    except Exception as e:
        logger.error(f"Error fetching whale leaderboard: {e}")
        await update.message.reply_text(
            "⚠️ Error fetching leaderboard. Please try again later."
        )

