# ml/collect_openphish.py
from pathlib import Path

import requests

URL = "https://openphish.com/feed.txt"


def fetch_openphish():
    resp = requests.get(URL)
    urls = resp.text.strip().split("\n")
    rows = [{"url": u, "label": "bad"} for u in urls if u]
    output_path = Path(__file__).parent / "data" / "openphish_raw.csv"
    import csv

    with open(output_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["url", "label"])
        writer.writeheader()
        writer.writerows(rows)
    print(f"Downloaded {len(rows)} phishing URLs to {output_path}")


if __name__ == "__main__":
    fetch_openphish()
