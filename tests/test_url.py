import pytest
from backend.core.url import URL

def test_valid_url():
    url = URL("https://example.com")
    assert url.domain == "example.com"

def test_missing_scheme_adds_http():
    url = URL("example.com/path")
    assert url.raw.startswith("http://")

def test_invalid_url_raises_error():
    with pytest.raises(ValueError):
        URL("invalid url")
