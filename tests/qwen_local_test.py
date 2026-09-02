from pathlib import Path
import sys
from time import perf_counter

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import mlx.core as mx

from backend.asr.factory import build_asr
from backend.config import CONFIG


def main() -> None:
    audio_path = Path("samples/qwen_zh_test.wav")
    assert audio_path.exists(), f"Missing test audio: {audio_path}"

    asr_config = CONFIG["asr"]
    model_path = Path(asr_config["qwen_local"]["model"])
    assert model_path.is_dir(), f"Missing local model folder: {model_path}"
    assert (model_path / "model.safetensors").is_file(), "Missing model weights"

    print("MLX device:", mx.default_device())
    print("Model path:", model_path)
    started = perf_counter()
    transcript = build_asr(asr_config, provider="qwen_local").transcribe(audio_path)
    print("Transcript:", transcript)
    print(f"Elapsed: {perf_counter() - started:.2f}s")


if __name__ == "__main__":
    main()
