"""
/threshold command handler - Set whale threshold
"""
from telegram import Update
from telegram.ext import ContextTypes
from loguru import logger


async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /threshold <amount> command"""
    user = update.effective_user
    
    # Check if amount was provided
    if not context.args:
        await update.message.reply_text(
            "⚠️ Please provide a threshold amount.\n\n"
            "Usage: `/threshold <amount>`\n"
            "Example: `/threshold 25000`\n\n"
            "This sets the minimum trade size for alerts.",
            parse_mode="Markdown"
        )
        return
    
    try:
        amount = int(context.args[0].replace(',', '').replace('$', ''))
        
        if amount < 500:
            await update.message.reply_text(
                "⚠️ Threshold must be at least $500.\n\n"
                "Recommended: $1,000+ for whale tracking",
                parse_mode="Markdown"
            )
            return
        
        if amount > 1000000:
            await update.message.reply_text(
                "⚠️ Threshold too high! Maximum is $1,000,000.\n\n"
                "You might miss important whale activity.",
                parse_mode="Markdown"
            )
            return
        
    except ValueError:
        await update.message.reply_text(
            "⚠️ Invalid amount. Please provide a number.\n\n"
            "Example: `/threshold 25000`",
            parse_mode="Markdown"
        )
        return
    
    logger.info(f"User {user.id} setting threshold to ${amount:,}")
    
    # Get database from context
    if "db" not in context.bot_data:
        await update.message.reply_text("⚠️ Database not available. Please try again later.")
        return
    
    db = context.bot_data["db"]
    
    try:
        # Update user threshold
        await db.update_user_settings(user.id, whale_threshold=amount)
        
        # Determine whale tier with new thresholds
        if amount >= 10000:
            tier = "🐋 Mega Whale"
        elif amount >= 5000:
            tier = "🐳 Large Whale"
        elif amount >= 1000:
            tier = "🐬 Medium Whale"
        else:
            tier = "🐟 Small Whale"
        
        await update.message.reply_text(
            f"✅ **Threshold Updated!**\n\n"
            f"New threshold: **${amount:,}**\n"
            f"Tier: {tier}\n\n"
            f"You'll only receive alerts for trades above this amount.\n\n"
            f"Use `/settings` to view all your settings.",
            parse_mode="Markdown"
        )
        
        logger.info(f"User {user.id} threshold set to ${amount:,}")
        
    except Exception as e:
        logger.error(f"Error setting threshold: {e}")
        await update.message.reply_text(
            "⚠️ Error updating threshold. Please try again later."
        )

