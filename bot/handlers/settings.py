"""
/settings command handler - User settings
"""
from telegram import Update
from telegram.ext import ContextTypes
from loguru import logger


async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /settings command"""
    user = update.effective_user
    logger.info(f"User {user.id} requested settings")
    
    # Get database from context
    if "db" not in context.bot_data:
        await update.message.reply_text("⚠️ Database not available. Please try again later.")
        return
    
    db = context.bot_data["db"]
    
    try:
        # Get user settings
        user_data = await db.get_user(user.id)
        
        if not user_data:
            # Create user first
            await db.create_user(
                telegram_id=user.id,
                username=user.username,
                first_name=user.first_name
            )
            user_data = await db.get_user(user.id)
        
        # Get settings from JSONB column or use defaults
        settings = user_data.get('settings', {}) if user_data else {}
        whale_threshold = settings.get('whale_threshold', 500)  # Changed default to 500
        notifications_enabled = settings.get('notifications_enabled', True)
        
        settings_message = f"""
⚙️ **Your Settings**

**Whale Threshold:** ${whale_threshold:,}
Only trades above this amount will trigger alerts.

**Notifications:** {'✅ Enabled' if notifications_enabled else '❌ Disabled'}

**Available Commands:**
• `/threshold <amount>` - Set minimum trade size
  Example: `/threshold 25000`

• `/alerts on` - Enable notifications
• `/alerts off` - Disable notifications

• `/mywhales` - View tracked whales
• `/track <address>` - Track a whale
• `/untrack <address>` - Untrack a whale

**Current Status:**
• Tracked whales: {len(await db.get_tracked_whales(user.id))}
• Notifications: {'Active' if notifications_enabled else 'Paused'}
"""
        
        await update.message.reply_text(
            settings_message,
            parse_mode="Markdown"
        )
        
    except Exception as e:
        logger.error(f"Error fetching settings: {e}")
        await update.message.reply_text(
            "⚠️ Error fetching settings. Please try again later."
        )

