#!/usr/bin/env sh
set -eu
if [ ! -d .venv ]; then
  python3 -m venv .venv
fi
. .venv/bin/activate
if ! python -c "import fastapi, mlx_qwen3_asr, uvicorn, yaml" >/dev/null 2>&1; then
  python -m pip install -r requirements-qwen.txt
fi
python -m uvicorn backend.main:app --host 127.0.0.1 --port 7860
