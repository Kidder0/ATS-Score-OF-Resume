from app.schemas.models import KeywordAnalysis, MatchAnalysisResponse
from app.services.evidence import build_evidence_items, fit_level
from app.services.grounding import (
    GUARDRAIL_WARNING,
    build_professional_summary,
    generate_cover_letter,
    rewrite_resume_bullets,
)
from app.services.keyword_extractor import extract_job_keywords
from app.services.llm import LLMClient
from app.services.prompts import JOB_KEYWORD_PROMPT
from app.services.scoring import build_recommendations, score_resume_match


def analyze_match(resume_text: str, job_description: str, resume_id: str | None = None) -> MatchAnalysisResponse:
    job_keywords = _extract_keywords_with_llm_fallback(job_description)
    score, breakdown, matched, missing, weak, weak_areas = score_resume_match(resume_text, job_keywords)
    bullets, _ = rewrite_resume_bullets(resume_text, job_keywords)
    return MatchAnalysisResponse(
        resume_id=resume_id,
        job_keywords=job_keywords,
        match_score=score,
        fit_level=fit_level(score),
        score_breakdown=breakdown,
        evidence=build_evidence_items(resume_text, matched, missing),
        matched_keywords=matched,
        missing_keywords=missing,
        weak_keywords=weak,
        weak_areas=weak_areas,
        recommendations=build_recommendations(missing, weak),
        rewritten_summary=build_professional_summary(resume_text, job_keywords),
        rewritten_bullets=bullets,
        cover_letter=generate_cover_letter(resume_text, job_description, job_keywords),
        guardrail_warning=GUARDRAIL_WARNING,
    )


def _extract_keywords_with_llm_fallback(job_description: str) -> KeywordAnalysis:
    rule_based = extract_job_keywords(job_description)
    llm_payload = LLMClient().complete_json(
        JOB_KEYWORD_PROMPT.format(job_description=job_description)
    )
    if not llm_payload:
        return rule_based
    return KeywordAnalysis(
        skills=_merge(rule_based.skills, llm_payload.get("skills", [])),
        tools=_merge(rule_based.tools, llm_payload.get("tools", [])),
        responsibilities=_merge(rule_based.responsibilities, llm_payload.get("responsibilities", [])),
        education=_merge(rule_based.education, llm_payload.get("education", [])),
        requirements=_merge(rule_based.requirements, llm_payload.get("requirements", [])),
    )


def _merge(left: list[str], right: list[str]) -> list[str]:
    merged: list[str] = []
    for item in left + [str(value) for value in right]:
        clean = item.strip()
        if clean and clean.lower() not in {existing.lower() for existing in merged}:
            merged.append(clean)
    return merged[:16]
