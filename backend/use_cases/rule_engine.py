# backend/use_cases/rule_engine.py
import re
from datetime import datetime
from typing import Dict, List, Tuple

import whois

RuleResult = Tuple[bool, int, str]

# -------------------------------------------------------------------
# Official domains – prevents false positives on legitimate sites
# -------------------------------------------------------------------
OFFICIAL_DOMAINS = {
    # KBZ Group
    'kbz': ['kbzbank.com', 'kbzpay.com'],
    'kbz bank': ['kbzbank.com'],
    'kbzbank': ['kbzbank.com'],
    'kanbawza': ['kbzbank.com'],
    'kanbawza bank': ['kbzbank.com'],
    'kbzpay': ['kbzpay.com', 'kbzpay.com.mm', 'kbzbank.com'],
    'kbz pay': ['kbzpay.com', 'kbzpay.com.mm', 'kbzbank.com'],
    'kpay': ['kbzpay.com', 'kbzpay.com.mm', 'kbzbank.com'],
    'k pay': ['kbzpay.com', 'kbzpay.com.mm', 'kbzbank.com'],
    'k+': ['kbzpay.com', 'kbzbank.com'],
    'kplus': ['kbzpay.com', 'kbzbank.com'],
    'k+wallet': ['kbzpay.com', 'kbzbank.com'],

    # CB Bank
    'cb': ['cbbank.com.mm'],
    'cb bank': ['cbbank.com.mm'],
    'cbbank': ['cbbank.com.mm'],
    'co-operative bank': ['cbbank.com.mm'],
    'cooperative bank': ['cbbank.com.mm'],
    'cb pay': ['cbbank.com.mm'],
    'cbpay': ['cbbank.com.mm'],

    # AYA Bank
    'aya': ['ayabank.com'],
    'aya bank': ['ayabank.com'],
    'ayabank': ['ayabank.com'],
    'ayeyarwady bank': ['ayeyarwadybank.com'],
    'aya pay': ['ayabank.com'],
    'ayapay': ['ayabank.com'],

    # UAB Bank
    'uab': ['uab.com.mm'],
    'uab bank': ['uab.com.mm'],
    'uabbank': ['uab.com.mm'],
    'united amara bank': ['uab.com.mm'],
    'uab pay': ['uab.com.mm'],
    'uabpay': ['uab.com.mm'],

    # A Bank (AGD)
    'a bank': ['abank.com.mm'],
    'abank': ['abank.com.mm'],
    'agd bank': ['agdbank.com'],
    'agd': ['agdbank.com'],
    'asia green development bank': ['agdbank.com'],

    # Yoma Bank
    'yoma': ['yoma.com.mm'],
    'yoma bank': ['yoma.com.mm'],
    'yomabank': ['yoma.com.mm'],
    'yoma pay': ['yoma.com.mm'],
    'yomapay': ['yoma.com.mm'],

    # Other Banks
    'mtb': ['mtb.com.mm'],
    'mtb bank': ['mtb.com.mm'],
    'myanma tourism bank': ['mtb.com.mm'],
    'sathapana': ['sathapanabank.com'],
    'sathapana bank': ['sathapanabank.com'],
    'cbm': ['cbm.gov.mm'],
    'central bank of myanmar': ['cbm.gov.mm'],

    # Wave Money
    'wave': ['wavemoney.com.mm'],
    'wave money': ['wavemoney.com.mm'],
    'wavemoney': ['wavemoney.com.mm'],
    'wave pay': ['wavemoney.com.mm'],
    'wavepay': ['wavemoney.com.mm'],

    # Telecom Operators
    'mpt': ['mpt.com.mm'],
    'myanmar posts and telecommunications': ['mpt.com.mm'],
    'telenor': ['telenor.com.mm'],
    'telenor myanmar': ['telenor.com.mm'],
    'ooredoo': ['ooredoo.com.mm'],
    'ooredoo myanmar': ['ooredoo.com.mm'],
    'mytel': ['mytel.com.mm'],
    'atom': ['atom.com.mm'],
    'atom myanmar': ['atom.com.mm'],

    # International Tech
    'google': ['google.com'],
    'facebook': ['facebook.com'],
    'messenger': ['facebook.com'],
    'meta': ['meta.com'],
    'gmail': ['google.com'],
    'apple': ['apple.com'],
    'icloud': ['icloud.com'],
    'microsoft': ['microsoft.com'],
    'outlook': ['outlook.com'],
    'netflix': ['netflix.com'],
    'whatsapp': ['whatsapp.com'],
    'instagram': ['instagram.com'],
    'tiktok': ['tiktok.com'],
    'viber': ['viber.com'],
    'telegram': ['telegram.org'],
    'zoom': ['zoom.us'],
    'paypal': ['paypal.com'],
    'binance': ['binance.com'],
    'octafx': ['octafx.com'],

    # E-commerce / others
    'lazada': ['lazada.com.mm'],
    'shopee': ['shopee.com.mm'],
    'amazon': ['amazon.com'],
    'aliexpress': ['aliexpress.com'],
    'grab': ['grab.com'],
    'foodpanda': ['foodpanda.com.mm'],
    'city mart': ['citymart.com.mm'],
    'citymart': ['citymart.com.mm'],
    'shop.com.mm': ['shop.com.mm'],

    # Delivery
    'dhl': ['dhl.com'],
    'fedex': ['fedex.com'],
    'ups': ['ups.com'],
    'royal express': ['royalexpress.com.mm'],
    'yangon door2door': ['yangondoor2door.com'],
    'j&t express': ['jtexpress.com'],
    'jt express': ['jtexpress.com'],

    # Government Departments & Public Bodies
    'ird': ['ird.gov.mm'],
    'internal revenue department': ['ird.gov.mm'],
    'dme': ['dme.gov.mm'],
    'department of myanmar examinations': ['dme.gov.mm'],
    'mrf': ['mrf.gov.mm'],
    'myanmar immigration': ['mip.gov.mm'],
    'immigration department': ['mip.gov.mm'],
    'ycdc': ['ycdc.gov.mm'],
    'yangon city development committee': ['ycdc.gov.mm'],
    'myanmar police force': ['myanmarpolice.gov.mm'],
    'myanmar police': ['myanmarpolice.gov.mm'],
    'rtad': ['rtad.gov.mm'],
    'road transport administration department': ['rtad.gov.mm'],
    'moee': ['moee.gov.mm'],
    'yangon electricity supply corporation': ['yesc.com.mm'],
    'yesc': ['yesc.com.mm'],
    'myanmar customs department': ['customs.gov.mm'],
    'myanmar customs': ['customs.gov.mm'],
    'department of labour': ['mol.gov.mm'],
    'uec': ['uec.gov.mm'],
    'union election commission': ['uec.gov.mm'],
    'dica': ['dica.gov.mm'],
    'directorate of investment and company administration': ['dica.gov.mm'],

    # Other Notable Organizations
    'kpmg': ['kpmg.com.mm'],
    'quick loan': ['quickloan.com.mm'],
    'quickloan': ['quickloan.com.mm'],
    'air thanlwin': ['airthanlwin.com'],
    'myanmar national airlines': ['flymna.com'],
    'man airlines': ['flymna.com'],
    'air kbz': ['airkbz.com'],
    'fmi': ['fmi.com.mm'],
    'first myanmar investment': ['fmi.com.mm'],
    'capital diamond star group': ['cdsg.com.mm'],
    'cdsg': ['cdsg.com.mm'],
    'max myanmar': ['maxmyanmar.com'],
    'shwe taung': ['shwetaung.com.mm'],
    'yoma strategic holdings': ['yoma.com.mm'],
}


def _is_official_domain(domain: str, brand: str) -> bool:
    """Check if domain is official for the given brand, stripping www if necessary."""
    official_list = OFFICIAL_DOMAINS.get(brand, [])
    if not official_list:
        return False
    domain_clean = domain.lower().rstrip('/')
    # Remove leading www. for reliable matching
    if domain_clean.startswith('www.'):
        domain_clean = domain_clean[4:]
    for official in official_list:
        if domain_clean == official or domain_clean.endswith('.' + official):
            return True
    return False


# -------------------------------------------------------------------
# WHOIS helper
# -------------------------------------------------------------------
def get_domain_age_days(domain: str) -> int | None:
    try:
        w = whois.whois(domain)
        creation_date = w.creation_date
        if isinstance(creation_date, list):
            creation_date = creation_date[0]
        if creation_date:
            return (datetime.now() - creation_date).days
    except Exception:
        pass
    return None


# -------------------------------------------------------------------
# Rule functions
# -------------------------------------------------------------------
def _rule_ip_address(features: Dict) -> RuleResult:
    if features.get('is_ip', 0) == 1:
        return (True, 30, "IP လိပ်စာကို တိုက်ရိုက်အသုံးပြုထားသည် (domain name အစား)။")
    return (False, 0, "")


def _rule_suspicious_tld(features: Dict) -> RuleResult:
    domain = features.get('domain', '')
    suspicious_tlds = ['.tk', '.ml', '.ga', '.cf', '.xyz', '.top', '.club',
                       '.info', '.website', '.online', '.test', '.help']
    tld_match = re.search(r'\.[a-z]{2,}$', domain)
    tld = tld_match.group(0) if tld_match else ''
    if tld in suspicious_tlds:
        return (True, 30, f"သံသယဖြစ်ဖွယ် domain အဆုံးသတ် ({tld}) ကို သုံးထားသည်။")
    return (False, 0, "")


def _rule_suspicious_keywords(features: Dict) -> RuleResult:
    count = features.get('suspicious_keyword_count', 0)
    if count >= 3:
        return (True, 35, f"သံသယဖြစ်ဖွယ် စာလုံးရေ {count} လုံး (login, verify, bonus, free စသည်) ပါဝင်သည်။")
    elif count >= 1:
        return (True, 20, f"သံသယဖြစ်ဖွယ် စာလုံး {count} လုံး ပါဝင်သည်။")
    return (False, 0, "")


def _rule_at_symbol(features: Dict) -> RuleResult:
    if features.get('has_at_symbol', 0) == 1:
        return (True, 20, "URL တွင် '@' သင်္ကေတ ပါဝင်သည်။")
    return (False, 0, "")


def _rule_double_slash_redirect(features: Dict) -> RuleResult:
    if features.get('has_double_slash', 0) == 1:
        return (True, 15, "လမ်းကြောင်းထဲတွင် '//' ပါဝင်သဖြင့် redirect လုပ်နိုင်ခြေရှိသည်။")
    return (False, 0, "")


def _rule_https_in_path(features: Dict) -> RuleResult:
    if features.get('has_https_in_path', 0) == 1:
        return (True, 15, "လမ်းကြောင်းထဲတွင် 'https' ပါဝင်သဖြင့် လှည့်စားရန် ကြိုးပမ်းမှုဖြစ်နိုင်သည်။")
    return (False, 0, "")


def _rule_domain_hyphens(features: Dict) -> RuleResult:
    count = features.get('domain_hyphen_count', 0)
    if count >= 3:
        return (True, 25, f"Domain တွင် hyphens {count} ခုပါဝင်သဖြင့် brand အတုခိုးရန် ကြိုးစားမှုဖြစ်နိုင်သည်။")
    elif count >= 2:
        return (True, 15, f"Domain တွင် hyphens {count} ခုပါဝင်သဖြင့် brand အတုခိုးရန် ကြိုးစားမှုဖြစ်နိုင်သည်။")
    return (False, 0, "")


def _rule_shortener(features: Dict) -> RuleResult:
    if features.get('is_shortener', 0) == 1:
        return (True, 15, "URL shortener ဝန်ဆောင်မှုကို သုံးထားသည်။")
    return (False, 0, "")


def _rule_long_url(features: Dict) -> RuleResult:
    length = features.get('url_length', 0)
    if length > 100:
        return (True, 10, f"URL အရှည် {length} လုံး ရှိသဖြင့် သံသယဖြစ်ဖွယ်ရှိသည်။")
    return (False, 0, "")


def _rule_brand_impersonation(features: Dict) -> RuleResult:
    brands_str = features.get('brands_detected', 'none')
    if brands_str == 'none':
        return (False, 0, "")
    domain = features.get('domain', '')
    brand_list = [b.strip() for b in brands_str.split(',')]
    suspicious_brands = []
    for brand in brand_list:
        if not _is_official_domain(domain, brand):
            suspicious_brands.append(brand)
    if suspicious_brands:
        return (True, 70, f"ဤ URL သည် {', '.join(suspicious_brands)} ၏ အမှတ်တံဆိပ်ကို အတုခိုးထားသည် — တရားဝင် မဟုတ်နိုင်ပါ။")
    return (False, 0, "")


def _rule_domain_numbers(features: Dict) -> RuleResult:
    digit_count = features.get('domain_digit_count', 0)
    if digit_count >= 4:
        return (True, 5, f"Domain တွင် နံပါတ်များ ပုံမှန်မဟုတ်ဘဲ များစွာပါဝင်သည် ({digit_count} လုံး)။")
    return (False, 0, "")


def _rule_idn_homograph(features: Dict) -> RuleResult:
    if features.get('has_idn', 0) == 1:
        return (True, 25, "ဤ domain တွင် IDN Homograph တိုက်ခိုက်မှု ပါဝင်သည်။")
    return (False, 0, "")


def _rule_domain_age(features: Dict) -> RuleResult:
    domain = features.get('domain', '')
    if not domain:
        return (False, 0, "")
    age_days = get_domain_age_days(domain)
    if age_days is not None and age_days < 30:
        return (True, 20, f"Domain သက်တမ်း {age_days} ရက်သာရှိသေးသည် (အသစ်ဖြစ်နိုင်သည်)။")
    return (False, 0, "")


ALL_RULES = [
    _rule_ip_address,
    _rule_suspicious_tld,
    _rule_suspicious_keywords,
    _rule_at_symbol,
    _rule_double_slash_redirect,
    _rule_https_in_path,
    _rule_domain_hyphens,
    _rule_shortener,
    _rule_long_url,
    _rule_brand_impersonation,
    _rule_domain_numbers,
    _rule_idn_homograph,
    _rule_domain_age,
]


def run_rule_engine(features: Dict) -> List[Dict]:
    matched_rules = []
    for rule_func in ALL_RULES:
        triggered, score, reason = rule_func(features)
        if triggered:
            matched_rules.append({
                "rule_name": rule_func.__name__,
                "score": score,
                "reason": reason,
            })
    return matched_rules