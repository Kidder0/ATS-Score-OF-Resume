import re

from app.schemas.models import KeywordAnalysis
from app.services.text_utils import contains_phrase, sentences, unique_preserve_order


GUARDRAIL_WARNING = (
    "Do not invent experience. Suggestions are grounded in the uploaded resume; "
    "unsupported JD keywords are labeled as genuine gaps."
)


def classify_keyword_support(resume_text: str, keywords: list[str]) -> tuple[list[str], list[str]]:
    matched: list[str] = []
    gaps: list[str] = []
    for keyword in keywords:
        if contains_phrase(resume_text, keyword):
            matched.append(keyword)
        else:
            gaps.append(keyword)
    return unique_preserve_order(matched), unique_preserve_order(gaps)


def build_professional_summary(resume_text: str, job_keywords: KeywordAnalysis) -> str:
    matched, _ = classify_keyword_support(resume_text, job_keywords.skills + job_keywords.tools)
    focus = ", ".join(matched[:6]) or "software development, data analysis, and AI project work"
    role = "Entry-level AI Engineer / GenAI Developer"
    evidence = _best_resume_sentence(resume_text, matched)
    if evidence:
        return (
            f"{role} candidate with resume-backed experience in {focus}. "
            f"Relevant evidence: {evidence}"
        )
    return f"{role} candidate with resume-supported experience in {focus}."


def rewrite_resume_bullets(resume_text: str, job_keywords: KeywordAnalysis, max_bullets: int = 6) -> tuple[list[str], list[str]]:
    all_keywords = job_keywords.skills + job_keywords.tools + job_keywords.responsibilities
    matched, gaps = classify_keyword_support(resume_text, all_keywords)
    source_sentences = sentences(resume_text)
    selected: list[str] = []

    for sentence in source_sentences:
        if any(contains_phrase(sentence, keyword) for keyword in matched):
            selected.append(sentence)

    if not selected:
        selected = source_sentences[:max_bullets]

    bullets: list[str] = []
    for sentence in selected[:max_bullets]:
        cleaned = _clean_bullet_source(sentence)
        bullets.append(_rewrite_bullet(cleaned, matched))
    return unique_preserve_order(bullets)[:max_bullets], gaps


def generate_cover_letter(resume_text: str, job_description: str, job_keywords: KeywordAnalysis) -> str:
    matched, gaps = classify_keyword_support(resume_text, _all_keywords(job_keywords))
    focus = ", ".join(matched[:5]) or "AI application development"
    evidence = _best_resume_sentence(resume_text, matched)
    gap_sentence = ""
    if gaps:
        gap_sentence = (
            " I would also treat "
            + ", ".join(gaps[:3])
            + " as growth areas unless my resume evidence can support them."
        )
    return (
        "Dear Hiring Team,\n\n"
        "I am excited to apply for your AI engineering role. My resume shows hands-on "
        f"experience aligned with {focus}. "
        f"{evidence if evidence else 'I have built practical technical projects and collaborated across software workflows.'} "
        "I would bring a grounded, implementation-focused approach to building reliable "
        "LLM and GenAI applications while keeping outputs truthful and user-focused."
        f"{gap_sentence}\n\n"
        "Thank you for your time and consideration.\n"
        "Sincerely,\n"
        "Candidate"
    )


def _all_keywords(job_keywords: KeywordAnalysis) -> list[str]:
    return unique_preserve_order(
        job_keywords.skills
        + job_keywords.tools
        + job_keywords.responsibilities
        + job_keywords.education
    )


def _best_resume_sentence(resume_text: str, keywords: list[str]) -> str:
    candidates = sentences(resume_text)
    if not candidates:
        return ""
    ranked = sorted(
        candidates,
        key=lambda sentence: sum(1 for keyword in keywords if contains_phrase(sentence, keyword)),
        reverse=True,
    )
    return ranked[0]


def _clean_bullet_source(sentence: str) -> str:
    cleaned = re.sub(r"^[•*\-]\s*", "", sentence).strip()
    cleaned = re.sub(r"\s+", " ", cleaned)
    return cleaned.rstrip(".")


def _keyword_hint(sentence: str, matched_keywords: list[str]) -> str:
    hints = [keyword for keyword in matched_keywords if contains_phrase(sentence, keyword)]
    return ", ".join(hints[:2])


def _rewrite_bullet(sentence: str, matched_keywords: list[str]) -> str:
    clean = sentence.strip()
    if not clean:
        return clean
    if re.match(r"^(built|developed|implemented|designed|optimized|created|deployed|integrated|analyzed|automated)\b", clean, re.I):
        return clean[0].upper() + clean[1:]
    hint = _keyword_hint(clean, matched_keywords)
    if hint:
        return f"Strengthened {hint} experience through resume-backed work: {clean[0].lower() + clean[1:]}"
    return f"Improved technical delivery through resume-backed work: {clean[0].lower() + clean[1:]}"
