# ml/generate_synthetic_myanmar.py
import csv
import random
from pathlib import Path

# Import brand list and suspicious TLDs from your feature extractor
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from backend.use_cases.feature_extractor import MYANMAR_BRANDS, SUSPICIOUS_TLDS

# Common phishing keywords (from our list)
PHISHING_KEYWORDS = [
    'login', 'verify', 'secure', 'account', 'update', 'confirm',
    'bonus', 'claim', 'gift', 'free', 'win', 'prize',
    'security', 'support', 'password', 'banking', 'unlock'
]

# Official domains for legitimate examples (from rule_engine)
OFFICIAL_DOMAINS = {
    'kbz': ['kbzbank.com', 'kbzpay.com', 'kbzlife.com'],
    'cb': ['cbbank.com.mm'],
    'aya': ['ayabank.com'],
    'uab': ['uab.com.mm'],
    'wave': ['wavemoney.com.mm'],
    'mpt': ['mpt.com.mm'],
    'mytel': ['mytel.com.mm'],
    'atom': ['atom.com.mm'],
    'google': ['google.com'],
    'facebook': ['facebook.com'],
}

def generate_synthetic_phishing_urls(n=300):
    urls = []
    for _ in range(n):
        brand = random.choice(MYANMAR_BRANDS).replace(' ', '')
        tld = random.choice(SUSPICIOUS_TLDS)
        keyword1 = random.choice(PHISHING_KEYWORDS)
        keyword2 = random.choice(PHISHING_KEYWORDS)
        pattern = random.choice([
            f"https://{brand}-{keyword1}-{keyword2}{tld}",
            f"https://{brand}{keyword1}-{keyword2}{tld}",
            f"https://{keyword1}.{brand}.{keyword2}{tld}",
            f"https://{brand}-{keyword1}{tld}/{keyword2}",
            f"https://www.{brand}{keyword1}.{keyword2}{tld}"
        ])
        urls.append(pattern)
    return urls

def generate_legitimate_urls():
    urls = []
    for brand, domains in OFFICIAL_DOMAINS.items():
        for d in domains:
            urls.append(f"https://www.{d}")
            urls.append(f"https://{d}")
    return urls

def main():
    output_path = Path(__file__).parent / "data" / "myanmar_synthetic.csv"
    phish = generate_synthetic_phishing_urls(300)
    legit = generate_legitimate_urls()

    rows = [{"url": u, "label": "bad"} for u in phish]
    rows += [{"url": u, "label": "good"} for u in legit]

    with open(output_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["url", "label"])
        writer.writeheader()
        writer.writerows(rows)
    print(f"Synthetic dataset saved to {output_path} ({len(rows)} samples)")

if __name__ == "__main__":
    main()