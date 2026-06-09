import json
import logging
from typing import Any

from app.core.config import get_settings
from app.services.prompts import SYSTEM_GUARDRAIL


logger = logging.getLogger(__name__)


class LLMClient:
    def __init__(self) -> None:
        self.settings = get_settings()

    def complete_json(self, prompt: str) -> dict[str, Any] | None:
        content = self.complete(prompt)
        if not content:
            return None
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            logger.warning("LLM returned non-JSON content")
            return None

    def complete(self, prompt: str) -> str | None:
        provider = self.settings.ai_provider.lower()
        if provider == "openai" and self.settings.openai_api_key:
            return self._openai_complete(prompt)
        if provider == "gemini" and self.settings.google_api_key:
            return self._gemini_complete(prompt)
        return None

    def _openai_complete(self, prompt: str) -> str | None:
        try:
            from openai import OpenAI

            client = OpenAI(api_key=self.settings.openai_api_key)
            response = client.chat.completions.create(
                model=self.settings.openai_model,
                temperature=0.2,
                messages=[
                    {"role": "system", "content": SYSTEM_GUARDRAIL},
                    {"role": "user", "content": prompt},
                ],
            )
            return response.choices[0].message.content
        except Exception as exc:
            logger.warning("OpenAI generation failed: %s", exc)
            return None

    def _gemini_complete(self, prompt: str) -> str | None:
        try:
            import google.generativeai as genai

            genai.configure(api_key=self.settings.google_api_key)
            model = genai.GenerativeModel(self.settings.gemini_model)
            response = model.generate_content(f"{SYSTEM_GUARDRAIL}\n\n{prompt}")
            return response.text
        except Exception as exc:
            logger.warning("Gemini generation failed: %s", exc)
            return None

