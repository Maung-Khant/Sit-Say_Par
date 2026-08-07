# Sit-Say Par

> An Explainable Myanmar Phishing URL Risk Assessment Platform

[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE)

Sit-Say Par is a production-inspired phishing URL detection system **built specifically for Myanmar users**.
Unlike generic phishing detectors, it provides **clear, human-readable explanations in Burmese** and specializes in catching **impersonations of local brands** such as KBZ, Wave Money, CB Bank, and various telecom operators.

---

## 🚀 Key Features

- 🧠 **Explainable AI** – Every risk decision is backed by **Burmese-language reasons** (brand impersonation, suspicious keywords, etc.)
- 🇲🇲 **Myanmar-First Threat Intelligence** – Pre-built detection for **100+ local brands** including banks, mobile money, telecoms, and government services
- 📡 **Multi-Client Architecture** – Use the same engine via:
  - 🌐 **Web UI** (mobile-friendly)
  - 🤖 **Telegram Bot** (just forward a suspicious message)
  - 🔌 **REST API** (for developers)
- ⚙️ **Hybrid Detection Engine** – Rule Engine (80%) + Machine Learning (20%) with weighted fusion for maximum reliability
- 🔒 **Privacy-First** – No personal data collected; URL logs are anonymized
- 📊 **Analysis History** – View past scan results with risk scores

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | Python 3.11+, FastAPI |
| Database | SQLite (SQLAlchemy ORM) |
| ML | scikit-learn (Decision Tree) |
| Frontend | Jinja2 + HTML/CSS/JS |
| Bot | python-telegram-bot |
| Testing | Pytest (unit + integration) |
| Deployment | Ready for Render, Railway, etc. |

---

## 🏁 Quick Start

### Prerequisites
- Python 3.11+
- pip

### 1. Clone & Setup Environment
```bash
git clone https://github.com/your-username/Sit-Say_Par.git
cd Sit-Say_Par
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt

