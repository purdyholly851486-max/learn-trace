# Learn Trace v0.1

Learn Trace is a local-first learning diagnosis prototype. It records a learner's own think-aloud trace, grounds concept evaluation in uploaded course material, and produces two separate outputs:

1. Cognitive Engine: evidence-grounded session-level learning-process hypotheses.
2. Concept Engine: concept precision checks against uploaded PDF/Markdown/TXT material.

This is intentionally not an AI note taker. The first question is not "what did the lecture say?" but "what did the learner actually understand, confuse, correct, or fail to stabilize?"

## Architecture

```text
Browser microphone / manual transcript
              |
              v
         WAV / transcript
              |
       clean + segment
              |
      +-------+--------+
      |                |
      v                v
Cognitive Engine   Concept Engine
think-aloud rubric reference material
      |                |
      +-------+--------+
              v
      Learning Diagnosis
        JSON + Markdown
```

## Product shape

The app runs locally at `http://127.0.0.1:7860`.

- Browser UI: HTML/CSS/JavaScript
- Local API: FastAPI
- Audio capture: browser Web Audio API, encoded to WAV
- ASR adapters: manual, Qwen3-ASR local, Qwen3-ASR server
- Materials: PDF, Markdown, TXT
- Storage: local folders and JSON/Markdown; no database
- Semantic analysis: optional OpenAI-compatible endpoint

All session files are stored under `data/sessions/` by default.

## Quick start: no ASR model required

This is the easiest way to validate the core product idea before downloading a speech model.

```bash
./run.sh
```

Open:

```text
http://127.0.0.1:7860
```

Then:

1. Create a session.
2. Upload `samples/lecture_notes.md`.
3. Paste `samples/sample_transcript.txt` into the manual transcript field.
4. Click `END SESSION AND DIAGNOSE`.

Without a configured semantic LLM, Learn Trace uses conservative heuristics. It does not claim concept correctness in heuristic mode.

## Optional semantic analysis

Learn Trace can use any OpenAI-compatible chat-completions endpoint, including a local model server.

Set:

```bash
export LEARN_TRACE_LLM_BASE_URL=http://127.0.0.1:11434/v1
export LEARN_TRACE_LLM_MODEL=qwen3:8b
export LEARN_TRACE_LLM_API_KEY=EMPTY
```

Then restart the app.

When enabled:

- Cognitive Engine returns observation, evidence, session-level hypothesis, confidence, and intervention.
- Concept Engine compares student claims against uploaded reference material and labels concepts as `correct`, `partial`, `incorrect`, `unclear`, or `not_observed`.

## UI language, storage location, and Obsidian

The UI has an EN / 中文 toggle (top right). The choice is remembered per browser.

The Storage settings panel lets you pick where sessions are saved. Point it at a folder inside an Obsidian vault and every finished session writes an Obsidian-ready `report.md` (YAML frontmatter with `learn-trace` tags) plus `clean_transcript.md`. The setting persists in `settings.local.json` (git-ignored) and can be reset to the default `data/sessions/` from the same panel.

Absolute paths may point anywhere on disk; relative paths must stay inside the project.

## Qwen3-ASR local

On Apple Silicon, Learn Trace uses the community-maintained `mlx-qwen3-asr` runtime so inference runs through MLX/Metal instead of PyTorch. The model weights are the official `Qwen/Qwen3-ASR-0.6B` release.

The project already has an isolated `.venv`. Install the MLX ASR requirements into it once:

```bash
. .venv/bin/activate
pip install -r requirements-qwen.txt
```

Download the official 0.6B weights to iCloud Drive. Qwen recommends ModelScope for users in Mainland China:

```bash
modelscope download --model Qwen/Qwen3-ASR-0.6B \
  --local_dir "$HOME/Library/Mobile Documents/com~apple~CloudDocs/LearnTrace/models/Qwen3-ASR-0.6B"
```

In Finder, open `iCloud Drive/LearnTrace/models`, right-click `Qwen3-ASR-0.6B`, and choose **Keep Downloaded**. This prevents macOS from evicting the model files while retaining the iCloud copy.

Then either select `Qwen3-ASR local` in the UI or set:

```bash
export LEARN_TRACE_ASR_PROVIDER=qwen_local
```

The local model path is configured in `config.yaml`:

```yaml
asr:
  provider: qwen_local
  qwen_local:
    model: /Users/os/Library/Mobile Documents/com~apple~CloudDocs/LearnTrace/models/Qwen3-ASR-0.6B
    device: mlx
    dtype: auto
```

You can override the path without editing YAML:

```bash
export LEARN_TRACE_QWEN_MODEL="/absolute/path/to/Qwen3-ASR-0.6B"
```

The adapter loads the model only when transcription is requested and keeps it in memory for later recordings. With a complete local model folder, inference works with `HF_HUB_OFFLINE=1` and does not call a cloud ASR API.

Repeat the 16.96-second Chinese smoke test in forced-offline mode:

```bash
HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 \
  .venv/bin/python tests/qwen_local_test.py
```

The included test audio says:

```text
今天我正在测试学习轨迹的本地语音识别功能。这个模型运行在我的苹果电脑上，音频不会发送到云端。完成转写以后，我会检查文字是否准确，并把结果保存到本地。
```

## Qwen3-ASR server mode

If Qwen3-ASR is already exposed through an OpenAI-compatible ASR server, use `qwen_server`.

Default config:

```yaml
asr:
  qwen_server:
    base_url: http://127.0.0.1:8000/v1
    api_key: EMPTY
```

This keeps the Learn Trace web app lightweight while allowing the speech model to run in a separate process or machine.

## Session files

Each session is self-contained:

```text
data/sessions/<session-id>/
  session.json
  audio.wav
  raw_transcript.txt
  clean_transcript.md
  cognitive.json
  concepts.json
  report.md
  materials/
```

`audio.wav` exists only when microphone recording was used.

## Cognitive Engine guardrails

The Cognitive Engine deliberately avoids personality or mental-health diagnosis. A single learning session can support only a session-level hypothesis.

The initial rubric focuses on:

- Self-monitoring
- Error correction
- Concept boundaries
- Representation tracking
- Causal explanation
- Explanation structure

Each semantic diagnosis should contain direct transcript evidence and an explicit confidence score.

## Concept Engine grounding

Concept evaluation requires uploaded reference material. The intended semantic path is:

```text
Reference material -> course concepts / relevant evidence
Student transcript -> student claims
Student claims <-> reference concepts
Correct / Partial / Incorrect / Unclear
```

If no semantic LLM is configured, the fallback only detects material-derived concept mentions and marks them `unclear`. It does not fabricate correctness labels.

## Current v0.1 limitations

- No real-time ASR transcript yet; audio is transcribed after Stop.
- No system-audio capture from ChatGPT or other browser tabs.
- PDF extraction is text-based; scanned PDFs need OCR outside this prototype.
- Heuristic analysis is intentionally conservative.
- Long-term learner state / knowledge tracing is not implemented yet.
- Native desktop packaging is intentionally deferred.

## Suggested next milestones

- v0.2: streaming ASR and transcript timeline.
- v0.3: persistent learner state across sessions.
- v0.4: evidence-linked concept map and misconception history.
- v0.5: optional Tauri desktop wrapper after the core diagnosis is validated.

## Why local-first

The goal is to make the default path simple: a learner can run the app on their own machine, keep raw audio and materials local, and choose whether ASR and semantic analysis also run locally or through configured APIs.

## References used for the ASR adapter

- Qwen3-ASR official repository: https://github.com/QwenLM/Qwen3-ASR
- Apple Silicon MLX runtime: https://github.com/moona3k/mlx-qwen3-asr

The Qwen adapter is deliberately isolated from the learning-analysis engines so the ASR backend can be replaced without changing the product logic.
