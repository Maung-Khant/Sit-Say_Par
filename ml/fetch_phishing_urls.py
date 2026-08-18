# ml/fetch_phishing_urls.py
import csv
from pathlib import Path

import requests


def fetch_openphish(output_file: str, limit: int = 500):
    """Fetch phishing URLs from OpenPhish feed."""
    url = "https://openphish.com/feed.txt"
    resp = requests.get(url, timeout=30)
    urls = resp.text.strip().split("\n")
    # Take only the first 'limit' URLs
    urls = urls[:limit]

    with open(output_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["url", "label"])
        for u in urls:
            writer.writerow([u.strip(), "bad"])
    print(f"Saved {len(urls)} phishing URLs to {output_file}")


def fetch_phishtank(api_key: str, output_file: str, limit: int = 500):
    """Fetch verified phishing URLs from PhishTank (requires API key)."""
    # PhishTank API v2
    base = "https://data.phishtank.com/data/"
    params = {"format": "csv", "limit": limit, "verified": "true", "app_key": api_key}
    resp = requests.get(base, params=params, timeout=30)
    # The API returns CSV data directly
    if resp.status_code == 200:
        with open(output_file, "wb") as f:
            f.write(resp.content)
        print(f"Saved PhishTank data to {output_file}")
    else:
        print(f"PhishTank request failed: {resp.status_code}")


if __name__ == "__main__":
    data_dir = Path(__file__).parent / "data"
    data_dir.mkdir(exist_ok=True)

    # 1. OpenPhish
    fetch_openphish(data_dir / "openphish.csv", limit=500)

    # 2. PhishTank (if you have API key, uncomment and set key)
    # PHISHTANK_API_KEY = "your_api_key_here"
    # fetch_phishtank(PHISHTANK_API_KEY, data_dir / "phishtank.csv", limit=500)
