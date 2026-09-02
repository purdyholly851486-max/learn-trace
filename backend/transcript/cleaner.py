from __future__ import annotations

import re

_FILLERS = [
    r"\b(?:um+|uh+|erm+)\b",
    r"(?:^|[\s,，。！？])(?:嗯+|呃+|额+|啊+)(?=[\s,，。！？]|$)",
]


def clean_transcript(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)

    cleaned = text
    for pattern in _FILLERS:
        cleaned = re.sub(pattern, " ", cleaned, flags=re.IGNORECASE)

    cleaned = re.sub(r"[ ]{2,}", " ", cleaned)
    cleaned = re.sub(r" *\n *", "\n", cleaned)
    cleaned = re.sub(r"\s+([,.;:!?])", r"\1", cleaned)
    return cleaned.strip()


def segment_utterances(text: str) -> list[str]:
    pieces = re.split(r"(?<=[。！？!?\.])\s+|\n+", text)
    return [p.strip() for p in pieces if len(p.strip()) >= 3]
