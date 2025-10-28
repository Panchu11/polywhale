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
        # Fetch recent trades by this whale from Polymarket API
        from bot.services.polymarket_api import PolymarketAPI
        api = PolymarketAPI()

        # Fetch more trades to find this whale
        all_trades = await api.fetch_recent_trades(limit=500)
        whale_trades = [t for t in all_trades if t.trader_address.lower() == address.lower()]

        await api.close()

        if not whale_trades:
            await update.message.reply_text(
                f"🐋 No recent activity found for `{address[:6]}...{address[-4:]}`\n\n"
                "This address might not have made any trades recently.",
                parse_mode="Markdown"
            )
            return

        # Calculate stats
        total_volume = sum(t.size for t in whale_trades)
        trade_count = len(whale_trades)

        # Determine whale tier with lower thresholds
        if total_volume >= 10000:
            emoji = "🐋"
            tier = "Mega Whale"
        elif total_volume >= 5000:
            emoji = "🐳"
            tier = "Large Whale"
        elif total_volume >= 1000:
            emoji = "🐬"
            tier = "Medium Whale"
        else:
            emoji = "🐟"
            tier = "Small Trader"

        # Get trader info from first trade
        first_trade = whale_trades[0]
        trader_name = first_trade.get_trader_display_name()
        profile_url = first_trade.get_profile_url()

        # Format whale profile message
        message = f"{emoji} **Whale Profile**\n\n"
        message += f"Trader: [{trader_name}]({profile_url})\n"
        message += f"Tier: {tier}\n\n"

        message += f"📊 **Recent Activity**\n"
        message += f"Total Volume: ${total_volume:,.0f}\n"
        message += f"Total Trades: {trade_count}\n"

        if whale_trades:
            latest = whale_trades[0]
            message += f"Last Trade: {latest.timestamp.strftime('%Y-%m-%d %H:%M')}\n"
            message += f"Last Market: [{latest.market_name[:40]}...]({latest.get_market_url()})\n"

        # Show recent trades
        message += f"\n🔥 **Recent Trades:**\n"
        for trade in whale_trades[:5]:
            message += f"• ${trade.size:,.0f} - {trade.side} {trade.outcome}\n"

        message += f"\n_Use /track {address} to follow this whale_"

        await update.message.reply_text(
            message,
            parse_mode="Markdown"
        )
        
    except Exception as e:
        logger.error(f"Error fetching whale profile: {e}")
        await update.message.reply_text(
            "⚠️ Error fetching whale profile. Please try again later."
        )

