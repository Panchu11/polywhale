"""
/start command handler
"""
from telegram import Update
from telegram.ext import ContextTypes
from loguru import logger


async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start command"""
    user = update.effective_user
    logger.info(f"User {user.id} ({user.username}) started the bot")
    
    welcome_message = f"""
🐋 **Welcome to PolyWhale!**

Hey {user.first_name}! 👋

I'm your personal whale tracker for Polymarket. I'll help you track the smartest money in prediction markets and never miss a whale move again.

**What I can do:**
🔔 Real-time whale alerts (trades >$10k)
📊 Top whale leaderboard
🔍 Market scanner & discovery
💰 Smart money flow analysis
📌 Track your favorite whales
⚙️ Custom alert settings

**Quick Start:**
• `/whales` - See recent whale trades
• `/markets` - Discover hot markets
• `/top` - View whale leaderboard
• `/help` - See all commands

**Get Started:**
Use `/settings` to customize your alerts and preferences.

Let's track some whales! 🚀
"""
    
    await update.message.reply_text(
        welcome_message,
        parse_mode="Markdown"
    )
    
    # Register user in database
    if "db" in context.bot_data:
        db = context.bot_data["db"]
        try:
            await db.create_user(
                user_id=user.id,
                username=user.username,
                first_name=user.first_name
            )
            logger.info(f"User {user.id} registered in database")
        except Exception as e:
            logger.error(f"Failed to register user {user.id}: {e}")

