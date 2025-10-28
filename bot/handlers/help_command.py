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
`/whales` - Recent whale trades ($500+)
`/whale <address>` - View whale profile
`/track <address>` - Track a whale
`/untrack <address>` - Stop tracking
`/mywhales` - Your tracked whales
`/top` - Whale leaderboard

**📊 Markets**
`/markets` - Top active markets

**⚙️ Settings**
`/settings` - View your settings
`/alerts on/off` - Toggle notifications
`/threshold <amount>` - Set min trade size (default: $500)

**ℹ️ Info**
`/help` - Show this help message
`/about` - About PolyWhale

**💡 Tips:**
• Set your whale threshold to filter alerts
• Track whales to get notified of their trades
• All markets and traders are clickable links to Polymarket
• Default threshold is $500 - adjust with /threshold

**Whale Tiers:**
🐟 $500+ | 🐬 $1,000+ | 🐳 $5,000+ | 🐋 $10,000+

Need help? Contact @Zun2025
"""
    
    await update.message.reply_text(
        help_text,
        parse_mode="Markdown"
    )

