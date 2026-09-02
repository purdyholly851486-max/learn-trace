# Learn Trace v0.1 Architecture

## Core principle

Speech capture is infrastructure. The product value begins after transcription.
Learn Trace keeps Cognitive Diagnosis and Concept Diagnosis as separate engines because they answer different questions and require different evidence.

## Runtime topology

```text
Browser at localhost:7860
  |
  +-- reference material upload
  |      |
  |      v
  |   local session/materials
  |
  +-- microphone start/stop
         |
         v
      audio.wav
         |
         v
      ASR adapter
      |   |   |
      |   |   +-- qwen_server
      |   +------ qwen_local
      +---------- manual transcript fallback
         |
         v
   raw_transcript.txt
         |
         v
   clean_transcript.md
         |
      +--+-------------------+
      |                      |
      v                      v
Cognitive Engine        Concept Engine
think-aloud evidence    uploaded material
      |                      |
      v                      v
observation             student claim
hypothesis              reference concept
confidence              correctness status
intervention            correction
      |                      |
      +----------+-----------+
                 v
              report.md
              JSON files
```

## Trust boundary

By default, session files remain under `data/sessions/` on the same machine running the server.

Local-only path:

```text
microphone -> local WAV -> local ASR -> local LLM -> local report
```

Hybrid path:

```text
microphone -> local WAV -> configured ASR/LLM endpoint -> local report
```

The UI should always make the selected ASR mode visible. Future versions should expose the analysis endpoint mode with the same clarity.

## Cognitive Engine contract

Input:

- cleaned think-aloud transcript

Output:

- direct observation
- short evidence excerpts
- session-level hypothesis
- confidence
- intervention
- dimension-level notes
- limitations

The engine must not turn one session into a stable personality, intelligence, or mental-health claim.

## Concept Engine contract

Input:

- cleaned student transcript
- uploaded reference material

Output per concept:

- concept name
- correct / partial / incorrect / unclear / not_observed
- student understanding
- transcript evidence
- reference understanding
- correction
- importance

Without reference material, correctness is not evaluated.
Without a semantic LLM, the fallback only detects concept mentions and returns `unclear`.

## Why no database in v0.1

A folder-per-session structure is easier to inspect, fork, export to Obsidian, version, and debug. A database becomes useful only when longitudinal learner state is added.

## Planned boundary for v0.2+

Long-term learner state should be a separate layer above session reports, not mixed into single-session diagnosis.

```text
session diagnosis history
        |
        v
learner_state.json
        |
        v
recurring misconception / strategy pattern
```
