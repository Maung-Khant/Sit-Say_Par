# tests/test_api.py
from fastapi.testclient import TestClient

from backend.api.main import app

client = TestClient(app)


def test_home_page():
    response = client.get("/")
    assert response.status_code == 200
    assert "Sit-Say Par" in response.text


def test_analyze_endpoint_valid_url():
    response = client.post("/analyze", json={"url": "https://www.wikipedia.org"})
    assert response.status_code == 200
    data = response.json()
    assert data["risk_level"] == "Low"
    assert "explanation" in data


def test_analyze_endpoint_phishing_url():
    response = client.post(
        "/analyze", json={"url": "http://login.paypal.com.verify.tk/secure/update.php"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["risk_score"] > 30
    assert data["total_rules_triggered"] >= 2


def test_analyze_endpoint_invalid_url():
    response = client.post("/analyze", json={"url": "not-a-valid-url"})
    assert response.status_code == 422  # Pydantic validation error


def test_analyze_web_valid_url():
    response = client.post("/analyze-web", data={"url": "https://www.wikipedia.org"})
    assert response.status_code == 200
    assert "စစ်ဆေးမှုရလဒ်" in response.text
    assert "နည်းပါးသည်" in response.text


def test_analyze_web_phishing_url():
    response = client.post(
        "/analyze-web", data={"url": "http://kbzpay.workers.dev/login"}
    )
    assert response.status_code == 200
    # Should indicate high risk and brand impersonation
    assert "မြင့်မားသည်" in response.text or "အလွန်မြင့်မားသည်" in response.text


def test_history_page():
    response = client.get("/history")
    assert response.status_code == 200
    assert "စစ်ဆေးမှုမှတ်တမ်း" in response.text
