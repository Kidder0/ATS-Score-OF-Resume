import logging
from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import Response

from app.core.config import get_settings
from app.schemas.models import (
    AnalyzeRequest,
    CoverLetterRequest,
    CoverLetterResponse,
    ExportRequest,
    ResumeUploadResponse,
    RewriteRequest,
    RewriteResponse,
    TailoredResumeRequest,
    TailoredResumeResponse,
)
from app.services.analyzer import analyze_match
from app.services.document_parser import DocumentParseError, extract_resume_text, validate_upload
from app.services.exporter import render_docx_report, render_markdown_report
from app.services.grounding import GUARDRAIL_WARNING, generate_cover_letter, rewrite_resume_bullets
from app.services.keyword_extractor import extract_job_keywords
from app.services.resume_store import resume_store
from app.services.tailored_resume import (
    build_tailored_resume,
    render_tailored_resume_docx,
    render_tailored_resume_markdown,
)


logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/upload-resume", response_model=ResumeUploadResponse)
async def upload_resume(file: UploadFile = File(...)) -> ResumeUploadResponse:
    settings = get_settings()
    content = await file.read()
    try:
        validate_upload(file.filename or "", file.content_type, len(content), settings.max_upload_bytes)
    except DocumentParseError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    extension = Path(file.filename or "").suffix.lower()
    temp_path = settings.upload_dir / f"{uuid4()}{extension}"
    try:
        temp_path.write_bytes(content)
        text = extract_resume_text(temp_path)
    except DocumentParseError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    finally:
        temp_path.unlink(missing_ok=True)

    resume_id = resume_store.put(text, file.filename or "resume")
    logger.info("Uploaded and parsed resume %s", file.filename)
    return ResumeUploadResponse(
        resume_id=resume_id,
        filename=file.filename or "resume",
        text=text,
        preview=text[:1200],
        character_count=len(text),
    )


@router.post("/analyze-match")
def analyze(request: AnalyzeRequest):
    resume_text = _resolve_resume_text(request.resume_id, request.resume_text)
    return analyze_match(resume_text, request.job_description, request.resume_id)


@router.post("/rewrite-bullets", response_model=RewriteResponse)
def rewrite_bullets(request: RewriteRequest) -> RewriteResponse:
    resume_text = _resolve_resume_text(request.resume_id, request.resume_text)
    keywords = extract_job_keywords(request.job_description)
    bullets, gaps = rewrite_resume_bullets(resume_text, keywords, request.max_bullets)
    return RewriteResponse(bullets=bullets, genuine_gaps=gaps, guardrail_warning=GUARDRAIL_WARNING)


@router.post("/generate-cover-letter", response_model=CoverLetterResponse)
def cover_letter(request: CoverLetterRequest) -> CoverLetterResponse:
    resume_text = _resolve_resume_text(request.resume_id, request.resume_text)
    keywords = extract_job_keywords(request.job_description)
    return CoverLetterResponse(
        cover_letter=generate_cover_letter(resume_text, request.job_description, keywords),
        guardrail_warning=GUARDRAIL_WARNING,
    )


@router.post("/export")
def export_report(request: ExportRequest):
    if request.format == "markdown":
        content = render_markdown_report(request.report)
        return Response(
            content=content,
            media_type="text/markdown",
            headers={"Content-Disposition": 'attachment; filename="match-report.md"'},
        )
    buffer = render_docx_report(request.report)
    return Response(
        content=buffer.getvalue(),
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={"Content-Disposition": 'attachment; filename="match-report.docx"'},
    )


@router.post("/export-tailored-resume")
def export_tailored_resume(request: TailoredResumeRequest):
    resume_text = _resolve_resume_text(request.resume_id, request.resume_text)
    tailored_resume = build_tailored_resume(resume_text, request.job_description)
    if request.format == "markdown":
        content = render_tailored_resume_markdown(tailored_resume)
        return Response(
            content=content,
            media_type="text/markdown",
            headers={"Content-Disposition": 'attachment; filename="tailored-resume.md"'},
        )
    buffer = render_tailored_resume_docx(tailored_resume)
    return Response(
        content=buffer.getvalue(),
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={"Content-Disposition": 'attachment; filename="tailored-resume.docx"'},
    )


@router.post("/tailored-resume", response_model=TailoredResumeResponse)
def tailored_resume_preview(request: AnalyzeRequest) -> TailoredResumeResponse:
    resume_text = _resolve_resume_text(request.resume_id, request.resume_text)
    return TailoredResumeResponse(**build_tailored_resume(resume_text, request.job_description))


def _resolve_resume_text(resume_id: str | None, resume_text: str | None) -> str:
    if resume_text and len(resume_text.strip()) >= 40:
        return resume_text.strip()
    if resume_id:
        stored = resume_store.get(resume_id)
        if stored:
            return stored.text
    raise HTTPException(status_code=404, detail="Resume text was not found. Upload a resume again.")
