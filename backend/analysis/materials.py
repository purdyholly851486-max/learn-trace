from __future__ import annotations

import re
from pathlib import Path

from pypdf import PdfReader


def extract_text(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in {".txt", ".md", ".markdown"}:
        return path.read_text(encoding="utf-8", errors="ignore")
    if suffix == ".pdf":
        reader = PdfReader(str(path))
        pages = []
        for index, page in enumerate(reader.pages, start=1):
            text = page.extract_text() or ""
            pages.append(f"\n[Page {index}]\n{text}")
        return "\n".join(pages)
    raise ValueError(f"Unsupported material type: {suffix}")


def combine_materials(paths: list[Path], max_chars: int = 18000) -> str:
    parts: list[str] = []
    remaining = max_chars
    for path in paths:
        if remaining <= 0:
            break
        try:
            text = extract_text(path)
        except Exception as exc:
            text = f"[Could not parse {path.name}: {exc}]"
        block = f"\n\n=== {path.name} ===\n{text}"
        block = block[:remaining]
        parts.append(block)
        remaining -= len(block)
    return "".join(parts).strip()


def fallback_reference_concepts(material_text: str, limit: int = 24) -> list[str]:
    headings = re.findall(r"(?m)^#{1,6}\s+(.+)$", material_text)
    backticks = re.findall(r"`([^`\n]{2,60})`", material_text)
    english_terms = re.findall(r"\b[A-Za-z][A-Za-z0-9_-]{2,30}\b", material_text)

    stop = {
        "the", "and", "for", "with", "this", "that", "from", "into", "your", "you", "are", "was",
        "were", "have", "has", "not", "can", "will", "then", "than", "when", "where", "what", "why",
        "how", "using", "used", "use", "each", "also", "about", "more", "some", "such", "one", "two",
    }
    freq: dict[str, int] = {}
    for term in english_terms:
        key = term.strip()
        if key.lower() in stop:
            continue
        freq[key] = freq.get(key, 0) + 1

    ranked = [k for k, v in sorted(freq.items(), key=lambda x: (-x[1], x[0].lower())) if v >= 2]
    out: list[str] = []
    for item in headings + backticks + ranked:
        item = re.sub(r"\s+", " ", item).strip(" :-")
        if len(item) < 2:
            continue
        existing = {x.lower() for x in out}
        low = item.lower()
        covered_by_phrase = any(low != x and len(low.split()) == 1 and low in x.split() for x in existing)
        if low not in existing and not covered_by_phrase:
            out.append(item)
        if len(out) >= limit:
            break
    return out
