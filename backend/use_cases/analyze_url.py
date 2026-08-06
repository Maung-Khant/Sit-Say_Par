# backend/use_cases/analyze_url.py
import re
from backend.core.url import URL
from backend.use_cases.feature_extractor import extract_features
from backend.use_cases.rule_engine import run_rule_engine
from backend.use_cases.risk_scorer import generate_risk_assessment, determine_risk_level
from backend.use_cases.explanation_generator import generate_burmese_explanation
from backend.infrastructure.ml_predictor import ml_predictor

URL_PATTERN = re.compile(r'(https?://[^\s]+)')

def extract_first_url(text: str) -> str:
    matches = URL_PATTERN.findall(text)
    if matches:
        return matches[0].rstrip(',.;:!?')
    return text.strip()

class AnalyzeURLUseCase:
    def execute(self, url_string: str) -> dict:
        # 1. Extract and validate URL
        clean_url = extract_first_url(url_string)
        url = URL(clean_url)

        # 2. Feature extraction
        features = extract_features(url)

        # 3. Rule engine
        matched_rules = run_rule_engine(features)
        rule_result = generate_risk_assessment(matched_rules)
        rule_score = rule_result['risk_score']

        # 4. ML prediction (if available)
        ml_prob = ml_predictor.predict_proba(features)
        if ml_prob is not None:
            ml_score = int(ml_prob * 100)
            # Weighted combination: 80% rule, 20% ML (prioritize explainability)
            final_score = int(0.8 * rule_score + 0.2 * ml_score)
            final_score = min(final_score, 100)
            if final_score < 1 and (rule_score > 0 or ml_score > 0):
                final_score = 1
        else:
            ml_score = None
            final_score = rule_score

        # 5. Determine risk level from final score
        level = determine_risk_level(final_score)

        # Build result
        result = {
            "url": str(url),
            "risk_score": final_score,
            "risk_level": level,
            "total_rules_triggered": len(matched_rules),
            "matched_rules": matched_rules,
            "features": features,
            "ml_score": ml_score,
            "rule_score": rule_score,
        }
        # Add explanation (now includes ml_score if available)
        result["explanation"] = generate_burmese_explanation(result)
        return result