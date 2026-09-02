from __future__ import annotations

import json
import os
import re
from typing import Any

import httpx


class OpenAICompatibleLLM:
    def __init__(self) -> None:
        self.base_url = os.getenv("LEARN_TRACE_LLM_BASE_URL", "").rstrip("/")
        self.model = os.getenv("LEARN_TRACE_LLM_MODEL", "")
        self.api_key = os.getenv("LEARN_TRACE_LLM_API_KEY", "EMPTY")

    @property
    def available(self) -> bool:
        return bool(self.base_url and self.model)

    def complete_json(self, system: str, user: str, timeout: float = 180.0) -> dict[str, Any]:
        if not self.available:
            raise RuntimeError("No LLM endpoint configured")
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        body = {
            "model": self.model,
            "temperature": 0.1,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        }
        with httpx.Client(timeout=timeout) as client:
            response = client.post(f"{self.base_url}/chat/completions", headers=headers, json=body)
            response.raise_for_status()
            text = response.json()["choices"][0]["message"]["content"]
        return _extract_json(text)


def _extract_json(text: str) -> dict[str, Any]:
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)
        text = re.sub(r"\s*```$", "", text)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        start = text.find("{")
        end = text.rfind("}")
        if start >= 0 and end > start:
            return json.loads(text[start : end + 1])
        raise
