import pytest

from backend.use_cases.analyze_url import AnalyzeURLUseCase, extract_first_url


def test_extract_first_url_with_url():
    assert extract_first_url("https://example.com") == "https://example.com"


def test_extract_first_url_mixed_text():
    text = "Hey check this link https://phish.tk/login and tell me"
    assert extract_first_url(text) == "https://phish.tk/login"


def test_extract_first_url_no_url():
    text = "Hello, how are you?"
    assert extract_first_url(text) == "Hello, how are you?"


def test_analyze_url_use_case_legitimate():
    use_case = AnalyzeURLUseCase()
    result = use_case.execute("https://www.google.com")
    assert result["risk_level"] == "Low"
    assert result["risk_score"] == 0


def test_analyze_url_use_case_phishing():
    use_case = AnalyzeURLUseCase()
    result = use_case.execute("http://login.paypal.com.verify.tk/secure/update.php")
    assert result["risk_level"] in ("High", "Critical", "Medium")
    assert result["risk_score"] > 30


def test_analyze_url_use_case_mixed_text():
    use_case = AnalyzeURLUseCase()
    result = use_case.execute("ဒီမှာကြည့် https://wavemoney-free-bonus.com/claim")
    assert result["url"] == "https://wavemoney-free-bonus.com/claim"
    assert result["risk_level"] in ("High", "Critical")
