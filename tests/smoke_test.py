from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient

from backend.main import app


def main() -> None:
    client = TestClient(app)
    health = client.get("/api/health")
    assert health.status_code == 200

    session = client.post("/api/sessions", json={"title": "Smoke Test"})
    assert session.status_code == 200
    session_id = session.json()["id"]

    notes = Path("samples/lecture_notes.md")
    with notes.open("rb") as handle:
        upload = client.post(
            f"/api/sessions/{session_id}/materials",
            files={"files": (notes.name, handle, "text/markdown")},
        )
    assert upload.status_code == 200, upload.text

    transcript = Path("samples/sample_transcript.txt").read_text(encoding="utf-8")
    saved = client.post(
        f"/api/sessions/{session_id}/transcript/manual",
        json={"transcript": transcript},
    )
    assert saved.status_code == 200, saved.text

    finished = client.post(
        f"/api/sessions/{session_id}/finish",
        json={"asr_provider": "manual"},
    )
    assert finished.status_code == 200, finished.text
    payload = finished.json()
    assert payload["cognitive"]["primary_bottleneck"]["label"]
    assert "report_markdown" in payload

    print("Smoke test passed")
    print("Session:", session_id)
    print("Primary pattern:", payload["cognitive"]["primary_bottleneck"]["label"])


if __name__ == "__main__":
    main()
