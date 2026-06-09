from app.services.keyword_extractor import extract_job_keywords


def test_keyword_extraction_detects_ai_role_terms():
    jd = """
    We need an entry-level GenAI Developer to build RAG applications with Python,
    FastAPI, React, OpenAI, vector search, SQL, and prompt engineering.
    Bachelor's degree in Computer Science preferred.
    """

    keywords = extract_job_keywords(jd)

    assert "RAG" in keywords.skills
    assert "Python" in keywords.tools
    assert "Fastapi" in keywords.tools or "FastAPI" in keywords.tools
    assert "Computer Science" in keywords.education

