from typing import Tuple

CATEGORY_KEYWORDS = {
    'Sanitation': ['garbage','waste','trash','litter','cleaning','sewage','drain','smell','dirty','filthy','hygiene','toilet','sanitation','stench'],
    'Infrastructure': ['road','pothole','bridge','construction','building','wall','pavement','footpath','sidewalk','crack','damage','broken','repair'],
    'Water Supply': ['water','pipe','leak','supply','pump','tap','contamination','shortage','drinking','borewell','tanker','muddy'],
    'Electricity': ['power','electricity','light','outage','blackout','wire','cable','transformer','voltage','electric','streetlight'],
    'Public Safety': ['crime','theft','robbery','assault','accident','safety','police','security','dangerous','threat','violence','harassment'],
    'Healthcare': ['hospital','clinic','medicine','doctor','health','medical','ambulance','patient','treatment','nurse','dispensary'],
    'Education': ['school','college','teacher','education','student','class','book','library','university','classroom'],
    'Transportation': ['bus','traffic','transport','auto','rickshaw','signal','vehicle','route','stop','parking','metro'],
    'Environment': ['pollution','noise','tree','environment','park','garden','smoke','air','chemical','river','deforestation'],
    'Animal Control': ['dog','stray','animal','bite','cattle','pest','mosquito','rat','insect','snake','monkey'],
}

URGENCY_KEYWORDS = {
    'critical': ['emergency','urgent','critical','immediately','life-threatening','dangerous','accident','fire','flood','dying'],
    'high': ['serious','severe','major','terrible','horrible','unacceptable','disgusting','months','years','repeatedly'],
    'low': ['minor','small','slight','sometimes','occasionally','maybe','suggestion','request'],
}

def categorize_complaint(text: str) -> str:
    text_lower = text.lower()
    scores = {cat: sum(1 for kw in kws if kw in text_lower) for cat, kws in CATEGORY_KEYWORDS.items()}
    scores = {k: v for k, v in scores.items() if v > 0}
    return max(scores, key=scores.get) if scores else 'General'

def analyze_urgency(text: str) -> Tuple[str, float]:
    text_lower = text.lower()
    score_map = {'critical': -1.0, 'high': -0.6, 'low': 0.3}
    for level in ['critical', 'high', 'low']:
        if any(kw in text_lower for kw in URGENCY_KEYWORDS[level]):
            return level, score_map[level]
    try:
        from textblob import TextBlob
        polarity = TextBlob(text).sentiment.polarity
        if polarity < -0.5: return 'high', polarity
        elif polarity < -0.1: return 'medium', polarity
        else: return 'low', polarity
    except Exception:
        return 'medium', 0.0

def analyze_complaint(title: str, description: str) -> dict:
    full = f"{title} {description}"
    category = categorize_complaint(full)
    urgency, score = analyze_urgency(full)
    return {'category': category, 'urgency': urgency, 'sentiment_score': round(score, 4)}
