"""Ground truth parsing and binary label conversion."""
from pathlib import Path
import numpy as np
from src.models import GroundTruthSegment, OriginalLabel, BinaryLabel

def to_binary_label(label: OriginalLabel) -> BinaryLabel:
    """Map sil to silence and both v and uv to speech."""
    if label == "sil":
        return "silence"
    if label in ("v", "uv"):
        return "speech"
    raise ValueError(f"Unknown LAB segmentation label: {label}")

def parse_labels(path: Path) -> list[GroundTruthSegment]:
    """Read labeled intervals in seconds; ignore final F0mean/F0std rows."""
    segments = []
    for line_number, line in enumerate(Path(path).read_text(encoding="utf-8-sig").splitlines(), 1):
        fields = line.split()
        if not fields or fields[0].lower() in ("f0mean", "f0std"):
            continue
        try:
            if len(fields) != 3:
                raise ValueError("Expected start, end and label.")
            start, end = float(fields[0]), float(fields[1])
            label = to_binary_label(fields[2])
            if not np.isfinite(start) or not np.isfinite(end) or start < 0 or end <= start:
                raise ValueError("Intervals must be finite with 0 <= start < end.")
            if segments and start < segments[-1].end:
                raise ValueError("Intervals must be ordered and nonoverlapping.")
        except ValueError as exc:
            raise ValueError(f"{path}:{line_number}: {exc}") from exc
        segments.append(GroundTruthSegment(start, end, fields[2], label))
    if not segments:
        raise ValueError(f"No segmentation intervals in {path}")
    return segments

def speech_silence_boundaries(segments: list[GroundTruthSegment]) -> list[float]:
    """Return binary transitions; merge adjacent speech labels v/uv."""
    return [current.start for previous, current in zip(segments, segments[1:])
            if abs(previous.end - current.start) <= 1e-9 and previous.label != current.label]


def labels_at_timestamps(segments: list[GroundTruthSegment], timestamps: np.ndarray) -> np.ndarray:
    """Map second-valued frame centers into half-open LAB intervals [start, end).

    Return 0=silence, 1=speech, -1=uncovered. Gaps and LAB tail differences are
    never silently filled; callers must exclude uncovered frames from scoring.
    """
    times = np.asarray(timestamps, dtype=np.float64)
    if times.ndim != 1 or not np.all(np.isfinite(times)):
        raise ValueError("Timestamps must be a finite one-dimensional array.")
    labels = np.full(times.shape, -1, dtype=np.int64)
    for segment in segments:
        covered = (times >= segment.start) & (times < segment.end)
        if np.any(labels[covered] != -1):
            raise ValueError("LAB intervals overlap at frame timestamps.")
        labels[covered] = 1 if segment.label == "speech" else 0
    return labels
