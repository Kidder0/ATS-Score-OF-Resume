import re

from app.schemas.models import KeywordAnalysis
from app.services.text_utils import unique_preserve_order


SKILL_TERMS = [
    "machine learning",
    "deep learning",
    "natural language processing",
    "nlp",
    "generative ai",
    "genai",
    "llm",
    "rag",
    "prompt engineering",
    "fine tuning",
    "classification",
    "clustering",
    "model evaluation",
    "data preprocessing",
    "feature engineering",
    "api development",
    "backend development",
    "frontend development",
    "full stack",
    "data analysis",
    "vector search",
]

TOOL_TERMS = [
    "python",
    "typescript",
    "javascript",
    "react",
    "fastapi",
    "flask",
    "django",
    "node.js",
    "sql",
    "postgresql",
    "sqlite",
    "mongodb",
    "docker",
    "kubernetes",
    "aws",
    "azure",
    "gcp",
    "openai",
    "gemini",
    "langchain",
    "llamaindex",
    "hugging face",
    "sentence transformers",
    "pytorch",
    "tensorflow",
    "scikit-learn",
    "pandas",
    "numpy",
    "pinecone",
    "chroma",
    "faiss",
    "git",
    "github",
]

EDUCATION_TERMS = [
    "bachelor",
    "master",
    "computer science",
    "data science",
    "artificial intelligence",
    "machine learning",
    "certification",
    "degree",
]

RESPONSIBILITY_PATTERNS = [
    r"(?:build|develop|implement|design|deploy|integrate|evaluate|optimize|maintain|collaborate|create|automate)[^.\n]{8,120}",
    r"(?:experience|responsible|work(?:ed)? with|hands-on)[^.\n]{8,120}",
]


def extract_job_keywords(job_description: str) -> KeywordAnalysis:
    text = job_description.lower()
    skills = _extract_terms(text, SKILL_TERMS)
    tools = _extract_terms(text, TOOL_TERMS)
    education = _extract_terms(text, EDUCATION_TERMS)
    responsibilities = _extract_responsibilities(job_description)
    requirements = _extract_requirements(job_description)
    return KeywordAnalysis(
        skills=skills,
        tools=tools,
        responsibilities=responsibilities,
        education=education,
        requirements=requirements,
    )


def _extract_terms(text: str, terms: list[str]) -> list[str]:
    matches: list[str] = []
    for term in terms:
        escaped = re.escape(term)
        if re.search(rf"(?<!\w){escaped}(?!\w)", text):
            matches.append(_display_term(term))
    return unique_preserve_order(matches)


def _extract_responsibilities(job_description: str) -> list[str]:
    matches: list[str] = []
    for pattern in RESPONSIBILITY_PATTERNS:
        matches.extend(re.findall(pattern, job_description, flags=re.IGNORECASE))
    bullet_lines = [
        line.strip(" -*\t")
        for line in job_description.splitlines()
        if line.strip().startswith(("-", "*", "•"))
    ]
    matches.extend(bullet_lines)
    return unique_preserve_order(matches)[:12]


def _extract_requirements(job_description: str) -> list[str]:
    requirements: list[str] = []
    for line in job_description.splitlines():
        clean = line.strip(" -*\t")
        if re.search(r"\b(required|required|must|preferred|qualification|experience|degree)\b", clean, re.I):
            requirements.append(clean)
    return unique_preserve_order(requirements)[:12]


def _display_term(term: str) -> str:
    mapping = {
        "nlp": "NLP",
        "llm": "LLM",
        "rag": "RAG",
        "genai": "GenAI",
        "api development": "API development",
        "fastapi": "FastAPI",
        "langchain": "LangChain",
        "hugging face": "Hugging Face",
        "chroma": "Chroma",
        "faiss": "FAISS",
        "node.js": "Node.js",
        "sql": "SQL",
        "aws": "AWS",
        "azure": "Azure",
        "gcp": "GCP",
        "openai": "OpenAI",
        "typescript": "TypeScript",
        "javascript": "JavaScript",
        "postgresql": "PostgreSQL",
    }
    return mapping.get(term, term.title())
