from __future__ import annotations

import re
from collections import Counter
from typing import Any

from backend.analysis.llm import OpenAICompatibleLLM
from backend.transcript.cleaner import segment_utterances

SYSTEM_PROMPT = """You analyze learning process traces, not personality or mental health.
Use only evidence in the transcript. Distinguish observation from hypothesis.
Focus on metacognition and learning process: self-monitoring, error correction,
concept boundaries, representation tracking, causal explanation, and explanation structure.
Never diagnose stable traits from one session. Return JSON only."""

USER_TEMPLATE = """Analyze this think-aloud learning transcript.

Return exactly this JSON shape:
{{
  "summary": "one sentence",
  "primary_bottleneck": {{
    "label": "short label",
    "observation": "what was directly observed",
    "hypothesis": "session-level learning hypothesis",
    "confidence": 0.0,
    "evidence": ["short verbatim or near-verbatim excerpts"],
    "intervention": ["specific next-step learning behaviors"]
  }},
  "dimensions": [
    {{
      "name": "Self-monitoring|Error correction|Concept boundary|Representation tracking|Causal explanation|Explanation structure",
      "status": "strength|mixed|weak|insufficient_evidence",
      "observation": "evidence-grounded note"
    }}
  ],
  "recurring_patterns": [
    {{"pattern": "...", "count_or_frequency": "...", "evidence": ["..."]}}
  ],
  "limitations": ["..."]
}}

Transcript:
---
{transcript}
---
"""


def analyze_cognitive(transcript: str, llm: OpenAICompatibleLLM | None = None) -> dict[str, Any]:
    llm = llm or OpenAICompatibleLLM()
    if llm.available:
        try:
            result = llm.complete_json(SYSTEM_PROMPT, USER_TEMPLATE.format(transcript=transcript))
            result["mode"] = "llm"
            return result
        except Exception as exc:
            fallback = _heuristic(transcript)
            fallback["warning"] = f"LLM analysis failed; heuristic fallback used: {exc}"
            return fallback
    return _heuristic(transcript)


def _heuristic(transcript: str) -> dict[str, Any]:
    utterances = segment_utterances(transcript)
    correction_rx = re.compile(r"(不对|等等|等一下|应该不是|我错了|wait|actually|no[, ]|not right)", re.I)
    uncertainty_rx = re.compile(r"(为什么|怎么|区别|是不是|还是|不知道|不太懂|忘了|why|how|difference|confus)", re.I)
    causal_rx = re.compile(r"(因为|所以|因此|也就是说|because|therefore|so that|which means)", re.I)
    boundary_rx = re.compile(r"(区别|是不是.*还是|到底.*区别|vs\.?|versus|difference|\b(?:is|are|was|were).{0,100}\bor\b)", re.I)
    representation_terms = re.compile(r"\b(token|id|byte|bit|string|vector|matrix|tensor|embedding|shape|axis|index|encoding)\b", re.I)

    corrections = [u for u in utterances if correction_rx.search(u)]
    uncertainties = [u for u in utterances if uncertainty_rx.search(u)]
    causal = [u for u in utterances if causal_rx.search(u)]
    boundaries = [u for u in utterances if boundary_rx.search(u)]
    rep_utterances = [u for u in utterances if len(representation_terms.findall(u)) >= 2]
    rep_confusions = [u for u in rep_utterances if uncertainty_rx.search(u) or correction_rx.search(u) or boundary_rx.search(u)]

    candidates = [
        ("Representation tracking", len(rep_confusions) * 2 + len(boundaries)),
        ("Self-monitoring", len(corrections)),
        ("Question-driven clarification", len(uncertainties)),
        ("Causal explanation", len(causal)),
    ]
    primary = max(candidates, key=lambda x: x[1])[0] if utterances else "Insufficient evidence"

    if primary == "Representation tracking":
        observation = "Multiple utterances place two or more representation-level terms in direct comparison or uncertainty."
        hypothesis = "During this session, transitions between adjacent representations may be less stable than isolated definitions."
        intervention = [
            "For each new object, write: name, example, type, shape, source, and next step.",
            "Draw the full data pipeline before memorizing individual definitions.",
            "After each transformation, say aloud what changed and what stayed the same.",
        ]
        evidence_pool = boundaries + rep_confusions + rep_utterances
    elif primary == "Self-monitoring":
        observation = "The learner repeatedly detects and corrects their own statements."
        hypothesis = "Self-monitoring is active, but some concepts may require a more stable external representation to reduce rework."
        intervention = ["Keep self-corrections, then record the corrected rule in one sentence."]
        evidence_pool = corrections
    elif primary == "Question-driven clarification":
        observation = "The transcript contains many uncertainty and clarification questions."
        hypothesis = "The learner is actively testing boundaries but may benefit from grouping questions by concept before continuing."
        intervention = ["Pause every 5-10 minutes and consolidate open questions into a short queue."]
        evidence_pool = uncertainties
    else:
        observation = "The learner frequently uses causal connectors while explaining concepts."
        hypothesis = "Causal explanation appears to be a relative strength in this session."
        intervention = ["Continue explaining causes, then test the explanation with one counterexample."]
        evidence_pool = causal

    evidence = []
    for item in evidence_pool:
        if item not in evidence:
            evidence.append(item[:220])
        if len(evidence) == 4:
            break

    dims = [
        {
            "name": "Self-monitoring",
            "status": "strength" if len(corrections) >= 2 else "mixed" if corrections else "insufficient_evidence",
            "observation": f"Detected {len(corrections)} explicit self-correction utterance(s).",
        },
        {
            "name": "Concept boundary",
            "status": "weak" if len(boundaries) >= 3 else "mixed" if boundaries else "insufficient_evidence",
            "observation": f"Detected {len(boundaries)} boundary-comparison or distinction utterance(s).",
        },
        {
            "name": "Representation tracking",
            "status": "weak" if len(rep_utterances) >= 4 else "mixed" if rep_utterances else "insufficient_evidence",
            "observation": f"Detected {len(rep_utterances)} utterance(s) involving multiple representation-level terms.",
        },
        {
            "name": "Causal explanation",
            "status": "strength" if len(causal) >= 4 else "mixed" if causal else "insufficient_evidence",
            "observation": f"Detected {len(causal)} causal/explanatory utterance(s).",
        },
        {
            "name": "Error correction",
            "status": "mixed" if corrections else "insufficient_evidence",
            "observation": "Heuristic mode detects correction attempts but cannot reliably judge whether the correction is conceptually correct.",
        },
        {
            "name": "Explanation structure",
            "status": "insufficient_evidence",
            "observation": "Requires stronger discourse analysis than the heuristic baseline provides.",
        },
    ]

    counts = Counter({
        "self_corrections": len(corrections),
        "uncertainty_questions": len(uncertainties),
        "concept_boundary_checks": len(boundaries),
        "representation_comparisons": len(rep_utterances),
        "causal_explanations": len(causal),
    })

    return {
        "mode": "heuristic",
        "summary": "Baseline process analysis generated from observable language markers; use an LLM endpoint for semantic diagnosis.",
        "primary_bottleneck": {
            "label": primary,
            "observation": observation,
            "hypothesis": hypothesis,
            "confidence": 0.45 if utterances else 0.1,
            "evidence": evidence,
            "intervention": intervention,
        },
        "dimensions": dims,
        "recurring_patterns": [
            {"pattern": key, "count_or_frequency": str(value), "evidence": []}
            for key, value in counts.most_common()
            if value
        ],
        "limitations": [
            "Heuristic mode cannot infer deep misconceptions or stable learning traits.",
            "A single session should only support session-level hypotheses.",
        ],
    }
