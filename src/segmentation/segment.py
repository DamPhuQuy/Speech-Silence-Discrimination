import numpy as np

from src.features.extraction import extract_features
from src.features.framing import apply_framing
from src.models import AudioSignal, SegmentationResult
from src.segmentation.postprocess import (
    extract_boundaries_and_segments,
    filter_short_silence,
)


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
    algo_lower = algorithm.lower()

    if algo_lower == "histogram":
        feature_vals: np.ndarray = feats.log_ste
    else:
        feature_vals = feats.ste_norm

    raw_decisions = (feature_vals >= threshold).astype(int)

    # Hậu xử lý theo đúng yêu cầu đề bài: Gộp các khoảng lặng ngắn (< 200ms)
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
