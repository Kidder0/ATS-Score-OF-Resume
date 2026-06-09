from pydantic import BaseModel, Field


class ResumeUploadResponse(BaseModel):
    resume_id: str
    filename: str
    text: str
    preview: str
    character_count: int


class AnalyzeRequest(BaseModel):
    job_description: str = Field(..., min_length=40)
    resume_id: str | None = None
    resume_text: str | None = None


class RewriteRequest(AnalyzeRequest):
    max_bullets: int = Field(default=6, ge=1, le=12)


class CoverLetterRequest(AnalyzeRequest):
    tone: str = "professional"


class ExportRequest(BaseModel):
    format: str = Field(default="markdown", pattern="^(markdown|docx)$")
    report: dict


class TailoredResumeRequest(AnalyzeRequest):
    format: str = Field(default="docx", pattern="^(markdown|docx)$")


class TailoredResumeResponse(BaseModel):
    name: str
    contact_lines: list[str]
    target_title: str
    summary: str
    supported_keywords: list[str]
    rewritten_bullets: list[str]
    project_or_experience_lines: list[str]
    education_lines: list[str]
    match_score: float
    matched_keywords: list[str]
    missing_keywords: list[str]
    weak_keywords: list[str]
    weak_areas: list[str]
    genuine_gaps: list[str]
    guardrail_warning: str
    gap_action_plan: list[str]
    section_suggestions: list[dict]
    preserved_format_note: str


class KeywordAnalysis(BaseModel):
    skills: list[str]
    tools: list[str]
    responsibilities: list[str]
    education: list[str]
    requirements: list[str]


class ScoreBreakdownItem(BaseModel):
    category: str
    weight: int
    score: float
    earned_points: float
    matched: list[str]
    missing: list[str]
    rationale: str


class EvidenceItem(BaseModel):
    keyword: str
    status: str
    evidence: str | None = None
    recommendation: str


class MatchAnalysisResponse(BaseModel):
    resume_id: str | None = None
    job_keywords: KeywordAnalysis
    match_score: float
    fit_level: str
    score_breakdown: list[ScoreBreakdownItem]
    evidence: list[EvidenceItem]
    matched_keywords: list[str]
    missing_keywords: list[str]
    weak_keywords: list[str]
    weak_areas: list[str]
    recommendations: list[str]
    rewritten_summary: str
    rewritten_bullets: list[str]
    cover_letter: str
    guardrail_warning: str


class RewriteResponse(BaseModel):
    bullets: list[str]
    guardrail_warning: str
    genuine_gaps: list[str]


class CoverLetterResponse(BaseModel):
    cover_letter: str
    guardrail_warning: str
