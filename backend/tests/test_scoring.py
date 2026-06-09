from app.services.analyzer import analyze_match


def test_match_score_generation_has_breakdown():
    resume = """
    Built an AI resume analyzer using Python, FastAPI, React, OpenAI, SQL, and RAG.
    Developed prompt engineering workflows and evaluated LLM outputs for accuracy.
    Bachelor of Science in Computer Science.
    """
    jd = """
    Build GenAI and RAG applications using Python, FastAPI, React, OpenAI, SQL, and prompt engineering.
    Bachelor's degree in Computer Science required.
    """

    result = analyze_match(resume, jd)

    assert result.match_score > 70
    assert result.fit_level in {"Good fit", "Strong fit"}
    assert len(result.score_breakdown) == 4
    assert result.evidence
    assert "Python" in result.matched_keywords


def test_no_fabrication_guardrail_labels_genuine_gap():
    resume = "Built Python and React applications for resume analysis. Bachelor of Science in Computer Science."
    jd = "Deploy Kubernetes services on AWS with TensorFlow certification and RAG systems."

    result = analyze_match(resume, jd)

    assert "AWS" in result.missing_keywords
    assert "Kubernetes" in result.missing_keywords
    assert "Do not invent experience" in result.guardrail_warning
    assert "AWS" not in " ".join(result.rewritten_bullets)
