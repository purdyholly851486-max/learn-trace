from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
SETTINGS_PATH = ROOT / "settings.local.json"


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


def load_user_settings() -> dict[str, Any]:
    if not SETTINGS_PATH.exists():
        return {}
    try:
        return json.loads(SETTINGS_PATH.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}


def save_user_settings(updates: dict[str, Any]) -> dict[str, Any]:
    settings = load_user_settings()
    settings.update(updates)
    SETTINGS_PATH.write_text(
        json.dumps(settings, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return settings


def clear_user_setting(key: str) -> dict[str, Any]:
    settings = load_user_settings()
    settings.pop(key, None)
    SETTINGS_PATH.write_text(
        json.dumps(settings, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return settings


def normalize_data_dir(raw: str) -> Path:
    expanded = os.path.expandvars(os.path.expanduser(str(raw).strip()))
    path = Path(expanded)
    if not path.is_absolute():
        path = ROOT / path
    return path


def resolve_data_dir() -> Path:
    custom = load_user_settings().get("data_dir")
    if custom:
        return normalize_data_dir(custom)
    return normalize_data_dir(CONFIG["app"].get("data_dir", "data/sessions"))


def ensure_data_dir() -> Path:
    path = resolve_data_dir()
    path.mkdir(parents=True, exist_ok=True)
    return path
