from __future__ import annotations

import re
from typing import Any

from backend.analysis.llm import OpenAICompatibleLLM
from backend.analysis.materials import fallback_reference_concepts

SYSTEM_PROMPT = """You are a strict concept-grounding evaluator for learning sessions.
Use the uploaded reference material as the source of truth. Evaluate only concepts that are supported by the material.
Separate what the learner explicitly said from your correction. Do not invent quotes.
Use statuses: correct, partial, incorrect, unclear, not_observed.
Return JSON only."""

USER_TEMPLATE = """Reference material:
---
{material}
---

Student transcript:
---
{transcript}
---

Return exactly this JSON shape:
{{
  "overview": "one sentence",
  "concepts": [
    {{
      "concept": "name",
      "status": "correct|partial|incorrect|unclear|not_observed",
      "student_understanding": "short paraphrase based on transcript",
      "evidence": ["short transcript excerpts"],
      "reference_understanding": "precise definition grounded in material",
      "correction": "what to change or add",
      "importance": "high|medium|low"
    }}
  ],
  "priority_review": ["concept names"],
  "limitations": ["..."]
}}

Prioritize concepts the learner actually discusses. Include at most 16 concepts.
"""


def analyze_concepts(
    transcript: str,
    material_text: str,
    llm: OpenAICompatibleLLM | None = None,
) -> dict[str, Any]:
    if not material_text.strip():
        return {
            "mode": "no_material",
            "overview": "No reference material was uploaded, so concept correctness was not evaluated.",
            "concepts": [],
            "priority_review": [],
            "limitations": ["Upload PDF, Markdown, or text material to enable concept grounding."],
        }

    llm = llm or OpenAICompatibleLLM()
    if llm.available:
        try:
            result = llm.complete_json(
                SYSTEM_PROMPT,
                USER_TEMPLATE.format(material=material_text, transcript=transcript),
            )
            result["mode"] = "llm_grounded"
            return result
        except Exception as exc:
            fallback = _heuristic(transcript, material_text)
            fallback["warning"] = f"LLM concept analysis failed; heuristic fallback used: {exc}"
            return fallback
    return _heuristic(transcript, material_text)


def _heuristic(transcript: str, material_text: str) -> dict[str, Any]:
    concepts = fallback_reference_concepts(material_text, limit=20)
    transcript_lower = transcript.lower()
    results = []
    observed = []

    for concept in concepts:
        needle = concept.lower().strip()
        if len(needle) < 3:
            continue
        found = needle in transcript_lower
        if not found and " " in needle:
            words = [w for w in re.findall(r"[a-z0-9_-]+", needle) if len(w) >= 3]
            found = bool(words) and sum(w in transcript_lower for w in words) >= max(1, len(words) - 1)
        if found:
            observed.append(concept)
            results.append(
                {
                    "concept": concept,
                    "status": "unclear",
                    "student_understanding": "Concept was mentioned, but heuristic mode cannot reliably judge correctness.",
                    "evidence": [],
                    "reference_understanding": "See uploaded material.",
                    "correction": "Configure an OpenAI-compatible LLM endpoint for grounded semantic evaluation.",
                    "importance": "medium",
                }
            )

    return {
        "mode": "heuristic",
        "overview": f"Detected {len(observed)} material-derived concept mention(s); correctness requires semantic analysis.",
        "concepts": results,
        "priority_review": observed[:5],
        "limitations": [
            "Heuristic mode checks mention overlap only and does not claim conceptual correctness.",
            "Set LEARN_TRACE_LLM_BASE_URL and LEARN_TRACE_LLM_MODEL for grounded concept diagnosis.",
        ],
    }
