"""
/alerts command handler - Manage alert settings
"""
from telegram import Update
from telegram.ext import ContextTypes
from loguru import logger


async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /alerts command"""
    user = update.effective_user
    
    # Get database from context
    if "db" not in context.bot_data:
        await update.message.reply_text("⚠️ Database not available. Please try again later.")
        return
    
    db = context.bot_data["db"]
    
    # Check if on/off argument provided
    if context.args:
        action = context.args[0].lower()
        
        try:
            if action == "on":
                await db.update_user_settings(user.id, notifications_enabled=True)
                await update.message.reply_text(
                    "✅ **Alerts Enabled!**\n\n"
                    "You'll now receive notifications for:\n"
                    "• Whale trades above your threshold\n"
                    "• Trades from your tracked whales\n\n"
                    "Use `/alerts off` to disable",
                    parse_mode="Markdown"
                )
                logger.info(f"User {user.id} enabled alerts")
                
            elif action == "off":
                await db.update_user_settings(user.id, notifications_enabled=False)
                await update.message.reply_text(
                    "🔕 **Alerts Disabled!**\n\n"
                    "You won't receive any notifications.\n\n"
                    "Use `/alerts on` to re-enable",
                    parse_mode="Markdown"
                )
                logger.info(f"User {user.id} disabled alerts")
                
            else:
                await update.message.reply_text(
                    "⚠️ Invalid option. Use:\n"
                    "• `/alerts on` - Enable notifications\n"
                    "• `/alerts off` - Disable notifications",
                    parse_mode="Markdown"
                )
                
        except Exception as e:
            logger.error(f"Error updating alert settings: {e}")
            await update.message.reply_text(
                "⚠️ Error updating settings. Please try again later."
            )
    else:
        # Show current alert settings
        try:
            user_data = await db.get_user(user.id)
            settings = user_data.get('settings', {}) if user_data else {}
            notifications_enabled = settings.get('notifications_enabled', True)
            
            message = f"""
🔔 **Alert Settings**

**Status:** {'✅ Enabled' if notifications_enabled else '❌ Disabled'}

**Commands:**
• `/alerts on` - Enable notifications
• `/alerts off` - Disable notifications

**What you'll receive:**
• Whale trades above your threshold
• Trades from your tracked whales
• Market updates

Use `/settings` to configure more options.
"""
            
            await update.message.reply_text(
                message,
                parse_mode="Markdown"
            )
            
        except Exception as e:
            logger.error(f"Error fetching alert settings: {e}")
            await update.message.reply_text(
                "⚠️ Error fetching settings. Please try again later."
            )

