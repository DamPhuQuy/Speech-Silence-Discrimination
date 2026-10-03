"""Merge short internal silence runs and convert frame labels to regions."""
import numpy as np
from src.models import BinaryLabel

def merge_short_silences(decisions: np.ndarray, frame_shift_ms: float, min_silence_ms: float = 200.0) -> np.ndarray:
    """Return a copy with internal silence runs shorter than the minimum filled.

    Decisions are 0/False=silence and 1/True=speech. For uniformly spaced frame
    centers, an internal run of N frames occupies N * frame_shift_ms, matching
    midpoint-based boundaries. Use the actual sample-derived frame shift when
    it differs from the requested shift; overlapping frame length is not run
    duration. Runs exactly at the minimum (default 200 ms) remain silence.
    Preserve start/end silence, including all-silence input: only runs bounded
    by speech on both sides are merged. Preserve input shape and dtype without
    in-place edits; empty and all-speech inputs return independent copies.
    """
    for name, value in (("frame_shift_ms", frame_shift_ms), ("min_silence_ms", min_silence_ms)):
        if isinstance(value, (bool, np.bool_)) or not isinstance(value, (int, float, np.integer, np.floating)):
            raise ValueError(f"{name} must be a finite positive real number.")
        try:
            valid = np.isfinite(float(value)) and float(value) > 0
        except (OverflowError, ValueError):
            valid = False
        if not valid:
            raise ValueError(f"{name} must be a finite positive real number.")
    labels = np.asarray(decisions)
    if labels.ndim != 1 or labels.dtype.kind not in "biuf" or not np.all(np.isin(labels, (0, 1))):
        raise ValueError("Decisions must be a one-dimensional array of 0/1 labels.")
    filtered = labels.copy()

    # Inspect complete runs in the original labels; edge silence stays intact.
    i = 0
    while i < len(labels):
        if labels[i] == 1:
            i += 1
            continue
        start = i
        while i < len(labels) and labels[i] == 0:
            i += 1
        if start > 0 and i < len(labels):
            duration_ms = (i - start) * float(frame_shift_ms)
            if duration_ms < float(min_silence_ms):
                filtered[start:i] = 1
    return filtered

def decisions_to_segments(decisions: np.ndarray, timestamps: np.ndarray, duration_sec: float) -> list[tuple[float, float, BinaryLabel]]:
    """Convert 0/1 frame labels to intervals, placing transitions halfway between centers.

    Extend the first/last labels to 0/duration_sec. No silence merging is applied.
    Empty arrays return no segments; timestamps must increase within the WAV.
    """
    labels, times = np.asarray(decisions), np.asarray(timestamps, dtype=np.float64)
    if labels.ndim != 1 or times.shape != labels.shape or not np.all(np.isin(labels, (0, 1))):
        raise ValueError("Decisions and timestamps must be matching 1-D arrays with 0/1 labels.")
    if not np.isfinite(duration_sec) or duration_sec <= 0:
        raise ValueError("Duration must be finite and positive.")
    if not np.all(np.isfinite(times)) or np.any(times < 0) or np.any(times > duration_sec) or np.any(np.diff(times) <= 0):
        raise ValueError("Frame timestamps must increase within the audio duration.")
    if not labels.size:
        return []
    segments = []
    start = 0.0
    for i in range(1, len(labels)):
        if labels[i] != labels[i - 1]:
            boundary = float((times[i - 1] + times[i]) / 2)
            segments.append((start, boundary, "speech" if labels[i - 1] else "silence"))
            start = boundary
    segments.append((start, float(duration_sec), "speech" if labels[-1] else "silence"))
    return segments

def segment_boundaries(segments: list[tuple[float, float, BinaryLabel]]) -> list[float]:
    """Extract internal speech/silence transitions in seconds."""
    return [current[0] for previous, current in zip(segments, segments[1:])
            if abs(previous[1] - current[0]) <= 1e-9 and previous[2] != current[2]]
