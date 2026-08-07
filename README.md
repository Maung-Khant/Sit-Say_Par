# Sit-Say Par

**An Explainable Myanmar Phishing URL Risk Assessment Platform**

[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.95.0-009688.svg?logo=fastapi)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

Sit-Say Par is a production-inspired cybersecurity platform designed for Myanmar users. It analyzes URLs for phishing threats and provides **explainable risk assessments in Burmese**, with special awareness of local brands (KBZ, Wave Money, CB Bank, etc.).

---

## 🚀 Features

- **Explainable Results** – Each risk level comes with clear Burmese-language reasons and recommendations.
- **Myanmar-First Intelligence** – Detects impersonation of 100+ local brands and organizations.
- **Multi-Client Access** – Web UI, REST API, Telegram Bot (Viber and browser extension planned).
- **Hybrid Detection Engine** – Combines a rule engine (80%) with a Decision Tree ML model (20%) for balanced accuracy and transparency.
- **History & Logging** – SQLite-backed analysis logs for review.
- **Clean Architecture** – Modular monolith following domain-driven design, easy to extend and test.

---

## 🛠️ Tech Stack

| Category        | Technology |
|----------------|------------|
| Backend         | Python 3.11, FastAPI |
| Database        | SQLite (with SQLAlchemy) |
| Machine Learning | scikit-learn (Decision Tree) |
| Frontend        | Jinja2 templates, HTML/CSS/JavaScript |
| Bot Framework   | python-telegram-bot |
| Testing         | Pytest |
| Deployment      | Render, Railway, or any ASGI server |

---

## 📦 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Maung-Khant/sit-say-par.git
   cd sit-say-par

    Create and activate a virtual environment
    bash

    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate

    Install dependencies
    bash

    pip install -r requirements.txt

    Train the ML model (optional but recommended)
    bash

    python ml/generate_dataset.py
    python ml/train_model.py

    Run the application
    bash

    uvicorn backend.api.main:app --reload

    Open http://localhost:8000 to access the web UI.
    API docs are at http://localhost:8000/docs.

🤖 Telegram Bot

    Create a bot via @BotFather and get the token.

    Copy .env.example to .env and set TELEGRAM_BOT_TOKEN=your_token.

    Run the bot:
    bash

    python backend/adapters/telegram/bot.py

📁 Project Structure
text

Sit-Say_Par/
├── backend/
│   ├── core/            # Domain entities (URL, RiskResult)
│   ├── use_cases/       # Feature extraction, rule engine, risk scoring
│   ├── infrastructure/  # Database, ML predictor
│   ├── api/             # FastAPI application, templates
│   └── adapters/        # Telegram bot, (future: Viber, browser ext.)
├── tests/               # Unit and integration tests
├── ml/                  # Model training scripts and datasets
├── docs/                # Documentation
├── .env.example
├── requirements.txt
└── README.md

🧪 Running Tests
bash

pytest tests/ -v

📄 License

This project is licensed under the MIT License. See LICENSE for details.
🙏 Acknowledgements

    Myanmar brand data collected from public sources.

    Phishing dataset inspired by open-source threat intelligence feeds.