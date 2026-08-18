# tests/test_ml_predictor.py
from backend.core.url import URL
from backend.infrastructure.ml_predictor import ml_predictor
from backend.use_cases.feature_extractor import extract_features


def test_ml_predictor_loads():
    # Model file should exist after training
    assert ml_predictor.model is not None


def test_ml_predictor_phishing():
    url = URL("http://login.paypal.com.verify.tk/secure/update.php")
    features = extract_features(url)
    proba = ml_predictor.predict_proba(features)
    assert proba is not None
    assert proba > 0.5


def test_ml_predictor_legitimate():
    url = URL("https://www.wikipedia.org")
    features = extract_features(url)
    proba = ml_predictor.predict_proba(features)
    assert proba is not None
    assert proba < 0.5
