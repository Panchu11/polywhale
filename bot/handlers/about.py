"""
/about command handler - About PolyWhale
"""
from telegram import Update
from telegram.ext import ContextTypes


async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /about command"""
    
    about_message = """
🐋 **About PolyWhale**

**The Ultimate Polymarket Whale Tracker**

PolyWhale helps you track the smartest money in prediction markets. Never miss a whale move again!

**Features:**
✅ Real-time whale trade alerts
✅ Top whale leaderboard
✅ Market discovery & analysis
✅ Smart money flow tracking
✅ Custom alert settings
✅ Track your favorite whales

**What's a Whale?**
Whales are traders who make large trades (typically $500+). They often have insider knowledge or superior analysis, making them valuable to follow.

**Whale Tiers:**
🐟 Small Whale: $500+
🐬 Medium Whale: $1,000+
🐳 Large Whale: $5,000+
🐋 Mega Whale: $10,000+

**Data Source:**
All data is fetched live from Polymarket's official APIs.

**Website:** https://www.polywhalestracker.xyz/

**Support:** @Zun2025

**Version:** 1.0.0
**Status:** ✅ Live & Tracking

Made with ❤️ for Polymarket traders
"""
    
    await update.message.reply_text(
        about_message,
        parse_mode="Markdown"
    )

