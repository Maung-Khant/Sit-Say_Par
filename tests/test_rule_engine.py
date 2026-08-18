import pytest

from backend.core.url import URL
from backend.use_cases.feature_extractor import extract_features
from backend.use_cases.rule_engine import run_rule_engine


def test_rule_engine_normal_url():
    url = URL("https://www.google.com")
    features = extract_features(url)
    matches = run_rule_engine(features)
    assert len(matches) == 0


def test_rule_engine_phishing_url():
    url = URL("http://login.paypal.com.verify.tk/secure/update.php")
    features = extract_features(url)
    matches = run_rule_engine(features)
    assert len(matches) >= 2


def test_rule_engine_brand_impersonation():
    url = URL("http://kbzpay.workers.dev/login")
    features = extract_features(url)
    matches = run_rule_engine(features)
    assert any(m["rule_name"] == "_rule_brand_impersonation" for m in matches)


def test_rule_engine_official_kbz():
    url = URL("https://www.kbzbank.com")
    features = extract_features(url)
    matches = run_rule_engine(features)
    assert not any(m["rule_name"] == "_rule_brand_impersonation" for m in matches)


def test_rule_engine_ip_address():
    url = URL("http://192.168.1.1/admin")
    features = extract_features(url)
    matches = run_rule_engine(features)
    assert any(m["rule_name"] == "_rule_ip_address" for m in matches)
