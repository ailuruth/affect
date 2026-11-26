"""The recogniser adapters and audio helpers of checks 4 and 5. Every model runtime is imported lazily, inside a
function, after the calling check's approval (Q34 items 4, 5, 10); models load from local paths only (A17's
models.lock, written by download_models), with the hub offline.

Written without a Mac or the models in this session: the Kyutai adapter follows the MLX inference script of Kyutai's
delayed-streams-modeling repository (24 kHz, 1920-sample frames at 12.5 Hz, `LmGen.step` per frame). If its API
differs on the Mac, only this file changes; the measurement and thresholds do not.
"""
from __future__ import annotations

import json
import os
import subprocess
import time
import wave
from pathlib import Path

from tools.week0 import common

os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("HF_HUB_DISABLE_TELEMETRY", "1")
MODELS_DIR = Path(os.environ.get("AFFECT_MODELS_DIR", Path.home() / "affect-models"))
READING = Path(__file__).with_name("reading.txt")
RECORDING = "reading.wav"
FRAME_S = 0.08                                  # Kyutai: 1920 samples at 24 kHz


def load_wav(path: Path, rate: int):
    """Mono float32 at `rate`. Non-WAV files are converted with macOS's own afconvert first (kept local)."""
    import numpy as np
    from scipy.signal import resample_poly
    path = Path(path)
    if path.suffix.lower() != ".wav":
        out = path.with_suffix(".converted.wav")
        subprocess.run(["afconvert", "-f", "WAVE", "-d", "LEI16", str(path), str(out)], check=True)
        path = out
    with wave.open(str(path)) as w:
        sr, ch, width = w.getframerate(), w.getnchannels(), w.getsampwidth()
        raw = w.readframes(w.getnframes())
    if width != 2:
        raise common.Refused(f"{path.name}: 16-bit PCM WAV expected")
    x = np.frombuffer(raw, dtype="<i2").astype(np.float32).reshape(-1, ch).mean(axis=1) / 32768.0
    if sr != rate:
        from math import gcd
        g = gcd(sr, rate)
        x = resample_poly(x, rate // g, sr // g).astype(np.float32)
    return x


def save_wav(path: Path, x, rate: int) -> None:
    import numpy as np
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(rate)
        w.writeframes((np.clip(x, -1, 1) * 32767).astype("<i2").tobytes())


def record(seconds: float, rate: int = 24000):
    """Record from the default microphone (lazily imported `sounddevice`; the microphone opens only now)."""
    sd = common.lazy("sounddevice", "uv pip install sounddevice (an addition to the mac extra, to approve)")
    print(f"recording {seconds:.0f} s: read tools/week0/reading.txt aloud at your normal pace now ...")
    x = sd.rec(int(seconds * rate), samplerate=rate, channels=1, dtype="float32")
    sd.wait()
    return x[:, 0]


def reading_audio(args, rate: int):
    """The 5-minute reading: --wav (a recording he made), the kept local recording, or a new recording."""
    if getattr(args, "wav", None):
        return load_wav(Path(args.wav), rate)
    kept = common.WEEK0_DIR / RECORDING
    if kept.is_file():
        return load_wav(kept, rate)
    x = record(getattr(args, "seconds", 300.0), 24000)
    save_wav(common.local_path(RECORDING), x, 24000)
    return load_wav(kept, rate)


# ------------------------------------------------------------------------------------------------ Whisper-small
def utterance_recogniser(language: str | None = None):
    """Callable audio (16 kHz float32) -> (text, [(word, start_s, end_s)]) with mlx-whisper on local weights."""
    mw = common.lazy("mlx_whisper", "uv sync --extra engine --extra mac")
    path = MODELS_DIR / "whisper_small"
    if not path.is_dir():
        raise common.Refused(f"{path} not found: run tools.week0.download_models first")

    def run(audio):
        out = mw.transcribe(audio, path_or_hf_repo=str(path), word_timestamps=True, language=language,
                            condition_on_previous_text=False)
        words = [(w["word"].strip(), float(w["start"]), float(w["end"]))
                 for seg in out.get("segments", []) for w in seg.get("words", [])]
        return out.get("text", ""), words
    return run


# ------------------------------------------------------------------------------------------------ Kyutai STT 1B
def stream_recogniser():
    """Callable audio (24 kHz float32) -> [(frame_index, compute_s, piece)] for every non-empty text piece, plus the
    per-frame compute times as the attribute `last_compute` of the callable (for the real-time queue)."""
    mx = common.lazy("mlx.core", "uv sync --extra engine --extra mac")
    nn = common.lazy("mlx.nn", "uv sync --extra engine --extra mac")
    rustymimi = common.lazy("rustymimi", "uv sync --extra engine --extra mac")
    spm = common.lazy("sentencepiece", "uv sync --extra engine --extra mac")
    models = common.lazy("moshi_mlx.models", "uv sync --extra engine --extra mac")
    utils = common.lazy("moshi_mlx.utils", "uv sync --extra engine --extra mac")
    import numpy as np
    root = MODELS_DIR / "kyutai_stt_1b_en_fr"
    if not (root / "config.json").is_file():
        raise common.Refused(f"{root} not found: run tools.week0.download_models first")
    cfg = json.loads((root / "config.json").read_text())
    lm_config = models.LmConfig.from_config_dict(cfg)
    model = models.Lm(lm_config)
    model.set_dtype(mx.bfloat16)
    weights = root / cfg.get("moshi_name", "model.safetensors")
    if weights.name.endswith(".q4.safetensors"):
        nn.quantize(model, bits=4, group_size=32)
    elif weights.name.endswith(".q8.safetensors"):
        nn.quantize(model, bits=8, group_size=64)
    model.load_weights(str(weights), strict=True)
    text_tok = spm.SentencePieceProcessor(str(root / cfg["tokenizer_name"]))
    other = lm_config.other_codebooks
    mimi = rustymimi.Tokenizer(str(root / cfg["mimi_name"]), num_codebooks=max(lm_config.generated_codebooks, other))
    model.warmup()

    def run(audio):
        steps = len(audio) // 1920
        gen = models.LmGen(model=model, max_steps=steps + 1, text_sampler=utils.Sampler(top_k=25, temp=0),
                           audio_sampler=utils.Sampler(top_k=250, temp=0.8), check=False)
        pcm = np.asarray(audio, dtype=np.float32)[None, :]
        out, compute = [], []
        for i in range(steps):
            t0 = time.perf_counter()
            block = pcm[:, i * 1920:(i + 1) * 1920][None, :, :]
            toks = mx.array(mimi.encode_step(block)).transpose(0, 2, 1)[:, :, :other]
            tok = gen.step(toks[0])[0].item()
            compute.append(time.perf_counter() - t0)
            if tok not in (0, 3):
                out.append((i, compute[-1], text_tok.id_to_piece(tok)))
        run.last_compute = compute
        return out
    run.last_compute = []
    return run


def stream_words(pieces):
    """Join sentencepiece pieces into words: [(word, frame_of_last_piece)]."""
    words = []
    for frame, _, piece in pieces:
        if piece.startswith("▁") or not words:
            words.append([piece.lstrip("▁"), frame])
        else:
            words[-1][0] += piece
            words[-1][1] = frame
    return [(w, f) for w, f in words if w]
