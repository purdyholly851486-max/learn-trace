from __future__ import annotations

import shutil
from pathlib import Path
from typing import Literal

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from backend.analysis.cognitive import analyze_cognitive
from backend.analysis.concept import analyze_concepts
from backend.analysis.llm import OpenAICompatibleLLM
from backend.analysis.materials import combine_materials
from backend.asr.factory import build_asr
from backend.config import (
    CONFIG,
    ROOT,
    clear_user_setting,
    load_user_settings,
    normalize_data_dir,
    resolve_data_dir,
    save_user_settings,
)
from backend.report.markdown import build_markdown
from backend.storage import (
    create_session,
    read_json,
    read_session,
    safe_filename,
    session_path,
    update_session,
    write_json,
)
from backend.transcript.cleaner import clean_transcript

app = FastAPI(title="Learn Trace", version="0.1.0")
FRONTEND = ROOT / "frontend"
app.mount("/static", StaticFiles(directory=FRONTEND), name="static")


class CreateSessionRequest(BaseModel):
    title: str = "Learning Session"


class ManualTranscriptRequest(BaseModel):
    transcript: str


class SettingsRequest(BaseModel):
    data_dir: str | None = None


class FinishRequest(BaseModel):
    asr_provider: Literal["manual", "qwen_local", "qwen_server"] | None = None


@app.get("/", response_class=HTMLResponse)
def home() -> HTMLResponse:
    return HTMLResponse((FRONTEND / "index.html").read_text(encoding="utf-8"))


@app.get("/api/health")
def health() -> dict:
    llm = OpenAICompatibleLLM()
    return {
        "ok": True,
        "version": "0.1.0",
        "default_asr": CONFIG.get("asr", {}).get("provider", "manual"),
        "llm_configured": llm.available,
    }


@app.get("/api/settings")
def api_get_settings() -> dict:
    return {
        "data_dir": str(resolve_data_dir()),
        "is_custom": bool(load_user_settings().get("data_dir")),
    }


@app.put("/api/settings")
def api_update_settings(payload: SettingsRequest) -> dict:
    if payload.data_dir is None:
        clear_user_setting("data_dir")
    else:
        raw = payload.data_dir.strip()
        if not raw:
            raise HTTPException(status_code=400, detail="Data directory is empty")
        path = normalize_data_dir(raw)
        if path == Path(path.anchor):
            raise HTTPException(status_code=400, detail="Refusing to use a filesystem root as data directory")
        if not Path(raw).is_absolute() and ROOT not in path.resolve().parents:
            raise HTTPException(
                status_code=400,
                detail="Relative paths must stay inside the project; use an absolute path for other locations",
            )
        try:
            path.mkdir(parents=True, exist_ok=True)
        except OSError as exc:
            raise HTTPException(status_code=400, detail=f"Cannot create data directory: {exc}")
        save_user_settings({"data_dir": str(path)})
    return {
        "data_dir": str(resolve_data_dir()),
        "is_custom": bool(load_user_settings().get("data_dir")),
    }


@app.post("/api/sessions")
def api_create_session(payload: CreateSessionRequest) -> dict:
    return create_session(payload.title)


@app.get("/api/sessions/{session_id}")
def api_get_session(session_id: str) -> dict:
    try:
        meta = read_session(session_id)
        path = session_path(session_id)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Session not found")

    response = {"session": meta}
    for name in ["cognitive.json", "concepts.json"]:
        file_path = path / name
        if file_path.exists():
            response[name.removesuffix(".json")] = read_json(file_path)
    report_path = path / "report.md"
    if report_path.exists():
        response["report_markdown"] = report_path.read_text(encoding="utf-8")
    return response


@app.post("/api/sessions/{session_id}/materials")
async def api_upload_materials(session_id: str, files: list[UploadFile] = File(...)) -> dict:
    try:
        path = session_path(session_id)
        meta = read_session(session_id)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Session not found")

    accepted = {".pdf", ".md", ".markdown", ".txt"}
    saved = []
    for upload in files:
        name = safe_filename(upload.filename or "material")
        suffix = Path(name).suffix.lower()
        if suffix not in accepted:
            raise HTTPException(status_code=400, detail=f"Unsupported material type: {suffix}")
        dest = path / "materials" / name
        with dest.open("wb") as handle:
            shutil.copyfileobj(upload.file, handle)
        saved.append(name)

    meta["materials"] = sorted(set(meta.get("materials", []) + saved))
    update_session(session_id, materials=meta["materials"], status="materials_uploaded")
    return {"saved": saved, "materials": meta["materials"]}


@app.post("/api/sessions/{session_id}/audio")
async def api_upload_audio(
    session_id: str,
    audio: UploadFile = File(...),
    duration_seconds: float | None = Form(default=None),
) -> dict:
    try:
        path = session_path(session_id)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Session not found")

    dest = path / "audio.wav"
    with dest.open("wb") as handle:
        shutil.copyfileobj(audio.file, handle)
    update_session(session_id, audio_file="audio.wav", duration_seconds=duration_seconds, status="audio_saved")
    return {"saved": "audio.wav", "duration_seconds": duration_seconds}


@app.post("/api/sessions/{session_id}/transcript/manual")
def api_manual_transcript(session_id: str, payload: ManualTranscriptRequest) -> dict:
    try:
        path = session_path(session_id)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Session not found")
    raw = payload.transcript.strip()
    if not raw:
        raise HTTPException(status_code=400, detail="Transcript is empty")
    (path / "raw_transcript.txt").write_text(raw, encoding="utf-8")
    update_session(session_id, transcript_source="manual", status="transcript_saved")
    return {"characters": len(raw)}


@app.post("/api/sessions/{session_id}/finish")
def api_finish_session(session_id: str, payload: FinishRequest) -> dict:
    try:
        path = session_path(session_id)
        meta = read_session(session_id)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Session not found")

    raw_path = path / "raw_transcript.txt"
    audio_path = path / "audio.wav"
    provider = payload.asr_provider or CONFIG.get("asr", {}).get("provider", "manual")

    if raw_path.exists():
        raw = raw_path.read_text(encoding="utf-8")
        transcript_source = meta.get("transcript_source", "manual")
    elif audio_path.exists():
        try:
            asr = build_asr(CONFIG.get("asr", {}), provider=provider)
            raw = asr.transcribe(audio_path)
        except Exception as exc:
            raise HTTPException(status_code=500, detail=f"ASR failed: {exc}")
        raw_path.write_text(raw, encoding="utf-8")
        transcript_source = provider
    else:
        raise HTTPException(status_code=400, detail="No transcript or audio available")

    clean = clean_transcript(raw)
    clean_doc = f"# {meta.get('title', 'Learning Session')} - Clean Transcript\n\n{clean}\n"
    (path / "clean_transcript.md").write_text(clean_doc, encoding="utf-8")

    material_paths = [path / "materials" / name for name in meta.get("materials", [])]
    max_material = int(CONFIG.get("analysis", {}).get("max_material_chars", 18000))
    max_transcript = int(CONFIG.get("analysis", {}).get("max_transcript_chars", 18000))
    material_text = combine_materials(material_paths, max_chars=max_material)
    transcript_for_analysis = clean[:max_transcript]

    llm = OpenAICompatibleLLM()
    cognitive = analyze_cognitive(transcript_for_analysis, llm=llm)
    concepts = analyze_concepts(transcript_for_analysis, material_text, llm=llm)

    write_json(path / "cognitive.json", cognitive)
    write_json(path / "concepts.json", concepts)
    report = build_markdown(meta, clean, cognitive, concepts)
    (path / "report.md").write_text(report, encoding="utf-8")

    meta = update_session(
        session_id,
        status="finished",
        transcript_source=transcript_source,
        analysis_mode={"cognitive": cognitive.get("mode"), "concept": concepts.get("mode")},
    )
    return {
        "session": meta,
        "cognitive": cognitive,
        "concepts": concepts,
        "report_markdown": report,
    }


@app.get("/api/sessions/{session_id}/report.md")
def api_report_markdown(session_id: str):
    try:
        path = session_path(session_id) / "report.md"
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Session not found")
    if not path.exists():
        raise HTTPException(status_code=404, detail="Report not generated")
    return FileResponse(path, media_type="text/markdown", filename=f"{session_id}-learn-trace.md")


@app.exception_handler(Exception)
async def unhandled_exception_handler(_request, exc: Exception):
    return JSONResponse(status_code=500, content={"detail": str(exc)})
