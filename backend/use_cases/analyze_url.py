# backend/use_cases/analyze_url.py
import re
from backend.core.url import URL
from backend.use_cases.feature_extractor import extract_features
from backend.use_cases.rule_engine import run_rule_engine
from backend.use_cases.risk_scorer import generate_risk_assessment
from backend.use_cases.explanation_generator import generate_burmese_explanation

# Simple URL extraction regex (matches http/https URLs)
URL_PATTERN = re.compile(r'(https?://[^\s]+)')

def extract_first_url(text: str) -> str:
    """Return the first URL found in the text, or the original text if no URL."""
    matches = URL_PATTERN.findall(text)
    if matches:
        return matches[0].rstrip(',.;:!?')
    return text.strip()

class AnalyzeURLUseCase:
    def execute(self, url_string: str) -> dict:
        # 1. Extract URL from mixed text
        clean_url = extract_first_url(url_string)

        # 2. Validate and parse URL
        url = URL(clean_url)

        # 3. Extract features
        features = extract_features(url)

        # 4. Run rule engine
        matched_rules = run_rule_engine(features)

        # 5. Generate risk assessment
        result = generate_risk_assessment(matched_rules)

        # 6. Add explanation in Burmese
        result["explanation"] = generate_burmese_explanation(result)

        # 7. Add additional info
        result["url"] = str(url)
        result["features"] = features
        return result