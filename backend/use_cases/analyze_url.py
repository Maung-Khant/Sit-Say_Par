# backend/use_cases/analyze_url.py
import re

from backend.core.url import URL
from backend.infrastructure.ml_predictor import ml_predictor
from backend.use_cases.explanation_generator import (
    generate_burmese_explanation, get_detection_confidence)
from backend.use_cases.feature_extractor import extract_features
from backend.use_cases.risk_scorer import (determine_risk_level,
                                           generate_risk_assessment)
from backend.use_cases.rule_engine import run_rule_engine

URL_PATTERN = re.compile(r"(https?://[^\s]+)")


def extract_first_url(text: str) -> str:
    matches = URL_PATTERN.findall(text)
    if matches:
        return matches[0].rstrip(",.;:!?")
    return text.strip()


class AnalyzeURLUseCase:
    def execute(self, url_string: str) -> dict:
        # 1. Extract and validate URL
        clean_url = extract_first_url(url_string)
        if len(clean_url) > 2000:
            raise ValueError("URL is too long (max 2000 characters)")
        url = URL(clean_url)

        # 2. Feature extraction
        features = extract_features(url)

        # 3. Rule engine
        matched_rules = run_rule_engine(features)
        rule_result = generate_risk_assessment(matched_rules)
        rule_score = rule_result["risk_score"]

        # 4. ML prediction (if available)
        ml_prob = ml_predictor.predict_proba(features)
        if ml_prob is not None:
            ml_score = int(ml_prob * 100)
            # Dynamic weighting based on ML confidence
            if ml_prob > 0.9:
                ml_weight = 0.5
            elif ml_prob > 0.7:
                ml_weight = 0.3
            else:
                ml_weight = 0.2
            final_score = int((1 - ml_weight) * rule_score + ml_weight * ml_score)
            final_score = min(final_score, 100)
            if final_score < 1 and (rule_score > 0 or ml_score > 0):
                final_score = 1
        else:
            ml_score = None
            final_score = rule_score

        # Safety fallback: if no rules triggered, ignore ML to prevent false positives
        if rule_score == 0:
            final_score = 0

        level = determine_risk_level(final_score)

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
        result["explanation"] = generate_burmese_explanation(result)
        return result
