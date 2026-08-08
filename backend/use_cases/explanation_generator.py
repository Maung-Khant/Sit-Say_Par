# backend/use_cases/explanation_generator.py
from typing import Dict

def get_confidence_level(risk_assessment: Dict) -> str:
    """Determine confidence level based on ML probability and rule triggers."""
    ml_score = risk_assessment.get('ml_score')
    rule_count = risk_assessment.get('total_rules_triggered', 0)

    if ml_score is not None:
        if ml_score >= 90 and rule_count >= 3:
            return "High"
        elif ml_score >= 70 or rule_count >= 2:
            return "Medium"
        else:
            return "Low"
    else:
        # No ML model – use rule count only
        if rule_count >= 3:
            return "High"
        elif rule_count >= 2:
            return "Medium"
        else:
            return "Low"

def generate_burmese_explanation(risk_assessment: Dict) -> str:
    score = risk_assessment['risk_score']
    level = risk_assessment['risk_level']
    rules = risk_assessment.get('matched_rules', [])
    ml_score = risk_assessment.get('ml_score')
    confidence = get_confidence_level(risk_assessment)

    level_map = {
        "Low": "နည်းပါးသည်",
        "Medium": "အလယ်အလတ်",
        "High": "မြင့်မားသည်",
        "Critical": "အလွန်မြင့်မားသည်"
    }
    burmese_level = level_map.get(level, level)

    explanation = f"ဤ URL ၏ အန္တရာယ်ရှိမှု အဆင့်မှာ **{burmese_level}** (ရမှတ် {score}/100) ဖြစ်သည်။\n"

    # Confidence indicator
    confidence_map = {"High": "မြင့်မား", "Medium": "အလယ်အလတ်", "Low": "နည်းပါး"}
    explanation += f"ယုံကြည်စိတ်ချရမှု အဆင့်: **{confidence_map[confidence]}**\n\n"

    if ml_score is not None:
        explanation += f"(ML ခန့်မှန်းချက် - {ml_score}/100)\n\n"

    if level == "Low":
        explanation += "ဤ URL တွင် သံသယဖြစ်ဖွယ် အချက်အလက်များ မတွေ့ရှိပါ။\n"
    else:
        explanation += "အောက်ပါ အကြောင်းအရင်းများကြောင့် သတိထားသင့်သည်။\n\n"
        for i, rule in enumerate(rules, 1):
            explanation += f"{i}. {rule['reason']}\n"

    explanation += "\n**အကြံပြုချက်:**\n"
    if level in ("High", "Critical"):
        explanation += (
            "• ဤလင့်ခ်ကို မဖွင့်မိပါစေနှင့်။\n"
            "• ကိုယ်ရေးအချက်အလက်များ (စကားဝှက်၊ ဘဏ်အချက်အလက်) ထည့်သွင်းခြင်းကို ရှောင်ကြဉ်ပါ။\n"
            "• သံသယရှိပါက ဆက်သွယ်ရေးလိပ်စာများကို တိုက်ရိုက်ရှာဖွေ၍ ဆက်သွယ်ပါ။"
        )
    elif level == "Medium":
        explanation += (
            "• ဤလင့်ခ်ကို မဖွင့်မီ သေချာစဉ်းစားပါ။\n"
            "• ဆိုက်၏ လိပ်စာသည် တရားဝင်ဟုတ်မဟုတ် ပြန်လည်စစ်ဆေးပါ။"
        )
    else:
        explanation += "• ဤ URL သည် အန္တရာယ်နည်းပါးသော်လည်း အမြဲသတိထားပါ။"

    return explanation