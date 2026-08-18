import pytest

from backend.use_cases.risk_scorer import (calculate_risk_score,
                                           determine_risk_level,
                                           generate_risk_assessment)


def test_calculate_risk_score_empty():
    assert calculate_risk_score([]) == 0


def test_calculate_risk_score_multiple():
    rules = [
        {"rule_name": "r1", "score": 30, "reason": ""},
        {"rule_name": "r2", "score": 25, "reason": ""},
    ]
    assert calculate_risk_score(rules) == 55


def test_calculate_risk_score_capped():
    rules = [{"rule_name": "r1", "score": 90}, {"rule_name": "r2", "score": 30}]
    assert calculate_risk_score(rules) == 100


def test_determine_risk_level():
    assert determine_risk_level(10) == "Low"
    assert determine_risk_level(40) == "Medium"
    assert determine_risk_level(70) == "High"
    assert determine_risk_level(90) == "Critical"


def test_generate_risk_assessment():
    rules = [{"rule_name": "test_rule", "score": 40, "reason": "Test reason"}]
    result = generate_risk_assessment(rules)
    assert result["risk_score"] == 40
    assert result["risk_level"] == "Medium"
    assert result["total_rules_triggered"] == 1
