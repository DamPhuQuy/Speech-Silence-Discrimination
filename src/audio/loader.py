"""Assemble an audio recording, optionally with ground truth."""
from pathlib import Path
from src.models import AudioSignal
from src.audio.wav import read_wav
from src.audio.labels import parse_labels, speech_silence_boundaries


def load_audio(wav_path: Path, lab_path: Path | None = None) -> AudioSignal:
    """Return normalized mono audio and metadata using the WAV's actual Fs.

    With no lab_path, return empty ground truth for input-only processing.
    Explicit LAB loading delegates to the shared label parser.
    """
    wav_path = Path(wav_path)
    fs, samples = read_wav(wav_path)
    segments = parse_labels(Path(lab_path)) if lab_path is not None else []
    boundaries = speech_silence_boundaries(segments) if lab_path is not None else []
    return AudioSignal(
        name=wav_path.stem, wav_path=wav_path, fs=fs, signal=samples,
        duration_sec=len(samples) / fs,
        is_phone=wav_path.stem.lower().startswith("phone_"),
        gt_segments=segments, gt_boundaries=boundaries,
    )
