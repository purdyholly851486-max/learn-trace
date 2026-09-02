from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]


def load_config() -> dict[str, Any]:
    path = ROOT / "config.yaml"
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}

    data.setdefault("app", {})
    data.setdefault("asr", {})
    data.setdefault("analysis", {})

    if os.getenv("LEARN_TRACE_ASR_PROVIDER"):
        data["asr"]["provider"] = os.environ["LEARN_TRACE_ASR_PROVIDER"]
    if os.getenv("LEARN_TRACE_QWEN_MODEL"):
        data["asr"].setdefault("qwen_local", {})["model"] = os.environ["LEARN_TRACE_QWEN_MODEL"]

    return data


CONFIG = load_config()
DATA_DIR = ROOT / CONFIG["app"].get("data_dir", "data/sessions")
DATA_DIR.mkdir(parents=True, exist_ok=True)
