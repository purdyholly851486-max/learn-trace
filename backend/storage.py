from __future__ import annotations

import json
import re
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from backend.config import ensure_data_dir, resolve_data_dir


def _slug(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9_-]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return value[:48] or "session"


def create_session(title: str) -> dict[str, Any]:
    now = datetime.now(timezone.utc)
    session_id = f"{now.strftime('%Y%m%d-%H%M%S')}-{_slug(title)}-{uuid.uuid4().hex[:6]}"
    path = ensure_data_dir() / session_id
    (path / "materials").mkdir(parents=True, exist_ok=True)
    meta = {
        "id": session_id,
        "title": title.strip() or "Untitled learning session",
        "created_at": now.isoformat(),
        "status": "created",
        "materials": [],
    }
    write_json(path / "session.json", meta)
    return meta


_SESSION_ID_RX = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]{0,127}$")


def session_path(session_id: str) -> Path:
    if not _SESSION_ID_RX.match(session_id):
        raise FileNotFoundError(session_id)
    path = resolve_data_dir() / session_id
    if not path.exists() or not path.is_dir():
        raise FileNotFoundError(session_id)
    return path


def read_session(session_id: str) -> dict[str, Any]:
    return read_json(session_path(session_id) / "session.json")


def update_session(session_id: str, **updates: Any) -> dict[str, Any]:
    path = session_path(session_id)
    meta = read_json(path / "session.json")
    meta.update(updates)
    write_json(path / "session.json", meta)
    return meta


def safe_filename(name: str) -> str:
    base = Path(name).name
    base = re.sub(r"[^A-Za-z0-9._-]+", "_", base)
    return base[:120] or "file"


def write_json(path: Path, data: Any) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))
