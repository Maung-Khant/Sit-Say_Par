import json
import time
import urllib.request
import urllib.error

#API_URL = "https://sit-say-par.onrender.com/analyze"   # Render
API_URL = "http://localhost:8000/analyze"            # Local

urls = [
    # Legitimate
    "https://www.google.com",
    "https://www.kbzbank.com",
    "https://www.kbzpay.com",
    "https://www.cbbank.com.mm",
    "https://www.abank.com.mm",
    "https://www.wavemoney.com.mm",
    "https://www.mpt.com.mm",
    "https://www.wikipedia.org",

    # Bare domains -> will be prefixed with http://
    "kbzbanks.co", "kbzbank.cc", "bank.party", "kbsbank.com", "kbzbank.net",
    "kbzbank.app", "kbzbnk.com", "bank.ml", "kbzbank.biz", "k.win",
    "kbzbank.info", "kbzbank.org", "bank.green", "ico.ai", "co.pub",
    "co.cc", "kbzbank.xyz", "bzbank.co", "kbbank.ai", "kbzbank.link",
    "kbz-bank.com", "kzbank.com", "kbzibank.com", "kbzbanks.com", "co.info",
    "k.biz", "co.sk", "kbzbank-me.xico.ru", "kbz.bank.works", "kbzbankmex.ico.pt",
    "kbzbank-mex.ico.pt", "kbzbank-mexi.co.pt", "bank.win", "bzbank.com",
    "bank.info", "kbzbankme.xico.mx", "bank.pub", "kbzbankmexi.co.pt", "xico.cc",
    "xico.nl", "co.club", "exico.info", "kbzbank-me.xico.mx", "k.casa",
    "bank.ie", "kbzbank.co", "ico.club", "kbbank.ru", "kbhbank.com",
    "kbebank.com", "nk.club", "co.casa", "bank.beer", "zbank.io",
    "exico.sk", "ico.biz", "kbbank.com", "exico.us", "co.works",
    "zbank.us", "bzbank.com.br", "co.beer", "zbank.ru", "co.biz",
    "bank.top", "exico.xyz", "k.cc", "k.beer", "cbzbank.com",
    "ank.ru", "kbzbankme.xico.ru", "ico.pw", "ank.be", "nk.sk",
    "kbzbank.site", "kbrbank.ru", "nk.au", "kzbank.ru", "ank.au",

    # Already have scheme
    "https://kbzpay-level2-upgrade.com",
    "https://wavemoney-free-bonus.com/claim",
    "https://facebook-security-login-auth.net/profile",
    "https://kbzpay.workers.dev/login",
    "https://mytel-lucky-draw-winner-2026.test",
    "https://meta-policy-support-team.com",
    "https://kpay-bonus-claim.com",
    "https://mm-immigration-evisa-fake.test",
]

def normalize_url(u):
    if u.startswith("http://") or u.startswith("https://"):
        return u
    return "http://" + u

def send_url(url):
    data = json.dumps({"url": url}).encode('utf-8')
    req = urllib.request.Request(API_URL, data=data, headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        return {"error": f"HTTP {e.code}"}
    except Exception as e:
        return {"error": str(e)}

def main():
    print(f"{'URL':<45} {'Level':<10} {'Score':<6} {'Conf':<10} Rules")
    print("="*110)
    for u in urls:
        nu = normalize_url(u)
        result = send_url(nu)
        if 'error' in result:
            print(f"{nu:<45} ERROR: {result['error']}")
        else:
            level = result.get('risk_level', '?')
            score = result.get('risk_score', '?')
            conf = result.get('detection_confidence', '?')
            rules = result.get('total_rules_triggered', 0)
            rule_names = [m['rule_name'].replace('_rule_', '') for m in result.get('matched_rules', [])]
            print(f"{nu:<45} {level:<10} {score:<6} {conf:<10} {rules} ({', '.join(rule_names)})")
        time.sleep(2)  # reduce request frequency to avoid 429
    print("\nDone.")

if __name__ == "__main__":
    main()