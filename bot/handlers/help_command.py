"""
/help command handler
"""
from telegram import Update
from telegram.ext import ContextTypes


async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /help command"""
    
    help_text = """
📚 **PolyWhale Commands**

**🐋 Whale Tracking**
`/whales` - Recent whale trades (last hour)
`/whale <address>` - View whale profile
`/track <address>` - Track a whale
`/untrack <address>` - Stop tracking
`/mywhales` - Your tracked whales
`/top` - Whale leaderboard

**📊 Markets**
`/markets` - Top markets by whale activity
`/trending` - Hottest markets right now
`/new` - Newly listed markets
`/closing` - Markets ending soon
`/search <query>` - Search markets

**💰 Analytics**
`/flow` - Smart money flow (24h)
`/consensus` - Whale consensus
`/stats` - Your usage statistics

**⚙️ Settings**
`/settings` - Configure preferences
`/alerts` - Manage alert settings
`/threshold <amount>` - Set min trade size
`/categories` - Subscribe to categories
`/quiet <hours>` - Set quiet hours

**ℹ️ Info**
`/help` - Show this help message
`/about` - About PolyWhale

**💡 Tips:**
• Set your whale threshold to filter alerts
• Track whales to get notified of their trades
• Use quiet hours to avoid notifications at night
• Check /flow daily to see where smart money is going

Need help? Contact @Zun2025
"""
    
    await update.message.reply_text(
        help_text,
        parse_mode="Markdown"
    )

