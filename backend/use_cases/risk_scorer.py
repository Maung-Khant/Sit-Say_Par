# backend/use_cases/risk_scorer.py
from typing import Dict, List


def calculate_risk_score(matched_rules: List[Dict]) -> int:
    total = sum(rule["score"] for rule in matched_rules)
    return min(total, 100)


def determine_risk_level(score: int) -> str:
    if score >= 80:
        return "Critical"
    elif score >= 60:
        return "High"
    elif score >= 30:
        return "Medium"
    else:
        return "Low"


def generate_risk_assessment(matched_rules: List[Dict]) -> Dict:
    score = calculate_risk_score(matched_rules)
    level = determine_risk_level(score)
    return {
        "risk_score": score,
        "risk_level": level,
        "matched_rules": matched_rules,
        "total_rules_triggered": len(matched_rules),
    }
