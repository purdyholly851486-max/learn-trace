from __future__ import annotations

import base64
import mimetypes
from pathlib import Path

import httpx

from backend.asr.base import ASRAdapter


class QwenServerASR(ASRAdapter):
    name = "qwen_server"

    def __init__(self, base_url: str, api_key: str = "EMPTY", timeout: float = 300.0) -> None:
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout

    def transcribe(self, audio_path: Path) -> str:
        mime = mimetypes.guess_type(audio_path.name)[0] or "audio/wav"
        payload = base64.b64encode(audio_path.read_bytes()).decode("ascii")
        data_url = f"data:{mime};base64,{payload}"
        body = {
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "audio_url", "audio_url": {"url": data_url}}
                    ],
                }
            ]
        }
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {self.api_key}"}
        with httpx.Client(timeout=self.timeout) as client:
            response = client.post(f"{self.base_url}/chat/completions", json=body, headers=headers)
            response.raise_for_status()
            content = response.json()["choices"][0]["message"]["content"]

        try:
            from qwen_asr import parse_asr_output

            _language, text = parse_asr_output(content)
            return text.strip()
        except Exception:
            return str(content).strip()
