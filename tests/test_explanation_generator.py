# tests/test_explanation_generator.py
from backend.use_cases.explanation_generator import \
    generate_burmese_explanation


def test_generate_explanation_low():
    assessment = {"risk_score": 10, "risk_level": "Low", "matched_rules": []}
    explanation = generate_burmese_explanation(assessment)
    assert "နည်းပါးသည်" in explanation
    assert "သံသယဖြစ်ဖွယ် အချက်အလက်များ မတွေ့ရှိပါ" in explanation


def test_generate_explanation_high():
    assessment = {
        "risk_score": 75,
        "risk_level": "High",
        "matched_rules": [
            {
                "rule_name": "r1",
                "score": 30,
                "reason": "IP လိပ်စာကို တိုက်ရိုက်သုံးထားသည်",
            },
            {"rule_name": "r2", "score": 25, "reason": "သံသယဖြစ်ဖွယ် TLD"},
        ],
    }
    explanation = generate_burmese_explanation(assessment)
    assert "မြင့်မားသည်" in explanation
    assert "IP လိပ်စာကို တိုက်ရိုက်သုံးထားသည်" in explanation
    assert "မဖွင့်မိပါစေနှင့်" in explanation


def test_generate_explanation_medium():
    assessment = {
        "risk_score": 45,
        "risk_level": "Medium",
        "matched_rules": [
            {
                "rule_name": "r1",
                "score": 20,
                "reason": "လမ်းကြောင်းထဲတွင် '//' ပါဝင်သည်",
            }
        ],
    }
    explanation = generate_burmese_explanation(assessment)
    assert "အလယ်အလတ်" in explanation
    assert "မဖွင့်မီ သေချာစဉ်းစားပါ" in explanation
