# backend/use_cases/feature_extractor.py
import re
from backend.core.url import URL

# Suspicious keywords
SUSPICIOUS_KEYWORDS = [
    'login', 'signin', 'verify', 'verification', 'secure', 'account',
    'update', 'upgrade', 'confirm', 'banking', 'password', 'credential',
    'urgent', 'alert', 'limited', 'suspended',
    'free', 'bonus', 'claim', 'gift', 'lucky', 'win', 'prize',
    'security', 'auth', 'authenticate', 'unlock', 'reactivate',
    'support', 'compliance', 'token', 'sync', 'mfa', 'authorization',
    'override', 'settlement', 'agent', 'portal', 'recover', 'restore'
]

# TLDs frequently abused by phishers
SUSPICIOUS_TLDS = ['.tk', '.ml', '.ga', '.cf', '.xyz', '.top', '.club', '.info', '.website', '.online', '.test', '.help']
# Comprehensive Myanmar brand list (lowercase)
MYANMAR_BRANDS = [
    # Banks & Financial / Mobile-Money
    "kbz", "kbz bank", "kbzbank", "kanbawza", "kanbawza bank",
    "kbzpay", "kbz pay", "kpay", "k pay", "k+", "kplus", "k+wallet",
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

    # URL shortener check
    shorteners = [
    'bit.ly', 'tinyurl.com', 'goo.gl', 'ow.ly', 't.co',
    'kpay.link', 'wavepay.cc', 'kbzpay.link', 'mpt.shop',
    'cutt.ly', 'shorturl.at', 'rb.gy'
    ]
    features['is_shortener'] = 1 if any(s in domain for s in shorteners) else 0

    # Brand detection
    brand_found = []
    for brand in MYANMAR_BRANDS:
        brand_normalized = brand.replace(' ', '')
        domain_clean = domain.replace(' ', '')
        if brand_normalized in domain_clean or brand in path:
            brand_found.append(brand)
    features['brands_detected'] = ','.join(brand_found) if brand_found else 'none'
    features['brand_count'] = len(brand_found)

    # Domain digit count
    features['domain_digit_count'] = sum(c.isdigit() for c in domain)

# Homograph detection: check if domain contains non-ASCII characters (IDN)
    try:
        import idna
        idna.encode(domain)  # If domain is already punycode, this won't raise
        features['has_idn'] = 1 if any(ord(c) > 127 for c in domain) else 0
    except:
        features['has_idn'] = 0

    # Include domain string for rule engine
    features['domain'] = domain

    return features