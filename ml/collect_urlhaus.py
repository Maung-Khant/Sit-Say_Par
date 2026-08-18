# ml/collect_urlhaus.py
import csv
from pathlib import Path

import requests

URLHAUS_FEED = "https://urlhaus.abuse.ch/downloads/csv_recent/"


def fetch_urlhaus():
    resp = requests.get(URLHAUS_FEED)
    lines = resp.text.strip().split("\n")
    # Skip header line
    rows = []
    for line in lines[9:]:  # First 9 lines are comments/headers
        if line.startswith("#"):
            continue
        parts = line.split(",")
        if len(parts) >= 3:
            url = parts[2].strip('"')
            if url:
                rows.append({"url": url, "label": "bad"})

    output_path = Path(__file__).parent / "data" / "urlhaus_raw.csv"
    with open(output_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["url", "label"])
        writer.writeheader()
        writer.writerows(rows)
    print(f"Downloaded {len(rows)} URLs from URLhaus to {output_path}")


if __name__ == "__main__":
    fetch_urlhaus()
