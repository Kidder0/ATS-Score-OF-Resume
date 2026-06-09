from app.services.tailored_resume import build_tailored_resume, render_tailored_resume_markdown
from fastapi.testclient import TestClient

from app.main import app


def test_tailored_resume_keeps_unsupported_gaps_out_of_resume_body():
    resume = """
    Rakesh Candidate
    Built Python, FastAPI, React, OpenAI, and RAG applications.
    Bachelor of Science in Computer Science.
    """
    jd = "Build RAG applications with Python, Kubernetes, AWS, TensorFlow, and LangChain."

    tailored = build_tailored_resume(resume, jd)
    markdown = render_tailored_resume_markdown(tailored)
    resume_body = markdown.split("## Truthfulness Review")[0]

    assert "Python" in resume_body
    assert "RAG" in resume_body
    assert "Kubernetes" not in resume_body
    assert "AWS" not in resume_body
    assert "Do not add" in markdown


def test_tailored_resume_preview_endpoint_returns_gap_plan():
    client = TestClient(app)
    response = client.post(
        "/api/tailored-resume",
        json={
            "resume_text": "Built Python, FastAPI, React, OpenAI, and RAG applications.",
            "job_description": "Build RAG apps with Python, AWS, Kubernetes, and LangChain.",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["rewritten_bullets"]
    assert body["gap_action_plan"]


def test_tailored_resume_name_parser_keeps_candidate_name():
    tailored = build_tailored_resume(
        "# Rakesh Candidate\n\nSkills\n- Python, TypeScript, SQL\n\nBuilt Python apps.",
        "Build Python applications.",
    )

    assert tailored["name"] == "Rakesh Candidate"


def test_tailored_resume_preserves_uploaded_section_headings():
    resume = """
    RAKESH REDDY JAMMULADINNE

    SUMMARY
    Frontend Software Engineer with SQL and React experience.

    TECHNICAL SKILLS
    JavaScript, TypeScript, React, SQL

    PROJECTS
    Built SQL-backed REST APIs for product catalog and inventory records.

    EDUCATION
    University of North Texas - MS in Cybersecurity, 2025
    """
    tailored = build_tailored_resume(
        resume,
        "Build GenAI apps with Python, SQL, React, AWS, Kubernetes, and LangChain.",
    )
    titles = [section["section_title"] for section in tailored["section_suggestions"]]
    markdown = render_tailored_resume_markdown(tailored)
    resume_body = markdown.split("## Truthfulness Review")[0]

    assert "Summary" in titles
    assert "Technical Skills" in titles
    assert "Projects" in titles
    assert "Education" in titles
    assert "AWS" not in resume_body
    assert "Kubernetes" not in resume_body
    assert "Degree" not in tailored["supported_keywords"]
