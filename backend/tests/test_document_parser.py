from pathlib import Path

from docx import Document
from reportlab.pdfgen import canvas

from app.services.document_parser import extract_resume_text


def test_pdf_parsing(tmp_path: Path):
    pdf_path = tmp_path / "resume.pdf"
    c = canvas.Canvas(str(pdf_path))
    c.drawString(72, 720, "AI Engineer resume with Python, FastAPI, OpenAI, and RAG projects.")
    c.save()

    text = extract_resume_text(pdf_path)

    assert "Python" in text
    assert "RAG" in text


def test_docx_parsing(tmp_path: Path):
    docx_path = tmp_path / "resume.docx"
    document = Document()
    document.add_paragraph("Built GenAI tools using React, TypeScript, Python, and vector search.")
    document.save(docx_path)

    text = extract_resume_text(docx_path)

    assert "GenAI" in text
    assert "TypeScript" in text

