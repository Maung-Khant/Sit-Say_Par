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