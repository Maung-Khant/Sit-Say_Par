# ml/generate_dataset.py
import sys
from pathlib import Path
import pandas as pd
import csv

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from backend.core.url import URL
from backend.use_cases.feature_extractor import extract_features

# Original hardcoded lists (optional, can be empty)
phishing_urls = []
legitimate_urls = [
    "https://www.google.com",
    "https://www.kbzbank.com",
    "https://www.kbzpay.com",
    "https://www.cbbank.com.mm",
    "https://www.abank.com.mm",
    "https://www.wavemoney.com.mm",
    "https://www.mpt.com.mm",
    "https://www.wikipedia.org",
    "https://github.com",
    "https://stackoverflow.com",
    "https://www.amazon.com",
    "https://www.microsoft.com",
    "https://www.apple.com",
    "https://www.linkedin.com",
    "https://www.youtube.com",
]

def load_urls_from_csv(csv_path, label):
    """Read URLs from a CSV file (with 'url' column)."""
    urls = []
    if not csv_path.exists():
        return []
    with open(csv_path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("url"):
                urls.append(row["url"].strip())
    return [(u, label) for u in urls]

def generate_csv(output_path: str):
    rows = []

    # Legitimate URLs (hardcoded)
    for url_str in legitimate_urls:
        rows.append((url_str, "good"))

    # External phishing sources
    data_dir = Path(__file__).parent / "data"
    rows.extend(load_urls_from_csv(data_dir / "openphish_raw.csv", "bad"))
    rows.extend(load_urls_from_csv(data_dir / "urlhaus_raw.csv", "bad"))
    rows.extend(load_urls_from_csv(data_dir / "myanmar_phish.csv", "bad"))
    rows.extend(load_urls_from_csv(data_dir / "typosquat_myanmar.csv", "bad"))

    # Process rows and extract features
    processed_rows = []
    for url_str, label in rows:
        try:
            url_obj = URL(url_str)
            feats = extract_features(url_obj)
            # Keep only numeric features for ML
            feats = {k: v for k, v in feats.items() if isinstance(v, (int, float, bool))}
            row = {"url": url_str, "label": label}
            row.update(feats)
            processed_rows.append(row)
        except Exception as e:
            print(f"Skipping {url_str}: {e}")

    if not processed_rows:
        raise ValueError("No valid URLs processed!")

    df = pd.DataFrame(processed_rows)
    # Ensure only numeric columns (plus url, label)
    numeric_cols = ['url', 'label'] + [c for c in df.columns if c not in ('url', 'label') and pd.api.types.is_numeric_dtype(df[c])]
    df = df[numeric_cols]
    df.to_csv(output_path, index=False)
    print(f"Dataset saved to {output_path} with {len(df)} samples.")
    print(f"Phishing: {len(df[df['label']=='bad'])} | Legitimate: {len(df[df['label']=='good'])}")

if __name__ == "__main__":
    output = Path(__file__).parent / "data" / "urlset.csv"
    generate_csv(str(output))