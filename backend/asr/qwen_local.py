from __future__ import annotations

import os
from pathlib import Path

from backend.asr.base import ASRAdapter


class QwenLocalASR(ASRAdapter):
    name = "qwen_local"

    def __init__(self, model_name: str, device: str = "auto", dtype: str = "auto") -> None:
        self.model_name = model_name
        self.device = device
        self.dtype = dtype
        self._model = None

    def _load(self):
        if self._model is not None:
            return self._model
        try:
            from mlx_qwen3_asr import Session
        except ImportError as exc:
            raise RuntimeError(
                "Qwen MLX ASR is not installed. Run: pip install -r requirements-qwen.txt"
            ) from exc

        model_name = os.path.expandvars(os.path.expanduser(self.model_name))
        model_path = Path(model_name)
        if model_path.is_absolute() and not model_path.exists():
            raise RuntimeError(f"Qwen model folder does not exist: {model_path}")

        kwargs = {"model": model_name}
        if self.dtype not in {"", "auto"}:
            kwargs["dtype"] = self.dtype
        self._model = Session(**kwargs)
        return self._model

    def transcribe(self, audio_path: Path) -> str:
        model = self._load()
        result = model.transcribe(str(audio_path), language=None)
        return result.text.strip()
