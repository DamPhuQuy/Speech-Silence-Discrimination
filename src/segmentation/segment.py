import numpy as np

from src.features.extraction import extract_features
from src.features.framing import apply_framing
from src.models import AudioSignal, SegmentationResult
from src.segmentation.postprocess import extract_boundaries_and_segments, filter_short_silence


def segment_signal(
    signal: AudioSignal,
    threshold: float,
    algorithm: str = "binary",
    min_silence_ms: float = 200.0,
    frame_size_ms: float = 25.0,
    frame_shift_ms: float = 10.0,
    window_type: str = "hamming",
) -> SegmentationResult:
    framed = apply_framing(
        signal,
        frame_size_ms=frame_size_ms,
        frame_shift_ms=frame_shift_ms,
        window_type=window_type,
    )

    feats = extract_features(framed)
    ste: np.ndarray = feats.ste_norm
    num_frames: int = len(ste)

    raw_decisions: np.ndarray = np.zeros(num_frames, dtype=int)
    for i in range(num_frames):
        if ste[i] >= threshold:
            raw_decisions[i] = 1
        else:
            raw_decisions[i] = 0

    filtered_decisions: np.ndarray = filter_short_silence(
        raw_decisions,
        frame_shift_ms=frame_shift_ms,
        min_silence_ms=min_silence_ms,
    )

    boundaries, segments = extract_boundaries_and_segments(
        framed.timestamps,
        filtered_decisions,
    )

    return SegmentationResult(
        signal_name=signal.name,
        algorithm=algorithm,
        threshold_used=threshold,
        timestamps=framed.timestamps,
        raw_decisions=raw_decisions,
        filtered_decisions=filtered_decisions,
        predicted_boundaries=boundaries,
        segments=segments,
    )
