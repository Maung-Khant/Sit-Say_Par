# ml/generate_dataset.py
import sys
from pathlib import Path
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from backend.core.url import URL
from backend.use_cases.feature_extractor import extract_features

phishing_urls = [
    "http://login.paypal.com.verify.tk/secure/update.php",
    "http://wavemoney-free-bonus.com/claim",
    "https://facebook-security-login-auth.net/profile",
    "http://192.168.1.1/kbz/login",
    "http://mytel-prize.ml/win",
    "https://www.google.com@phishing.cn/login",
    "http://bit.ly/2abcd3e",
    "http://secure-login.paypal.com.tk/",
    "https://verify-apple-id.com/account",
    "http://free-netflix-premium.xyz/verify",
    "http://update-kbzbank.com/login",
    "http://cbbank-online.website/account",
    "https://www.facebook.com.fake.tk/security",
    "http://urgent-paypal-alert.ga/restore",
    "http://gift-claim-mpt.ml/win",
    "http://kbzpay.workers.dev/login",
    "http://ayabank-online.ml/verify",
    "http://uab-pay.ml/confirm",
    "http://yoma-banking.xyz/login",
    "http://sathapana-verify.tk/account",
]

legitimate_urls = [
    "https://www.google.com",
    "https://www.facebook.com",
    "https://www.wavemoney.com.mm",
    "https://www.kbzbank.com",
    "https://www.cbbank.com.mm",
    "https://www.ayabank.com",
    "https://www.uab.com.mm",
    "https://www.mpt.com.mm",
    "https://www.telenor.com.mm",
    "https://www.wikipedia.org",
    "https://github.com",
    "https://stackoverflow.com",
    "https://www.bbc.com",
    "https://www.youtube.com",
    "https://www.amazon.com",
    "https://www.myanmarpixel.com",
    "https://www.mmmyanmar.com",
    "https://www.linkedin.com",
    "https://www.microsoft.com",
    "https://www.apple.com",
]

def generate_csv(output_path: str):
    rows = []
    for url_str in phishing_urls:
        try:
            url_obj = URL(url_str)
            feats = extract_features(url_obj)
            # Keep only numeric features (ML needs numbers)
            feats = {k: v for k, v in feats.items() if isinstance(v, (int, float, bool))}
            row = {'url': url_str, 'label': 'bad'}
            row.update(feats)
            rows.append(row)
        except Exception as e:
            print(f"Skipping {url_str}: {e}")

    for url_str in legitimate_urls:
        try:
            url_obj = URL(url_str)
            feats = extract_features(url_obj)
            feats = {k: v for k, v in feats.items() if isinstance(v, (int, float, bool))}
            row = {'url': url_str, 'label': 'good'}
            row.update(feats)
            rows.append(row)
        except Exception as e:
            print(f"Skipping {url_str}: {e}")

    if not rows:
        raise ValueError("No valid URLs processed!")

    df = pd.DataFrame(rows)
    # Reorder: url, feature columns, label
    feature_cols = [c for c in df.columns if c not in ('url', 'label') and pd.api.types.is_numeric_dtype(df[c])]
    df = df[['url'] + feature_cols + ['label']]
    df.to_csv(output_path, index=False)
    print(f"Dataset saved to {output_path} with {len(df)} samples ({len(feature_cols)} features).")

if __name__ == "__main__":
    output = Path(__file__).parent / "data" / "urlset.csv"
    generate_csv(str(output))
