# ml/generate_typosquat_dataset.py
import csv
import itertools
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from backend.use_cases.feature_extractor import MYANMAR_BRANDS, SUSPICIOUS_TLDS

# အသုံးပြုမည့် Common Typosquat Keywords / Suffixes
COMMON_WORDS = [
    "online",
    "login",
    "secure",
    "app",
    "pay",
    "bank",
    "money",
    "myanmar",
    "mm",
    "verify",
    "account",
    "update",
    "bonus",
    "claim",
    "free",
    "gift",
    "support",
    "service",
    "official",
]

# Leetspeak mapping for homoglyph (ဂဏန်းအသုံးပြုထားသော)
LEET_MAP = {
    "a": "4",
    "e": "3",
    "i": "1",
    "l": "1",
    "o": "0",
    "s": "5",
    "b": "8",
    "g": "9",
}


def leet_variant(text: str) -> str:
    """ဂဏန်းအသုံးပြုထားသော leetspeak variant ထုတ်လုပ်ပါ။"""
    return "".join(LEET_MAP.get(ch, ch) for ch in text)


def vowel_swaps(text: str) -> set:
    """သရအက္ခရာများကို အခြားသရဖြင့် လဲလှယ်ပါ။"""
    vowels = "aeiou"
    variants = set()
    for i, ch in enumerate(text):
        if ch in vowels:
            for v in vowels:
                if v != ch:
                    variants.add(text[:i] + v + text[i + 1 :])
    return variants


def generate_typosquats(brand_norm: str) -> set:
    """Brand တစ်ခုအတွက် Typosquat Variants များစွာ ထုတ်လုပ်ပါ။"""
    variants = set()

    # 1. Original
    variants.add(brand_norm)

    # 2. Omission (စာလုံးတစ်လုံးဖျက်)
    for i in range(len(brand_norm)):
        variants.add(brand_norm[:i] + brand_norm[i + 1 :])

    # 3. Insertion (အပိုစာလုံးထည့်)
    for pos in range(len(brand_norm) + 1):
        for ch in "sreaxy":
            variants.add(brand_norm[:pos] + ch + brand_norm[pos:])

    # 4. Replacement (ဆင်တူအက္ခရာ အစားထိုး)
    similar = {
        "a": "e",
        "e": "a",
        "o": "0",
        "0": "o",
        "l": "1",
        "i": "l",
        "l": "i",
        "b": "d",
        "d": "b",
        "m": "n",
        "n": "m",
        "v": "w",
        "w": "v",
        "s": "5",
        "5": "s",
        "z": "s",
        "s": "z",
    }
    for i, ch in enumerate(brand_norm):
        if ch in similar:
            variants.add(brand_norm[:i] + similar[ch] + brand_norm[i + 1 :])

    # 5. Vowel Swap
    variants.update(vowel_swaps(brand_norm))

    # 6. Plural (s/es ပေါင်း)
    variants.add(brand_norm + "s")
    variants.add(brand_norm + "es")

    # 7. Leetspeak (Homoglyph)
    leet = leet_variant(brand_norm)
    if leet != brand_norm:
        variants.add(leet)

    # 8. Dictionary + Brand combinations
    for word in COMMON_WORDS:
        variants.add(brand_norm + word)
        variants.add(word + brand_norm)
        variants.add(brand_norm + "-" + word)
        variants.add(word + "-" + brand_norm)

    # Filter out too short variants
    return {v for v in variants if len(v) >= 3}


def generate_dataset():
    output_path = Path(__file__).parent / "data" / "typosquat_myanmar.csv"
    rows = []

    for brand in MYANMAR_BRANDS:
        brand_norm = brand.replace(" ", "")
        if len(brand_norm) < 3:
            continue
        variants = generate_typosquats(brand_norm)
        # Common suspicious TLD များနှင့် ပေါင်းစပ်ပြီး URL များ ဖန်တီးပါ
        # (Dataset ကြီးလွန်းမသွားစေရန် TLD 5 ခုသာ သုံးပါ)
        chosen_tlds = [".tk", ".ml", ".xyz", ".top", ".online"]
        for var in variants:
            # Typosquat domain ၏ အဓိက ပုံစံများထဲမှ အနည်းငယ်ကိုသာ ယူပါ
            if len(rows) > 50000:  # Safety limit
                break
            for tld in chosen_tlds:
                rows.append({"url": f"http://{var}{tld}", "label": "bad"})
        if len(rows) > 50000:
            break

    # CSV သိမ်းဆည်း
    output_path.parent.mkdir(exist_ok=True)
    with open(output_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["url", "label"])
        writer.writeheader()
        writer.writerows(rows)
    print(f"Typosquat dataset saved to {output_path} with {len(rows)} samples")


if __name__ == "__main__":
    generate_dataset()
