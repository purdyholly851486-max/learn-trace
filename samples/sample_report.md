# Learn Trace - Smoke Test

- Session: `20260902-143519-smoke-test-3aa9dc`
- Created: 2026-09-02T14:35:19.843882+00:00
- Cognitive mode: `heuristic`
- Concept mode: `heuristic`

## 1. Cognitive Diagnosis

### Primary pattern: Representation tracking

**Observation:** Multiple utterances place two or more representation-level terms in direct comparison or uncertainty.

**Session-level hypothesis:** During this session, transitions between adjacent representations may be less stable than isolated definitions.

**Confidence:** 0.45

### Evidence

> If I see 231, is that a token ID or a byte value?

> I understand one token can map to four embedding numbers, but if there are three tokens with four numbers each, why is that two dimensional?

> Because one byte has 8 bits and each bit has two states, so 2 to the 8 is 256.

> I am still mixing up byte values and token IDs.

### Recommended intervention

- For each new object, write: name, example, type, shape, source, and next step.
- Draw the full data pipeline before memorizing individual definitions.
- After each transformation, say aloud what changed and what stayed the same.

### Cognitive dimensions

| Dimension | Status | Observation |
|---|---|---|
| Self-monitoring | STRONG | Detected 2 explicit self-correction utterance(s). |
| Concept boundary | MIXED | Detected 1 boundary-comparison or distinction utterance(s). |
| Representation tracking | WEAK | Detected 7 utterance(s) involving multiple representation-level terms. |
| Causal explanation | MIXED | Detected 1 causal/explanatory utterance(s). |
| Error correction | MIXED | Heuristic mode detects correction attempts but cannot reliably judge whether the correction is conceptually correct. |
| Explanation structure | N/A | Requires stronger discourse analysis than the heuristic baseline provides. |

## 2. Concept Diagnosis

Detected 13 material-derived concept mention(s); correctness requires semantic analysis.

| Concept | Status | Student understanding | Correction |
|---|---|---|---|
| UTF-8 and bytes | UNCLEAR | Concept was mentioned, but heuristic mode cannot reliably judge correctness. | Configure an OpenAI-compatible LLM endpoint for grounded semantic evaluation. |
| Byte-level BPE | UNCLEAR | Concept was mentioned, but heuristic mode cannot reliably judge correctness. | Configure an OpenAI-compatible LLM endpoint for grounded semantic evaluation. |
| Token IDs | UNCLEAR | Concept was mentioned, but heuristic mode cannot reliably judge correctness. | Configure an OpenAI-compatible LLM endpoint for grounded semantic evaluation. |
| Embedding lookup | UNCLEAR | Concept was mentioned, but heuristic mode cannot reliably judge correctness. | Configure an OpenAI-compatible LLM endpoint for grounded semantic evaluation. |
| byte | UNCLEAR | Concept was mentioned, but heuristic mode cannot reliably judge correctness. | Configure an OpenAI-compatible LLM endpoint for grounded semantic evaluation. |
| integer | UNCLEAR | Concept was mentioned, but heuristic mode cannot reliably judge correctness. | Configure an OpenAI-compatible LLM endpoint for grounded semantic evaluation. |
| matrix | UNCLEAR | Concept was mentioned, but heuristic mode cannot reliably judge correctness. | Configure an OpenAI-compatible LLM endpoint for grounded semantic evaluation. |
| merge | UNCLEAR | Concept was mentioned, but heuristic mode cannot reliably judge correctness. | Configure an OpenAI-compatible LLM endpoint for grounded semantic evaluation. |
| row | UNCLEAR | Concept was mentioned, but heuristic mode cannot reliably judge correctness. | Configure an OpenAI-compatible LLM endpoint for grounded semantic evaluation. |
| tokens | UNCLEAR | Concept was mentioned, but heuristic mode cannot reliably judge correctness. | Configure an OpenAI-compatible LLM endpoint for grounded semantic evaluation. |
| values | UNCLEAR | Concept was mentioned, but heuristic mode cannot reliably judge correctness. | Configure an OpenAI-compatible LLM endpoint for grounded semantic evaluation. |
| vector | UNCLEAR | Concept was mentioned, but heuristic mode cannot reliably judge correctness. | Configure an OpenAI-compatible LLM endpoint for grounded semantic evaluation. |
| vocabulary | UNCLEAR | Concept was mentioned, but heuristic mode cannot reliably judge correctness. | Configure an OpenAI-compatible LLM endpoint for grounded semantic evaluation. |

### Priority review

- UTF-8 and bytes
- Byte-level BPE
- Token IDs
- Embedding lookup
- byte

## 3. Clean Transcript

I think UTF-8 turns text into numbers. Wait, more precisely it turns Unicode characters into bytes. Why is the byte vocabulary 256 instead of 26? Because one byte has 8 bits and each bit has two states, so 2 to the 8 is 256. Then BPE finds frequent adjacent pairs and merges them.

I am still mixing up byte values and token IDs. If I see 231, is that a token ID or a byte value? It depends on which stage I am looking at. I need to track the representation. A token ID like 426 is just an integer index. Then embedding 426 means, no, that wording is bad. The model uses token ID 426 to select row 426 from the embedding matrix. That row is a vector, not a probability.

I understand one token can map to four embedding numbers, but if there are three tokens with four numbers each, why is that two dimensional? I guess the first axis is which token and the second axis is which feature, but I am not fully stable on what an axis means.


## Limitations

- Heuristic mode cannot infer deep misconceptions or stable learning traits.
- A single session should only support session-level hypotheses.
- Heuristic mode checks mention overlap only and does not claim conceptual correctness.
- Set LEARN_TRACE_LLM_BASE_URL and LEARN_TRACE_LLM_MODEL for grounded concept diagnosis.
