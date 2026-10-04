"""Data contracts shared by audio, algorithms and evaluation."""
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal
import numpy as np

FeatureType = Literal["ste", "ma", "logste", "logma"]
Algorithm = Literal["histogram"]
BinaryLabel = Literal["speech", "silence"]
OriginalLabel = Literal["sil", "v", "uv"]

@dataclass
class GroundTruthSegment:
    """Interval in seconds, retaining the original and binary labels."""
    start: float
    end: float
    original_label: OriginalLabel
    label: BinaryLabel

@dataclass
class AudioSignal:
    name: str
    wav_path: Path
    fs: int
    signal: np.ndarray
    duration_sec: float
    is_phone: bool  # Metadata for SNR analysis, not threshold selection.
    gt_segments: list[GroundTruthSegment]
    gt_boundaries: list[float]  # Speech/silence transitions in seconds.

@dataclass
class FrameSignal:
    """Frame arrays have shape (n_frames, frame_len); centers are seconds."""
    frames: np.ndarray
    timestamps: np.ndarray
    frame_len: int
    frame_shift: int
    fs: int
    raw_frames: np.ndarray

@dataclass
class ShortTimeFeatures:
    """One selected feature with raw and transformed values per frame."""
    feature_type: FeatureType
    raw_values: np.ndarray  # STE or MA sums before the optional log transform.
    values: np.ndarray  # Values used for training and prediction.
    timestamps: np.ndarray

@dataclass
class Threshold:
    """One method's threshold learned on train and reused on test."""
    algorithm: Algorithm
    feature_type: FeatureType
    value: float
    debug: dict[str, np.ndarray | float] = field(default_factory=dict)

@dataclass
class SegmentationResult:
    signal_name: str
    algorithm: Algorithm
    threshold_used: float
    timestamps: np.ndarray
    raw_decisions: np.ndarray  # 0 = Silence; 1 = Speech.
    filtered_decisions: np.ndarray
    predicted_boundaries: list[float]
    segments: list[tuple[float, float, BinaryLabel]]

@dataclass
class EvaluationMetrics:
    signal_name: str
    environment: str
    algorithm: Algorithm
    threshold: float
    mae_ms: float
    rmse_ms: float
    predicted_boundaries: list[float]
    gt_boundaries: list[float]
    matched_count: int = 0
    unmatched_predictions: int = 0
    unmatched_ground_truth: int = 0
    matched_pairs: list[tuple[float, float]] = field(default_factory=list)  # (predicted, GT) seconds.
    errors_ms: list[float] = field(default_factory=list)  # Signed predicted-minus-GT errors.
    unmatched_predicted_boundaries: list[float] = field(default_factory=list)
    unmatched_gt_boundaries: list[float] = field(default_factory=list)
    matching_tolerance_ms: float = 100.0
