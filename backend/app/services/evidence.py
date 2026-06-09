from app.schemas.models import EvidenceItem
from app.services.text_utils import contains_phrase, sentences, unique_preserve_order


def build_evidence_items(resume_text: str, matched: list[str], missing: list[str]) -> list[EvidenceItem]:
    items: list[EvidenceItem] = []
    for keyword in matched[:14]:
        items.append(
            EvidenceItem(
                keyword=keyword,
                status="matched",
                evidence=_find_evidence_sentence(resume_text, keyword),
                recommendation="Keep this keyword tied to the resume evidence shown.",
            )
        )
    for keyword in missing[:14]:
        items.append(
            EvidenceItem(
                keyword=keyword,
                status="gap",
                evidence=None,
                recommendation="Label as a genuine gap unless the resume has evidence that can support it.",
            )
        )
    return items


def fit_level(score: float) -> str:
    if score >= 85:
        return "Strong fit"
    if score >= 70:
        return "Good fit"
    if score >= 55:
        return "Partial fit"
    return "Needs targeting"


def _find_evidence_sentence(resume_text: str, keyword: str) -> str | None:
    candidates = sentences(resume_text)
    exact = [sentence for sentence in candidates if contains_phrase(sentence, keyword)]
    if exact:
        return exact[0]
    keyword_tokens = unique_preserve_order(keyword.split())
    for sentence in candidates:
        if any(contains_phrase(sentence, token) for token in keyword_tokens):
            return sentence
    return None

