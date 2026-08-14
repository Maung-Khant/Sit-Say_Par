# backend/use_cases/feature_extractor.py
import re
import difflib
from pathlib import Path
from backend.core.url import URL

# Suspicious keywords (English + Myanmar relevant)
SUSPICIOUS_KEYWORDS = [
    'login', 'signin', 'verify', 'verification', 'secure', 'account',
    'update', 'upgrade', 'confirm', 'banking', 'password', 'credential',
    'urgent', 'alert', 'limited', 'suspended',
    'free', 'bonus', 'claim', 'gift', 'lucky', 'win', 'prize',
    'security', 'auth', 'authenticate', 'unlock', 'reactivate',
    'support', 'compliance', 'token', 'sync', 'mfa', 'authorization',
    'override', 'settlement', 'agent', 'portal', 'recover', 'restore',
    # Myanmar scam keywords
    'ဆုကြေး', 'ငွေထုတ်', 'အကောင့်အဆင့်မြှင့်', 'အတည်ပြုရန်',
    'ပိတ်သိမ်းမည်', 'ချက်ချင်း', 'အရေးပေါ်', 'လက်ဆောင်',
    'အကောင့်ဝင်', 'စကားဝှက်', 'ဘဏ်', 'ငွေလွှဲ',
    'အောက်ပါလင့်ခ်', 'ဒီလင့်ခ်', 'ဆက်သွယ်ရန်',
    'အကောင့်ပိတ်မည်', 'ငွေထုတ်ယူရန်', 'အကောင့်အတည်ပြုခြင်း',
    'ဘဏ်အကောင့်', 'ငွေလက်ကျန်', 'ဘောနပ်စ်', 'ဆုလာဘ်',
    'ငွေသွင်းရန်', 'ငွေထုတ်ရန်'
]

# TLDs frequently abused by phishers
SUSPICIOUS_TLDS = ['.tk', '.ml', '.ga', '.cf', '.xyz', '.top', '.club',
                   '.info', '.website', '.online', '.test', '.help']

# Comprehensive Myanmar brand list (lowercase)
MYANMAR_BRANDS = [
    # Banks & Financial / Mobile-Money
    "kbz", "kbz bank", "kbzbank", "kanbawza", "kanbawza bank",
    "kbzpay", "kbz pay", "kpay", "k pay", "kplus",
    "cb", "cb bank", "cbbank", "co-operative bank", "cooperative bank",
    "cb pay", "cbpay",
    "yoma", "yoma bank", "yomabank", "yoma pay", "yomapay",
    "aya", "aya bank", "ayabank", "ayeyarwady bank", "aya pay", "ayapay",
    "uab", "uab bank", "uabbank", "united amara bank", "uab pay", "uabpay",
    "a bank", "abank", "agd bank", "agd", "asia green development bank",
    "mtb", "mtb bank", "myanma tourism bank", "myanmar tourism bank",
    "mtb pay", "mtbpay",
    "sathapana", "sathapana bank", "sathapana limited",
    "cbm", "central bank of myanmar",
    "wave", "wave money", "wavemoney", "wave pay", "wavepay", "waveshop",
    "ok dollar", "okdollar", "ok$", "true money", "truemoney",
    "global money", "citizens bank", "myanmar citizens bank", "mcb",
    "first private bank", "fpb", "innwa bank",
    "myanma economic bank", "meb",
    "myanma foreign trade bank", "mftb",
    "myawaddy bank", "mwd bank", "mwdbank",
    "myanma apex bank", "mab",
    "myanma oriental bank", "mob",
    "small and medium industrial development bank", "smidb",
    "yangon united bank", "yub",
    "global treasure bank", "gtb",
    "shwe bank", "rural development bank",
    "advans myanmar", "advans", "proximity finance",

    # Telecom Operators
    "mpt", "myanmar posts and telecommunications",
    "telenor", "telenor myanmar",
    "ooredoo", "ooredoo myanmar",
    "mytel",
    "kddi",
    "atom", "atom myanmar",

    # Online Shopping Platforms
    "lazada", "shopee", "ubuy",
    "grip digi", "gripdigi",
    "foodpanda", "grab", "grab myanmar",
    "city mart", "citymart",
    "aliexpress", "ali express", "alibaba",
    "amazon", "temu",
    "shop.com.mm",

    # Government Departments
    "ird", "internal revenue department",
    "dme", "department of myanmar examinations",
    "mrf",
    "myanmar immigration", "immigration department",
    "ycdc", "yangon city development committee",
    "myanmar police force", "myanmar police",
    "rtad", "road transport administration department",
    "moee", "yangon electricity supply corporation", "yesc",
    "myanmar customs department", "myanmar customs",
    "department of labour",
    "uec", "union election commission",
    "dica", "directorate of investment and company administration",

    # Other Notable Organizations
    "kpmg",
    "quick loan", "quickloan",
    "air thanlwin",
    "myanmar national airlines", "man airlines",
    "air kbz",
    "fmi", "first myanmar investment",
    "capital diamond star group", "cdsg",
    "max myanmar",
    "shwe taung",
    "yoma strategic holdings",
    "dhl", "fedex", "ups", "royal express", "yangon door2door",
    "j&t express", "jt express",

    # International Tech / Platform Brands
    "facebook", "messenger", "meta",
    "google", "gmail",
    "apple", "icloud",
    "microsoft", "outlook",
    "netflix",
    "whatsapp", "instagram", "tiktok", "viber", "telegram", "zoom",
    "paypal",
    "binance", "octafx",
]

# Leetspeak mapping for homoglyph/typosquatting detection
LEETSPEAK_MAP = str.maketrans({
    '0': 'o', '1': 'l', '3': 'e', '4': 'a', '5': 's', '7': 't', '8': 'b', '9': 'g', '@': 'a'
})

def normalize_leet(text: str) -> str:
    """Convert common leetspeak digits to letters and lowercase."""
    return text.translate(LEETSPEAK_MAP).lower()

def find_lookalike_brands(domain: str) -> list:
    """
    Detect brand names that are similar to part of the domain (typosquatting).
    Uses difflib to compute similarity ratio.
    """
    lookalikes = []
    # Remove leading www. and lower
    domain_clean = domain.lower()
    if domain_clean.startswith('www.'):
        domain_clean = domain_clean[4:]

    # Split domain into parts by dot
    parts = domain_clean.split('.')

    for brand in MYANMAR_BRANDS:
        brand_norm = brand.replace(' ', '')
        for part in parts:
            # Skip very short parts (avoid false positives like 'k')
            if len(part) < 3:
                continue
            # Compute similarity ratio (0 to 1)
            ratio = difflib.SequenceMatcher(None, part, brand_norm).ratio()
            # Trigger if very similar (>= 0.85) or identical length and edit distance small
            if ratio >= 0.85 or (abs(len(part) - len(brand_norm)) <= 1 and ratio >= 0.80):
                lookalikes.append(brand)
                break  # one brand matched enough

    return lookalikes

# URL shortener domains (exact or subdomain)
SHORTENER_DOMAINS = [
    'bit.ly', 'tinyurl.com', 'goo.gl', 'ow.ly', 't.co',
    'kpay.link', 'wavepay.cc', 'kbzpay.link', 'mpt.shop',
    'cutt.ly', 'shorturl.at', 'rb.gy'
]

def is_shortener_domain(domain: str) -> bool:
    """Check if domain is a URL shortener (exact match or subdomain)."""
    domain_clean = domain.lower()
    if domain_clean.startswith('www.'):
        domain_clean = domain_clean[4:]
    for short in SHORTENER_DOMAINS:
        if domain_clean == short or domain_clean.endswith('.' + short):
            return True
    return False


def extract_features(url: URL) -> dict:
    raw = url.raw.lower()
    domain = url.domain
    path = url.path

    features = {}

    # Basic lexical features
    features['url_length'] = len(raw)
    features['domain_dot_count'] = domain.count('.')
    features['is_ip'] = 1 if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', domain) else 0
    features['has_at_symbol'] = 1 if '@' in raw else 0
    features['has_double_slash'] = 1 if '//' in path else 0
    features['has_https_in_path'] = 1 if 'https' in path else 0
    features['domain_hyphen_count'] = domain.count('-')

    # Suspicious keywords count
    keyword_count = sum(1 for kw in SUSPICIOUS_KEYWORDS if kw in raw)
    features['suspicious_keyword_count'] = keyword_count

    # Suspicious TLD
    tld_match = re.search(r'\.[a-z]{2,}$', domain)
    tld = tld_match.group(0) if tld_match else ''
    features['suspicious_tld'] = 1 if tld in SUSPICIOUS_TLDS else 0

    # Path depth
    features['path_depth'] = path.count('/') if path else 0

    # URL shortener check using proper function
    features['is_shortener'] = 1 if is_shortener_domain(domain) else 0

    # Brand detection (with leetspeak normalization)
    brand_found = []
    # Normalize domain once
    domain_clean = domain.replace(' ', '')
    domain_leet = normalize_leet(domain_clean)  # e.g., micros0ft -> microsoft
    path_clean = path.replace(' ', '')

        # Lookalike brand detection (fuzzy)
    lookalike_brands = find_lookalike_brands(domain)
    features['lookalike_brands_detected'] = ','.join(lookalike_brands) if lookalike_brands else 'none'
    features['lookalike_brand_count'] = len(lookalike_brands)



    for brand in MYANMAR_BRANDS:
        brand_normalized = brand.replace(' ', '')
        # Check original domain and leetspeak-normalized domain
        if brand_normalized in domain_clean or brand_normalized in domain_leet or brand in path:
            brand_found.append(brand)

    features['brands_detected'] = ','.join(brand_found) if brand_found else 'none'
    features['brand_count'] = len(brand_found)

    # Domain digit count
    features['domain_digit_count'] = sum(c.isdigit() for c in domain)

    # Homograph / IDN detection
    try:
        import idna
        idna.encode(domain)  # Just to verify if IDN
        features['has_idn'] = 1 if any(ord(c) > 127 for c in domain) else 0
    except:
        features['has_idn'] = 0


    # Blacklist check
    blacklist = load_blacklist()
    domain_clean = domain.lower()
    if domain_clean.startswith('www.'):
        domain_clean = domain_clean[4:]
    features['in_blacklist'] = 1 if domain_clean in blacklist else 0
    
    # Include domain string for rule engine
    features['domain'] = domain

    return features


# Cache for blacklist
_BLACKLIST_CACHE = None

def load_blacklist() -> set:
    global _BLACKLIST_CACHE
    if _BLACKLIST_CACHE is None:
        blacklist_file = Path(__file__).resolve().parent.parent / "infrastructure" / "phishing_blacklist.txt"
        if blacklist_file.exists():
            with open(blacklist_file, 'r') as f:
                _BLACKLIST_CACHE = {line.strip().lower() for line in f if line.strip()}
        else:
            _BLACKLIST_CACHE = set()
    return _BLACKLIST_CACHE