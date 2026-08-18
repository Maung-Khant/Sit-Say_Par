# Sit-Say Par

**An Explainable Myanmar Phishing URL Risk Assessment Platform**

[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.95.0-009688.svg?logo=fastapi)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

Sit-Say Par is a production-inspired cybersecurity platform designed for Myanmar users. It analyzes URLs for phishing threats and provides **explainable risk assessments in Burmese**, with special awareness of local brands (KBZ, Wave Money, CB Bank, AYA Bank, etc.).

---

## 🚀 Features

- **Explainable Results** – Each risk level comes with clear Burmese-language reasons and recommendations.
- **Myanmar-First Intelligence** – Detects impersonation of 100+ local banks, mobile money providers, telecoms, and government bodies.
- **Multi-Client Access** – Web UI, REST API, Telegram Bot, and browser extension.
- **Hybrid Detection Engine** – Combines a rule engine (80%) with a Decision Tree/Random Forest ML model (20%) for balanced accuracy and transparency.
- **Threat Intelligence** – Includes local phishing blacklist, typosquat detection, leetspeak detection, and WHOIS domain age check.
- **History & Logging** – SQLite-backed analysis logs for review.
- **Clean Architecture** – Modular monolith following domain-driven design, easy to extend and test.

---

## 🛠️ Tech Stack

| Category        | Technology |
|----------------|------------|
| Backend         | Python 3.11, FastAPI |
| Database        | SQLite (with SQLAlchemy) |
| Machine Learning | scikit-learn (Decision Tree / Random Forest) |
| Frontend        | Jinja2 templates, HTML/CSS/JavaScript, Tailwind CSS |
| Bot Framework   | python-telegram-bot |
| Browser Extensions | Chrome (Manifest V3), Firefox (Manifest V2) |
| Testing         | Pytest |
| Deployment      | Render (free tier), Uvicorn |

---

## 📦 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Maung-Khant/Sit-Say_Par.git
   cd Sit-Say_Par

2. **Create and activate a virtual environment**
   ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate

3. **Install dependencies**
    ```bash
    pip install -r requirements.txt

4. **Train the ML model (optional but recommended)**
    ```bash
    python ml/generate_dataset.py
    python ml/train_model.py

5. **Run the application**
    ```bash
    uvicorn backend.api.main:app --reload 
    ```
    
    **Open http://localhost:8000 to access the web UI.**

    **API docs are at http://localhost:8000/docs.**

    # 🖥️ Usage
    # Web UI

    1.Go to http://localhost:8000

    2.Paste a URL or text containing a link.

    3.Click စစ်ဆေးမည် (Scan).

    4.View risk level, confidence, Burmese explanation, and recommendations.

    # REST API

    Endpoint: POST /analyze

    Request: {"url": "https://example.com"}

    Response: JSON with risk_score, risk_level, matched_rules, explanation, etc.

    Example:
    ```bash
    curl -X POST http://localhost:8000/analyze \
    -H "Content-Type: application/json" \
    -d '{"url":"https://example.com"}'
    ```

    # Telegram Bot

    1.Set TELEGRAM_BOT_TOKEN in .env or environment variable.

    2.Run webhook integrated in FastAPI (already configured in backend/api/main.py).

    3.Start the server; bot will be active.

    4.Message the bot with any URL or text to get instant analysis.

    # Browser Extension

    - Load browser-extension/chrome as unpacked extension for Chrome.

    - For Firefox, load browser-extension/firefox/manifest.json via about:debugging.

    # 📁 Project Structure

    ```text
    Sit-Say_Par/
    ├── backend/
    │   ├── core/            # Domain entities (URL, RiskResult)
    │   ├── use_cases/       # Feature extraction, rule engine, risk scoring, explanation
    │   ├── infrastructure/ # Database, ML predictor, phishing blacklist
    │   ├── api/             # FastAPI application, templates
    │   └── adapters/        # Telegram bot, (future: Viber)
    ├── tests/               # Unit and integration tests
    ├── ml/                  # Model training scripts and datasets
    ├── browser-extension/   # Chrome & Firefox extensions
    ├── docs/                # Documentation
    ├── .env.example
    ├── requirements.txt
    └── README.md    
    ```
    # 🧪 Testing
    
    Run all tests with:
    bash
    ```
    pytest tests/ -v
    ```
    Currently, there are 38 tests covering core detection logic, API endpoints, and ML predictor.

    # 🚀 Deployment
    
    # Render (Free Tier)

    1. Push code to GitHub.

    2. Create a new Web Service on Render.

    3. Build Command: `pip install -r requirements.txt`

    4. Start Command: `uvicorn backend.api.main:app --host 0.0.0.0 --port $PORT`

    5. Set environment variable `TELEGRAM_BOT_TOKEN` if using bot.
    
    # 📞 Support & Contact
    - Email: sitsaypar@gmail.com

    - GitHub Issues: [Report a problem](https://github.com/Maung-Khant/Sit-Say_Par/issues)

    - Telegram: @SitSayParSupport

    # 📄 License

    This project is licensed under the MIT License. See LICENSE for details.

    # 🙏 Acknowledgements
    * Myanmar brand data collected from public sources and CBM official lists.
    * Phishing datasets from OpenPhish, URLhaus, and self-collected Myanmar scam URLs.