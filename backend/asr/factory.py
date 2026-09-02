from __future__ import annotations

from backend.asr.base import ASRAdapter
from backend.asr.manual import ManualASR
from backend.asr.qwen_local import QwenLocalASR
from backend.asr.qwen_server import QwenServerASR


def build_asr(config: dict, provider: str | None = None) -> ASRAdapter:
    provider = provider or config.get("provider", "manual")
    if provider == "manual":
        return ManualASR()
    if provider == "qwen_local":
        cfg = config.get("qwen_local", {})
        return QwenLocalASR(
            model_name=cfg.get("model", "Qwen/Qwen3-ASR-0.6B"),
            device=cfg.get("device", "auto"),
            dtype=cfg.get("dtype", "auto"),
        )
    if provider == "qwen_server":
        cfg = config.get("qwen_server", {})
        return QwenServerASR(
            base_url=cfg.get("base_url", "http://127.0.0.1:8000/v1"),
            api_key=cfg.get("api_key", "EMPTY"),
        )
    raise ValueError(f"Unknown ASR provider: {provider}")
