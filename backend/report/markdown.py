from __future__ import annotations

from typing import Any


def _frontmatter_value(value: str) -> str:
    return str(value).replace('"', "'")


def _build_frontmatter(session: dict[str, Any], cognitive: dict[str, Any], concepts: dict[str, Any]) -> list[str]:
    return [
        "---",
        f"title: \"{_frontmatter_value(session.get('title', 'Learning Session'))}\"",
        f"session_id: \"{_frontmatter_value(session.get('id', ''))}\"",
        f"created: \"{_frontmatter_value(session.get('created_at', ''))}\"",
        f"cognitive_mode: \"{_frontmatter_value(cognitive.get('mode', 'unknown'))}\"",
        f"concept_mode: \"{_frontmatter_value(concepts.get('mode', 'unknown'))}\"",
        "tags:",
        "  - learn-trace",
        "  - learning-diagnosis",
        "---",
        "",
    ]


def _status_mark(status: str) -> str:
    return {
        "correct": "OK",
        "partial": "PARTIAL",
        "incorrect": "WRONG",
        "unclear": "UNCLEAR",
        "not_observed": "N/A",
        "strength": "STRONG",
        "mixed": "MIXED",
        "weak": "WEAK",
        "insufficient_evidence": "N/A",
    }.get(status, status.upper())


def build_markdown(
    session: dict[str, Any],
    transcript: str,
    cognitive: dict[str, Any],
    concepts: dict[str, Any],
) -> str:
    primary = cognitive.get("primary_bottleneck", {})
    lines = _build_frontmatter(session, cognitive, concepts)
    lines.extend([
        f"# Learn Trace - {session.get('title', 'Learning Session')}",
        "",
        f"- Session: `{session.get('id', '')}`",
        f"- Created: {session.get('created_at', '')}",
        f"- Cognitive mode: `{cognitive.get('mode', 'unknown')}`",
        f"- Concept mode: `{concepts.get('mode', 'unknown')}`",
        "",
        "## 1. Cognitive Diagnosis",
        "",
        f"### Primary pattern: {primary.get('label', 'Insufficient evidence')}",
        "",
        f"**Observation:** {primary.get('observation', '')}",
        "",
        f"**Session-level hypothesis:** {primary.get('hypothesis', '')}",
        "",
        f"**Confidence:** {primary.get('confidence', '')}",
        "",
        "### Evidence",
        "",
    ])

    evidence = primary.get("evidence", []) or []
    if evidence:
        for item in evidence:
            lines.append(f"> {item}")
            lines.append("")
    else:
        lines.append("No strong evidence extracted.")
        lines.append("")

    lines.extend(["### Recommended intervention", ""])
    for item in primary.get("intervention", []) or []:
        lines.append(f"- {item}")
    lines.extend(["", "### Cognitive dimensions", "", "| Dimension | Status | Observation |", "|---|---|---|"])
    for dim in cognitive.get("dimensions", []) or []:
        lines.append(
            f"| {dim.get('name', '')} | {_status_mark(dim.get('status', ''))} | {str(dim.get('observation', '')).replace('|', '/')} |"
        )

    lines.extend(["", "## 2. Concept Diagnosis", "", concepts.get("overview", ""), ""])
    concept_rows = concepts.get("concepts", []) or []
    if concept_rows:
        lines.extend(["| Concept | Status | Student understanding | Correction |", "|---|---|---|---|"])
        for item in concept_rows:
            lines.append(
                "| {concept} | {status} | {student} | {correction} |".format(
                    concept=str(item.get("concept", "")).replace("|", "/"),
                    status=_status_mark(item.get("status", "")),
                    student=str(item.get("student_understanding", "")).replace("|", "/"),
                    correction=str(item.get("correction", "")).replace("|", "/"),
                )
            )
    else:
        lines.append("No grounded concept evaluation available.")

    priority = concepts.get("priority_review", []) or []
    if priority:
        lines.extend(["", "### Priority review", ""])
        for item in priority:
            lines.append(f"- {item}")

    lines.extend(["", "## 3. Clean Transcript", "", transcript.strip(), ""])

    limitations = (cognitive.get("limitations", []) or []) + (concepts.get("limitations", []) or [])
    if limitations:
        lines.extend(["", "## Limitations", ""])
        for item in limitations:
            lines.append(f"- {item}")

    return "\n".join(lines).strip() + "\n"
