# backend/api/main.py
import os
import logging
from pathlib import Path

from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, HttpUrl
from sqlalchemy.orm import Session
from jinja2 import Environment, FileSystemLoader
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from slowapi import Limiter
from slowapi.util import get_remote_address

from backend.use_cases.analyze_url import AnalyzeURLUseCase
from backend.infrastructure.database import init_db, get_db
from backend.infrastructure.models import AnalysisLog
from backend.use_cases.explanation_generator import generate_burmese_explanation, get_detection_confidence

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Sit-Say_Par API", version="0.2.0")

# Rate limiter
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

# Jinja2 setup
BASE_DIR = Path(__file__).resolve().parent
template_env = Environment(loader=FileSystemLoader(os.path.join(BASE_DIR, "templates")))

def render_template(template_name: str, context: dict) -> HTMLResponse:
    template = template_env.get_template(template_name)
    return HTMLResponse(content=template.render(context))

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
    detection_confidence: str | None = None

# --- JSON API Endpoint ---
@app.post("/analyze", response_model=AnalyzeResponse)
@limiter.limit("60/minute")
def analyze_url(request: Request, analyze_req: AnalyzeRequest, db: Session = Depends(get_db)):
    try:
        use_case = AnalyzeURLUseCase()
        result = use_case.execute(str(analyze_req.url))

        result["detection_confidence"] = get_detection_confidence(result)

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
@limiter.limit("60/minute")
async def analyze_web(request: Request, url: str = Form(...), db: Session = Depends(get_db)):
    try:
        use_case = AnalyzeURLUseCase()
        result = use_case.execute(url)

        log = AnalysisLog(
            url=result["url"],
            risk_score=result["risk_score"],
            risk_level=result["risk_level"],
            rules_triggered=result["total_rules_triggered"],
            explanation=result["explanation"]
        )
        db.add(log)
        db.commit()

        confidence = get_detection_confidence(result)

        return render_template("result.html", {
            "request": request,
            "url": result["url"],
            "risk_score": result["risk_score"],
            "risk_level": result["risk_level"],
            "explanation": result["explanation"],
            "detection_confidence": confidence,
        })

    except ValueError as e:
        return render_template("index.html", {
            "request": request,
            "error": "URL ဖြည့်သွင်းမှု မမှန်ကန်ပါ။ ဥပမာ - http://example.com or https://example.com "
        })

@app.get("/history", response_class=HTMLResponse)
async def history(request: Request, db: Session = Depends(get_db)):
    logs = db.query(AnalysisLog).order_by(AnalysisLog.created_at.desc()).limit(20).all()
    return render_template("history.html", {"request": request, "logs": logs})

# ===================== Telegram Bot Integration =====================
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot_app = None

async def bot_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "မင်္ဂလာပါ၊ Sit-Say Par Bot မှကြိုဆိုပါတယ်။\n"
        "သံသယဖြစ်ဖွယ် URL (သို့) စာသားကို ပို့ပေးပါ။\n"
        "အကူအညီလိုအပ်ပါက /help ကိုနှိပ်ပါ။\n"
        "📧 sitsaypar@gmail.com"
    )

async def bot_handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    if not user_text:
        return
    try:
        use_case = AnalyzeURLUseCase()
        result = use_case.execute(user_text)

        confidence = get_detection_confidence(result)
        confidence_map = {"High": "မြင့်မား", "Medium": "အလယ်အလတ်", "Low": "နည်းပါး"}

        response = (
            f"🔗 *URL:* {result['url']}\n"
            f"⚠️ *အန္တရာယ်အဆင့်:* {result['risk_level']} ({result['risk_score']}/100)\n"
            f"📊 *စနစ်၏ စစ်ဆေးမှု သေချာမှု:* {confidence_map[confidence]}\n"
            f"{result['explanation']}"
        )
        await update.message.reply_text(response, parse_mode='Markdown')
    except Exception as e:
        logger.error(f"Bot handler error: {e}")
        await update.message.reply_text("ဝမ်းနည်းပါတယ်၊ စစ်ဆေးမှုမအောင်မြင်ပါ။")

async def bot_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Sit-Say Par Bot အသုံးပြုနည်း\n\n"
        "• URL သို့မဟုတ် စာသားကို ပို့ပါ။\n"
        "• ရလဒ်ကို ချက်ချင်း ရရှိပါမည်။\n\n"
        "အကူအညီလိုအပ်ပါက:\n"
        "📧 sitsaypar@gmail.com\n"
        "သို့မဟုတ် @SitSayParSupport (Telegram) သို့ ဆက်သွယ်ပါ။"
    )

@app.post("/telegram-webhook")
async def telegram_webhook(update: dict):
    if bot_app:
        await bot_app.process_update(Update.de_json(update, bot_app.bot))
    return {"status": "ok"}

@app.on_event("startup")
async def on_startup():
    global bot_app
    init_db()
    logger.info("Database initialized.")

    if BOT_TOKEN:
        try:
            bot_app = ApplicationBuilder().token(BOT_TOKEN).build()
            await bot_app.initialize()
            # Register command handlers BEFORE message handler
            bot_app.add_handler(CommandHandler("start", bot_start))
            bot_app.add_handler(CommandHandler("help", bot_help))
            bot_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, bot_handle_message))
            logger.info("Bot initialized and handlers registered.")

            webhook_url = "https://sit-say-par.onrender.com/telegram-webhook"
            await bot_app.bot.set_webhook(webhook_url)
            logger.info(f"Telegram webhook set to {webhook_url}")
        except Exception as e:
            logger.error(f"Failed to initialize bot: {e}")
    else:
        logger.warning("TELEGRAM_BOT_TOKEN not set. Bot disabled.")