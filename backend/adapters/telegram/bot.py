# backend/adapters/telegram/bot.py
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Add project root to sys.path so that we can import backend modules
project_root = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(project_root))

# Load environment variables from .env file
load_dotenv(project_root / ".env")

from backend.use_cases.analyze_url import AnalyzeURLUseCase

# Initialize the use case once
use_case = AnalyzeURLUseCase()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a welcome message when /start is issued."""
    await update.message.reply_text(
        "မင်္ဂလာပါ၊ Sit-Say Par Bot မှကြိုဆိုပါတယ်။\n"
        "သံသယဖြစ်ဖွယ် URL (သို့) စာသားကို ပို့ပေးပါ။ စစ်ဆေးပြီး အန္တရာယ်ရှိမှုကို အသိပေးပါမည်။"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Process any text message, extract URL, analyze, and reply."""
    user_text = update.message.text
    if not user_text:
        return

    try:
        # Analyze the URL (the use case handles mixed text extraction)
        result = use_case.execute(user_text)

        # Build response message
        response = (
            f"🔗 *URL:* {result['url']}\n"
            f"⚠️ *အန္တရာယ်အဆင့်:* {result['risk_level']} ({result['risk_score']}/100)\n"
        )
        if result.get('ml_score') is not None:
            response += f"🤖 *ML ခန့်မှန်းချက်:* {result['ml_score']}/100\n"
        response += f"\n{result['explanation']}"

        await update.message.reply_text(response, parse_mode='Markdown')
    except Exception as e:
        await update.message.reply_text(
            "ဝမ်းနည်းပါတယ်၊ စစ်ဆေးမှုမအောင်မြင်ပါ။ ထည့်သွင်းထားသော စာသားကို ပြန်စစ်ဆေးပါ။"
        )

def main():
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise ValueError("TELEGRAM_BOT_TOKEN environment variable not set. Check your .env file.")

    app = ApplicationBuilder().token(token).build()

    # Register handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()