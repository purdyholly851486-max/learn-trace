from __future__ import annotations

from pathlib import Path

from backend.asr.base import ASRAdapter


class ManualASR(ASRAdapter):
    name = "manual"

    def transcribe(self, audio_path: Path) -> str:
        raise RuntimeError(
            "Manual ASR mode is active. Paste a transcript in the UI, or configure qwen_local/qwen_server."
        )
