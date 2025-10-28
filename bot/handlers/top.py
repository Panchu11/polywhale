"""
/top command handler - Show whale leaderboard
"""
from telegram import Update
from telegram.ext import ContextTypes
from loguru import logger


async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /top command - Show top whales by volume"""
    user = update.effective_user
    logger.info(f"User {user.id} requested whale leaderboard")
    
    # Get database from context
    if "db" not in context.bot_data:
        await update.message.reply_text("⚠️ Database not available. Please try again later.")
        return
    
    db = context.bot_data["db"]
    
    try:
        # Fetch top whales from Polymarket API
        from bot.services.polymarket_api import PolymarketAPI
        api = PolymarketAPI()
        
        # Fetch recent trades and aggregate by trader
        trades = await api.fetch_recent_trades(limit=200)
        await api.close()
        
        if not trades:
            await update.message.reply_text(
                "📊 No whale data available yet.\n\n"
                "Check back soon!"
            )
            return
        
        # Aggregate trades by trader
        whale_stats = {}
        for trade in trades:
            if trade.size >= 10000:  # Only whales
                addr = trade.trader_address
                if addr not in whale_stats:
                    whale_stats[addr] = {
                        'total_volume': 0,
                        'trade_count': 0,
                        'largest_trade': 0
                    }
                whale_stats[addr]['total_volume'] += trade.size
                whale_stats[addr]['trade_count'] += 1
                whale_stats[addr]['largest_trade'] = max(whale_stats[addr]['largest_trade'], trade.size)
        
        # Sort by total volume
        top_whales = sorted(whale_stats.items(), key=lambda x: x[1]['total_volume'], reverse=True)[:10]
        
        if not top_whales:
            await update.message.reply_text(
                "🐋 No whale activity detected recently.\n\n"
                "Whales might be sleeping! 😴"
            )
            return
        
        # Format leaderboard message
        message = "🏆 **Top Whales Leaderboard**\n\n"
        
        for i, (address, stats) in enumerate(top_whales, 1):
            # Determine whale tier
            if stats['total_volume'] >= 100000:
                emoji = "🐋"
            elif stats['total_volume'] >= 50000:
                emoji = "🐳"
            else:
                emoji = "🐬"
            
            short_addr = f"{address[:6]}...{address[-4:]}"
            message += f"{i}. {emoji} `{short_addr}`\n"
            message += f"   💰 ${stats['total_volume']:,.0f} total volume\n"
            message += f"   📊 {stats['trade_count']} trades\n"
            message += f"   🎯 ${stats['largest_trade']:,.0f} largest\n"
            message += "\n"
        
        message += "_Use /whale <address> to view full profile_"
        
        await update.message.reply_text(
            message,
            parse_mode="Markdown"
        )
        
    except Exception as e:
        logger.error(f"Error fetching whale leaderboard: {e}")
        await update.message.reply_text(
            "⚠️ Error fetching leaderboard. Please try again later."
        )

