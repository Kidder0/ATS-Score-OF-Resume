from app.schemas.models import KeywordAnalysis, ScoreBreakdownItem
from app.services.similarity import cosine_similarity
from app.services.text_utils import contains_phrase, sentences, unique_preserve_order


WEIGHTS = {
    "Skills match": 40,
    "Tools/technologies match": 25,
    "Experience/responsibility match": 25,
    "Education/certification match": 10,
}


def score_resume_match(resume_text: str, job_keywords: KeywordAnalysis) -> tuple[float, list[ScoreBreakdownItem], list[str], list[str], list[str], list[str]]:
    breakdown = [
        _score_category("Skills match", job_keywords.skills, resume_text),
        _score_category("Tools/technologies match", job_keywords.tools, resume_text),
        _score_category("Experience/responsibility match", job_keywords.responsibilities, resume_text, semantic=True),
        _score_category("Education/certification match", job_keywords.education, resume_text),
    ]
    total = round(sum(item.earned_points for item in breakdown), 1)
    matched = unique_preserve_order([keyword for item in breakdown for keyword in item.matched])
    missing = unique_preserve_order([keyword for item in breakdown for keyword in item.missing])
    weak = unique_preserve_order([
        keyword
        for keyword in missing
        if _weak_keyword(keyword, resume_text)
    ])
    weak_areas = _weak_areas(breakdown)
    return total, breakdown, matched, missing, weak, weak_areas


def _score_category(category: str, keywords: list[str], resume_text: str, semantic: bool = False) -> ScoreBreakdownItem:
    weight = WEIGHTS[category]
    if not keywords:
        return ScoreBreakdownItem(
            category=category,
            weight=weight,
            score=1.0,
            earned_points=weight,
            matched=[],
            missing=[],
            rationale="No explicit requirements were found for this category, so no points were deducted.",
        )

    matched: list[str] = []
    missing: list[str] = []
    partial_credit = 0.0
    for keyword in keywords:
        if contains_phrase(resume_text, keyword):
            matched.append(keyword)
            partial_credit += 1.0
        elif semantic and _semantic_support(resume_text, keyword):
            matched.append(keyword)
            partial_credit += 0.7
        else:
            missing.append(keyword)

    score = partial_credit / len(keywords)
    earned = round(score * weight, 1)
    rationale = (
        f"Matched {len(matched)} of {len(keywords)} detected items. "
        f"Lost {round(weight - earned, 1)} points for missing or weak evidence."
    )
    return ScoreBreakdownItem(
        category=category,
        weight=weight,
        score=round(score, 3),
        earned_points=earned,
        matched=unique_preserve_order(matched),
        missing=unique_preserve_order(missing),
        rationale=rationale,
    )


def _weak_keyword(keyword: str, resume_text: str) -> bool:
    keyword_tokens = [part for part in keyword.lower().replace("/", " ").split() if len(part) > 3]
    return any(token in resume_text.lower() for token in keyword_tokens)


def _semantic_support(resume_text: str, keyword: str) -> bool:
    if cosine_similarity(resume_text, keyword) >= 0.12:
        return True
    return any(cosine_similarity(sentence, keyword) >= 0.22 for sentence in sentences(resume_text))


def _weak_areas(breakdown: list[ScoreBreakdownItem]) -> list[str]:
    areas: list[str] = []
    for item in breakdown:
        if item.score < 0.5:
            areas.append(f"{item.category}: add stronger resume-backed evidence for {', '.join(item.missing[:4])}.")
        elif item.missing:
            areas.append(f"{item.category}: improve coverage for {', '.join(item.missing[:3])}.")
    return areas


def build_recommendations(missing_keywords: list[str], weak_keywords: list[str]) -> list[str]:
    recommendations: list[str] = []
    if weak_keywords:
        recommendations.append(
            "Strengthen weak keywords by connecting them to existing projects, tools, or coursework already in the resume."
        )
    if missing_keywords:
        recommendations.append(
            "Treat unsupported keywords as genuine gaps unless you have resume evidence that can be safely added."
        )
    recommendations.append(
        "Prioritize AI/LLM project bullets that show the problem, tools used, and measurable or observable outcome."
    )
    recommendations.append(
        "Keep tailored bullets concise, truthful, and aligned with the ATS categories shown in the scoring breakdown."
    )
    return recommendations
