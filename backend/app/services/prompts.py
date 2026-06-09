SYSTEM_GUARDRAIL = """
You are an AI resume tailoring assistant. Use only the uploaded resume as the source of truth.
Never invent skills, companies, dates, certifications, degrees, metrics, publications, or experience.
If the job description asks for something not supported by the resume, label it as a genuine gap.
When adding ATS keywords, only add a keyword when the resume provides clear supporting evidence.
Keep all suggestions truthful, concise, and appropriate for an entry-level AI Engineer, GenAI Developer, or LLM Application Developer role.
""".strip()


JOB_KEYWORD_PROMPT = """
Extract job-description requirements into JSON with keys:
skills, tools, responsibilities, education, requirements.
Return only JSON arrays of short phrases.

Job description:
{job_description}
""".strip()


BULLET_REWRITE_PROMPT = """
Rewrite resume bullets for the target job using only the candidate resume below.
Use action verbs, impact language, and ATS keywords only when supported by resume evidence.
Return JSON: {{"bullets": [], "genuine_gaps": []}}.

Resume:
{resume_text}

Job keywords:
{job_keywords}
""".strip()


COVER_LETTER_PROMPT = """
Write a short, tailored cover letter for the target role using only the uploaded resume as evidence.
Do not add unsupported claims. Keep it under 220 words.

Resume:
{resume_text}

Job description:
{job_description}
""".strip()

