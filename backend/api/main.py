# backend/api/main.py
import os
from pathlib import Path

from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, HttpUrl
from sqlalchemy.orm import Session
from jinja2 import Environment, FileSystemLoader

from backend.use_cases.analyze_url import AnalyzeURLUseCase
from backend.infrastructure.database import init_db, get_db
from backend.infrastructure.models import AnalysisLog

app = FastAPI(title="Sit-Say_Par API", version="0.2.0")

# Manual Jinja2 setup (avoids Starlette's internal Jinja2Templates cache bug)
BASE_DIR = Path(__file__).resolve().parent
template_env = Environment(loader=FileSystemLoader(os.path.join(BASE_DIR, "templates")))

def render_template(template_name: str, context: dict) -> HTMLResponse:
    template = template_env.get_template(template_name)
    return HTMLResponse(content=template.render(context))

@app.on_event("startup")
def on_startup():
    init_db()

# --- Request/Response Schemas ---
class AnalyzeRequest(BaseModel):
    url: HttpUrl

class AnalyzeResponse(BaseModel):
    url: str
    risk_score: int
    risk_level: str
    total_rules_triggered: int
    matched_rules: list
    features: dict
    explanation: str
    ml_score: int | None = None
    rule_score: int | None = None
# --- JSON API Endpoint ---
@app.post("/analyze", response_model=AnalyzeResponse)
def analyze_url(request: AnalyzeRequest, db: Session = Depends(get_db)):
    try:
        use_case = AnalyzeURLUseCase()
        result = use_case.execute(str(request.url))

        # Save to database
        log = AnalysisLog(
            url=result["url"],
            risk_score=result["risk_score"],
            risk_level=result["risk_level"],
            rules_triggered=result["total_rules_triggered"],
            explanation=result["explanation"]
        )
        db.add(log)
        db.commit()

        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# --- Web UI Endpoints ---
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return render_template("index.html", {"request": request})

@app.post("/analyze-web", response_class=HTMLResponse)
async def analyze_web(request: Request, url: str = Form(...), db: Session = Depends(get_db)):
    try:
        use_case = AnalyzeURLUseCase()
        result = use_case.execute(url)

        # Save to database
        log = AnalysisLog(
            url=result["url"],
            risk_score=result["risk_score"],
            risk_level=result["risk_level"],
            rules_triggered=result["total_rules_triggered"],
            explanation=result["explanation"]
        )
        db.add(log)
        db.commit()

        return render_template("result.html", {
            "request": request,
            "url": result["url"],
            "risk_score": result["risk_score"],
            "risk_level": result["risk_level"],
            "explanation": result["explanation"],
        })
    except ValueError as e:
        return render_template("index.html", {
            "request": request,
            "error": f"မမှန်ကန်သော URL - {str(e)}"
        })

@app.get("/history", response_class=HTMLResponse)
async def history(request: Request, db: Session = Depends(get_db)):
    # Get last 20 logs ordered by most recent
    logs = db.query(AnalysisLog).order_by(AnalysisLog.created_at.desc()).limit(20).all()
    return render_template("history.html", {"request": request, "logs": logs})

# Telegram Bot Webhook Integration
import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot_app = None

if BOT_TOKEN:
    # Initialize bot application
    bot_app = ApplicationBuilder().token(BOT_TOKEN).build()
    use_case = AnalyzeURLUseCase()

    async def bot_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            "မင်္ဂလာပါ၊ Sit-Say Par Bot မှကြိုဆိုပါတယ်။\n"
            "သံသယဖြစ်ဖွယ် URL (သို့) စာသားကို ပို့ပေးပါ။"
        )

    async def bot_handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_text = update.message.text
        if not user_text:
            return
        try:
            result = use_case.execute(user_text)
            response = (
                f"🔗 *URL:* {result['url']}\n"
                f"⚠️ *အန္တရာယ်အဆင့်:* {result['risk_level']} ({result['risk_score']}/100)\n"
                f"{result['explanation']}"
            )
            await update.message.reply_text(response, parse_mode='Markdown')
        except Exception as e:
            await update.message.reply_text("ဝမ်းနည်းပါတယ်၊ စစ်ဆေးမှုမအောင်မြင်ပါ။")

    # Add handlers
    bot_app.add_handler(CommandHandler("start", bot_start))
    bot_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, bot_handle_message))

    @app.post("/telegram-webhook")
    async def telegram_webhook(update: dict):
        """Process incoming Telegram updates using the bot application."""
        if bot_app:
            # Use process_update to handle the update synchronously
            await bot_app.process_update(Update.de_json(update, bot_app.bot))
        return {"status": "ok"}

    @app.on_event("startup")
    async def set_telegram_webhook():
        """Initialize bot and set webhook URL on startup."""
        if not BOT_TOKEN:
            logging.warning("TELEGRAM_BOT_TOKEN not set. Bot disabled.")
            return
        await bot_app.initialize()  # Important: prepare bot for processing
        webhook_url = "https://sit-say-par.onrender.com/telegram-webhook"  # ← Replace with your real URL
        try:
            await bot_app.bot.set_webhook(webhook_url)
            logging.info(f"Telegram webhook set to {webhook_url}")
        except Exception as e:
            logging.error(f"Failed to set webhook: {e}")

else:
    logging.warning("TELEGRAM_BOT_TOKEN environment variable missing.")