import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes
)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Configuration - REPLACE THESE WITH YOUR LINKS
CHANNEL_LINK = "https://t.me/your_channel"
GROUP_LINK = "https://t.me/your_group"
TWITTER_LINK = "https://twitter.com/your_twitter"

# Use token from environment or hardcoded fallback
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "7442229206:AAE2x7pfMt0YG340BOOkwBLi-iLjenvBKDI")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    keyboard = [
        [InlineKeyboardButton("✅ I've Joined Everything", callback_data="joined")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    message = (
        f"👋 Hey {user.mention_markdown_v2()}! Welcome to our Airdrop Bot!\n\n"
        "📋 To participate:\n"
        f"1️⃣ Join our [Channel]({CHANNEL_LINK})\n"
        f"2️⃣ Join our [Group]({GROUP_LINK})\n"
        f"3️⃣ Follow our [Twitter]({TWITTER_LINK})\n\n"
        "After joining, click the button below!"
    )
    
    await update.message.reply_markdown_v2(
        message,
        reply_markup=reply_markup
    )

async def handle_join_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("🚀 Awesome! Now send me your Solana wallet address:")
    context.user_data["awaiting_wallet"] = True

async def handle_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.user_data.get("awaiting_wallet"):
        return
    
    wallet_address = update.message.text
    context.user_data["awaiting_wallet"] = False
    
    # Fake transaction URL
    fake_tx_url = "https://solscan.io/tx/5xWzJyhVgLJQy9C7U7bV7E2vD2eR5tY8uH0aK3jFhG7dS4fGhD8"
    
    message = (
        "🎉 Congratulations!\n\n"
        f"10 SOL has been sent to your wallet:\n`{wallet_address}`\n\n"
        f"🔗 [View Transaction]({fake_tx_url})\n\n"
        "Note: This is a test environment. No real SOL was sent."
    )
    
    await update.message.reply_markdown_v2(message)

def main() -> None:
    # Create Application
    application = Application.builder().token(BOT_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(handle_join_button, pattern="^joined$"))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_wallet))

    # Deployment configuration
    if os.getenv("RENDER"):
        # Running on Render
        port = int(os.environ.get("PORT", 8443))
        webhook_url = os.getenv("RENDER_EXTERNAL_URL")
        
        if not webhook_url:
            logger.error("RENDER_EXTERNAL_URL environment variable not set")
            return
            
        application.run_webhook(
            listen="0.0.0.0",
            port=port,
            webhook_url=f"{webhook_url}/webhook",
            cert=None
        )
    else:
        # Running locally
        logger.info("Starting bot in polling mode...")
        application.run_polling()

if __name__ == "__main__":
    main()
