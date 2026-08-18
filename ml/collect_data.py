# ml/collect_data.py
import csv
from pathlib import Path

import requests

DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)


def fetch_openphish():
    """Download active phishing URLs from OpenPhish feed."""
    url = "https://openphish.com/feed.txt"
    resp = requests.get(url, timeout=15)
    resp.raise_for_status()
    urls = resp.text.strip().split("\n")
    rows = [{"url": u.strip(), "label": "bad"} for u in urls if u.strip()]
    output_path = DATA_DIR / "openphish_raw.csv"
    with open(output_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["url", "label"])
        writer.writeheader()
        writer.writerows(rows)
    print(f"OpenPhish: {len(rows)} URLs saved to {output_path}")


def fetch_urlhaus():
    """Download recent malicious URLs from URLhaus (abuse.ch)."""
    url = "https://urlhaus.abuse.ch/downloads/csv_recent/"
    resp = requests.get(url, timeout=15)
    resp.raise_for_status()
    lines = resp.text.strip().split("\n")
    rows = []
    # URLhaus CSV has 9 header lines, then actual data
    for line in lines[9:]:
        if line.startswith("#"):
            continue
        parts = line.split(",")
        if len(parts) >= 3:
            url_field = parts[2].strip('"')
            if url_field:
                rows.append({"url": url_field, "label": "bad"})
    output_path = DATA_DIR / "urlhaus_raw.csv"
    with open(output_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["url", "label"])
        writer.writeheader()
        writer.writerows(rows)
    print(f"URLhaus: {len(rows)} URLs saved to {output_path}")


if __name__ == "__main__":
    fetch_openphish()
    fetch_urlhaus()
