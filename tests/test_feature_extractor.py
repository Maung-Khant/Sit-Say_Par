# tests/test_feature_extractor.py
from backend.core.url import URL
from backend.use_cases.feature_extractor import extract_features

def test_extract_features_normal_url():
    url = URL("https://www.example.com/page")
    features = extract_features(url)
    assert features['url_length'] > 0
    assert features['domain_dot_count'] == 2
    assert features['is_ip'] == 0
    assert features['has_at_symbol'] == 0
    assert features['suspicious_keyword_count'] == 0
    assert features['suspicious_tld'] == 0
    assert features['is_shortener'] == 0

def test_extract_features_phishing_url():
    url = URL("http://login.paypal.com.verify.tk/secure/update.php")
    features = extract_features(url)
    assert features['suspicious_keyword_count'] >= 3
    assert features['suspicious_tld'] == 1
    assert features['domain_dot_count'] >= 4

def test_extract_features_ip_url():
    url = URL("http://192.168.1.1/admin")
    features = extract_features(url)
    assert features['is_ip'] == 1

def test_extract_features_shortener():
    url = URL("https://bit.ly/abc123")
    features = extract_features(url)
    assert features['is_shortener'] == 1

def test_extract_features_brand_kbz_impersonation():
    url = URL("http://kbzpay.workers.dev/login")
    features = extract_features(url)
    assert 'kbz' in features['brands_detected']
    assert features['brand_count'] >= 1

def test_extract_features_brand_official():
    url = URL("https://www.kbzbank.com")
    features = extract_features(url)
    # Official KBZ domain still detected as brand (but rule engine will filter it out)
    assert 'kbz' in features['brands_detected']
