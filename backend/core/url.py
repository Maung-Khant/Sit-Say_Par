import re
from urllib.parse import urlparse

class URL:
    def __init__(self, url_string: str):
        if not url_string:
            raise ValueError("URL cannot be empty")

        url_string = url_string.strip()
        if ' ' in url_string:
            raise ValueError(f"URL cannot contain spaces: {url_string}")

        if not re.match(r'^[a-zA-Z][a-zA-Z\d+\-.]*://', url_string):
            url_string = 'http://' + url_string

        self._raw = url_string
        self._parsed = urlparse(url_string)
        if not self._parsed.netloc:
            raise ValueError(f"Invalid URL: {url_string}")

    @property
    def raw(self) -> str:
        return self._raw

    @property
    def domain(self) -> str:
        return self._parsed.netloc.lower()

    @property
    def path(self) -> str:
        return self._parsed.path

    def __str__(self):
        return self._raw
