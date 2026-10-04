"""Orchestration only: load -> frame -> feature -> train -> predict -> evaluate."""
from dataclasses import asdict
import hashlib
from pathlib import Path
from typing import Any

import numpy as np

from src.audio.framing import frame_signal
from src.audio.labels import labels_at_timestamps, parse_labels, speech_silence_boundaries
from src.audio.loader import load_audio
from src.config import Config, load_frozen_histogram
from src.evaluate.metrics import boundary_mae_ms, boundary_rmse_ms, evaluate_result
from src.evaluate.snr import (
    POWER_CONTRAST_NAME, POWER_CONTRAST_DEFINITION,
    analyze_background_noise, estimate_snr_db,
)
from src.features.ma import compute_ma
from src.features.normalize import log_transform
from src.features.ste import compute_ste
from src.models import (
    AudioSignal, FrameSignal, SegmentationResult,
    ShortTimeFeatures, Threshold,
)
from src.segmentation.histogram import predict, train_histogram
from src.segmentation.postprocess import (
    decisions_to_segments, merge_short_silences, segment_boundaries,
)


def prepare_frames(signal: AudioSignal, config: Config) -> FrameSignal:
    """Frame mono audio using configured durations and its actual Fs."""
    return frame_signal(signal, config.frame_duration_ms, config.frame_shift_ms)


def extract_features(frames: FrameSignal, config: Config) -> ShortTimeFeatures:
    """Return selected sum feature, optionally logged, with frame timestamps.

    Audio is already PCM-scaled; no additional feature normalization is applied.
    Each row produces one STE/MA value and retains its original frame center.
    """
    if config.feature_type not in ("ste", "ma", "logste", "logma"):
        raise ValueError(f"Unsupported feature type: {config.feature_type}")
    raw = compute_ste(frames.frames) if config.feature_type in ("ste", "logste") else compute_ma(frames.frames)
    if frames.timestamps.shape != raw.shape:
        raise ValueError("Each frame must have exactly one timestamp and feature.")
    values = log_transform(raw, config.epsilon) if config.feature_type.startswith("log") else raw.copy()
    return ShortTimeFeatures(config.feature_type, raw, values, frames.timestamps.copy())


def train_histogram_from_training_set(
    training_directory: Path, config: Config, *, weight: float,
    min_peak_distance: int = 2, min_relative_height: float = 0.1,
) -> tuple[Threshold, dict[str, object]]:
    """Fit one common threshold from all WAVs in the supplied training directory.

    Discover direct child WAVs in filename order; never load LAB or other
    directories. Reuse production audio/framing/features and concatenate the
    frame vectors before calling train_histogram exactly once. The caller
    supplies training-only data and parameters selected before fitting.
    Return the Threshold and JSON-serializable parameters/per-file frame counts.
    """
    directory = Path(training_directory).resolve()
    if not directory.is_dir():
        raise ValueError(f"Training directory does not exist: {directory}")
    if config.histogram_bins is None or config.histogram_smoothing_window is None:
        raise ValueError("Set histogram_bins and histogram_smoothing_window before training.")
    paths = sorted(
        (p for p in directory.iterdir() if p.is_file() and p.suffix.lower() == ".wav"),
        key=lambda p: p.name,
    )
    if not paths:
        raise ValueError(f"No training WAV files found in {directory}")

    # Collect every training feature vector without reading ground truth.
    vectors, file_reports = [], []
    for path in paths:
        audio = load_audio(path)
        frames = prepare_frames(audio, config)
        features = extract_features(frames, config)
        if not features.values.size:
            raise ValueError(f"Training WAV has no complete frames: {path.name}")
        vectors.append(features.values)
        file_reports.append({
            "wav": path.name, "fs": audio.fs, "frames": len(features.values),
            "frame_length_samples": frames.frame_len,
            "frame_shift_samples": frames.frame_shift,
        })

    # Estimate one common training threshold from the pooled frame values.
    combined = np.concatenate(vectors)
    model = train_histogram(
        combined, config.histogram_bins, config.histogram_smoothing_window, weight,
        feature_type=config.feature_type, min_peak_distance=min_peak_distance,
        min_relative_height=min_relative_height,
    )
    report = {
        "training_directory": str(directory), "number_of_wavs": len(paths),
        "files": file_reports, "feature": config.feature_type,
        "total_combined_frames": len(combined),
        "parameters": {
            "frame_duration_ms": config.frame_duration_ms,
            "frame_shift_ms": config.frame_shift_ms, "epsilon": config.epsilon,
            "num_bins": config.histogram_bins,
            "smooth_window": config.histogram_smoothing_window, "weight": weight,
            "min_peak_distance": min_peak_distance,
            "min_relative_height": min_relative_height,
        },
        "m1": model.debug["m1"], "m2": model.debug["m2"],
        "threshold": model.value,
    }
    return model, report


def evaluate_histogram_on_training_set(
    training_directory: Path, model: Threshold, config: Config, *,
    tolerance_ms: float | None = None,
) -> dict[str, object]:
    """Evaluate training predictions with a previously fitted common threshold.

    No fit or tuning occurs. LAB is read after prediction and mapped to frame
    centers; uncovered centers are excluded from accuracy. Return per-frame
    labels, postprocessed boundaries, LAB intervals and boundary errors.
    """
    report = _evaluate_histogram_on_directory(
        training_directory, model, config, tolerance_ms=tolerance_ms,
    )
    report["training_directory"] = report.pop("dataset_directory")
    return report


def evaluate_histogram_on_test_set(
    test_directory: Path, model: Threshold, config: Config, *, tolerance_ms: float,
) -> dict[str, object]:
    """Evaluate all test WAVs using the supplied frozen feature and threshold.

    Reuse training validation's prediction/postprocessing/matching path. LAB
    follows prediction and supplies evaluation/noise analysis only. No fitting,
    peak selection, threshold calculation or parameter tuning occurs here.
    """
    report = _evaluate_histogram_on_directory(
        test_directory, model, config, tolerance_ms=tolerance_ms, include_noise=True,
    )
    report["test_directory"] = report.pop("dataset_directory")
    report["number_of_wavs"] = len(report["files"])
    return report


def evaluate_frozen_histogram(
    test_directory: Path, config: Config, model: Threshold,
    training_information: dict[str, Any],
) -> dict[str, Any]:
    """Evaluate all test recordings with the unchanged training-only model.

    Verify loaded settings, threshold and lock hash before/after evaluation.
    Return the frozen configuration, per-file diagnostics and pooled matched
    boundary errors. Report actual file count and any difference from four.
    """
    saved = training_information
    lock_path = Path(saved["lock_file"])
    frozen_config, frozen_threshold = asdict(config), model.value
    if (saved["selection_scope"] != "training_only" or saved["locked"] is not True
            or model.algorithm != "histogram" or model.feature_type != saved["feature"]
            or frozen_config != saved["config_snapshot"] or frozen_threshold != saved["threshold"]
            or hashlib.sha256(lock_path.read_bytes()).hexdigest() != saved["lock_sha256"]):
        raise ValueError("Use the unchanged configuration and threshold loaded from the training lock.")
    if config.min_silence_ms != 200.0:
        raise ValueError("The saved model must use the project's 200 ms silence minimum.")

    # Test labels only evaluate predictions; the existing model is never fitted.
    report = evaluate_histogram_on_test_set(
        test_directory, model, config, tolerance_ms=saved["evaluation_tolerance_ms"],
    )
    if (hashlib.sha256(lock_path.read_bytes()).hexdigest() != saved["lock_sha256"]
            or asdict(config) != frozen_config or model.value != frozen_threshold):
        raise RuntimeError("Frozen model or configuration changed during evaluation; results are not saved.")
    if any(row["threshold"] != frozen_threshold for row in report["files"]):
        raise RuntimeError("Every test recording must use the identical frozen threshold.")

    # Pool already matched pairs; never match boundaries across recordings.
    pairs = [pair for row in report["files"] for pair in row["boundary_evaluation"]["matched_pairs_sec"]]
    report.update(
        scope="test_evaluation_only", lock_file=str(lock_path),
        lock_sha256=saved["lock_sha256"], lock_unchanged=True,
        frozen_configuration={
            "feature": saved["feature"], "parameters": saved["parameters"],
            "m1": saved["m1"], "m2": saved["m2"], "threshold": frozen_threshold,
            "evaluation_tolerance_ms": saved["evaluation_tolerance_ms"],
        },
        total_frames=sum(row["frames"] for row in report["files"]),
        expected_number_of_wavs=4,
        file_count_warning=None if report["number_of_wavs"] == 4 else
        f"Expected four test WAVs, found {report['number_of_wavs']}; all actual files were processed.",
        noise_metric_name=POWER_CONTRAST_NAME,
        noise_metric_definition=POWER_CONTRAST_DEFINITION,
        aggregate_boundary_evaluation={
            "predicted_count": sum(row["boundary_evaluation"]["predicted_count"] for row in report["files"]),
            "gt_count": sum(row["boundary_evaluation"]["gt_count"] for row in report["files"]),
            "matched_count": len(pairs),
            "unmatched_predicted_count": sum(len(row["boundary_evaluation"]["unmatched_predicted_boundaries"]) for row in report["files"]),
            "unmatched_gt_count": sum(len(row["boundary_evaluation"]["unmatched_gt_boundaries"]) for row in report["files"]),
            "mae_ms": boundary_mae_ms(pairs) if pairs else None,
            "rmse_ms": boundary_rmse_ms(pairs) if pairs else None,
        },
    )
    return report


def run_final_evaluation(test_directory: Path, lock_path: Path) -> dict[str, Any]:
    """Load the saved training-only lock and delegate frozen test evaluation."""
    config, model, information = load_frozen_histogram(lock_path)
    return evaluate_frozen_histogram(test_directory, config, model, information)


def _background_noise_report(audio: AudioSignal) -> dict[str, object]:
    """Serialize existing LAB powers and the explicitly selected dB convention."""
    report = analyze_background_noise(audio)
    report["metric"] = "speech_to_silence_power"
    report["metric_name"] = POWER_CONTRAST_NAME
    report["contrast_db"] = None
    try:
        contrast = estimate_snr_db(audio, definition="speech_to_silence_power")
    except ValueError as exc:
        report.update(contrast_status="unavailable", reason=str(exc))
    else:
        if np.isfinite(contrast):
            report.update(contrast_db=contrast, contrast_status="finite")
        else:
            report["contrast_status"] = "positive_infinity" if contrast > 0 else "negative_infinity"
    return report


def _evaluate_histogram_on_directory(
    dataset_directory: Path, model: Threshold, config: Config, *,
    tolerance_ms: float | None = None, include_noise: bool = False,
) -> dict[str, object]:
    """Shared fit-free evaluation; optional LAB noise analysis follows prediction."""
    if model.algorithm != "histogram" or model.feature_type != config.feature_type:
        raise ValueError("Use the fitted Histogram model's feature type.")
    directory = Path(dataset_directory).resolve()
    if not directory.is_dir():
        raise ValueError(f"Dataset directory does not exist: {directory}")
    paths = sorted(
        (p for p in directory.iterdir() if p.is_file() and p.suffix.lower() == ".wav"),
        key=lambda p: p.name,
    )
    if not paths:
        raise ValueError("No dataset WAV files found.")

    reports = []
    for path in paths:
        # Prediction uses WAV features and the supplied T, without reading LAB.
        audio = load_audio(path)
        frames = prepare_frames(audio, config)
        features = extract_features(frames, config)
        if not features.values.size:
            raise ValueError(f"No complete frames in {path.name}")
        predicted = predict(features.values, model.value)
        filtered = merge_short_silences(
            predicted, frames.frame_shift * 1000 / frames.fs, config.min_silence_ms,
        )

        # Read ground truth after prediction, for scoring and analysis only.
        truth_segments = parse_labels(path.with_suffix(".lab"))
        truth = labels_at_timestamps(truth_segments, frames.timestamps)
        segments = decisions_to_segments(filtered, frames.timestamps, audio.duration_sec)
        audio.gt_segments = truth_segments
        audio.gt_boundaries = speech_silence_boundaries(truth_segments)
        result = SegmentationResult(
            audio.name, model.algorithm, model.value, frames.timestamps,
            predicted, filtered, segment_boundaries(segments), segments,
        )
        metrics = evaluate_result(audio, result, tolerance_ms)
        known = truth != -1

        # LAB gaps/tails stay uncovered instead of being extended to the WAV.
        warnings = []
        if truth_segments[0].start > 0:
            warnings.append(f"LAB starts at {truth_segments[0].start:.6f}s, after WAV start.")
        for previous, current in zip(truth_segments, truth_segments[1:]):
            if current.start - previous.end > 1e-9:
                warnings.append(f"LAB gap: {previous.end:.6f} to {current.start:.6f}s.")
        tail_ms = (audio.duration_sec - truth_segments[-1].end) * 1000
        if abs(tail_ms) > 1e-6:
            warnings.append(f"WAV end minus LAB end: {tail_ms:.3f} ms; labels are not extended.")
        if np.any(~known):
            warnings.append(f"{int(np.sum(~known))} frame centers lack ground truth; excluded from scoring.")

        # Mode/label counts are diagnostics; they do not recalculate threshold.
        modes = {}
        if "m1" in model.debug and "m2" in model.debug:
            midpoint = (model.debug["m1"] + model.debug["m2"]) / 2
            for name, mask in (("lower_feature_mode", features.values <= midpoint),
                               ("higher_feature_mode", features.values > midpoint)):
                selected = truth[known & mask]
                modes[name] = {
                    "frames": len(selected), "silence_frames": int(np.sum(selected == 0)),
                    "speech_frames": int(np.sum(selected == 1)),
                }
        # Known prefixes identify dataset groups, not measured room conditions.
        # An unfamiliar filename must not be silently described as studio.
        prefix = path.stem.lower().split("_", 1)[0]
        environment = prefix if prefix in ("phone", "studio") else None
        reports.append({
            "wav": path.name, "fs": audio.fs, "frames": len(predicted),
            "recording_environment": environment,
            "recording_environment_source": "filename_prefix" if environment else None,
            "duration_sec": audio.duration_sec, "threshold": model.value,
            "frame_length_samples": frames.frame_len, "frame_shift_samples": frames.frame_shift,
            "timestamps_sec": frames.timestamps.tolist(), "feature_values": features.values.tolist(),
            "raw_predicted_frame_labels": predicted.tolist(), "predicted_frame_labels": filtered.tolist(),
            "ground_truth_frame_labels": truth.tolist(),
            "ground_truth_intervals": [
                {"start": s.start, "end": s.end, "original_label": s.original_label, "label": s.label}
                for s in truth_segments
            ],
            "predicted_segments": segments, "predicted_boundaries": metrics.predicted_boundaries,
            "ground_truth_boundaries": metrics.gt_boundaries,
            "boundary_evaluation": {
                "predicted_count": len(metrics.predicted_boundaries), "gt_count": len(metrics.gt_boundaries),
                "matched_count": metrics.matched_count, "matched_pairs_sec": metrics.matched_pairs,
                "signed_errors_ms": metrics.errors_ms, "absolute_errors_ms": [abs(e) for e in metrics.errors_ms],
                "mae_ms": metrics.mae_ms if metrics.matched_count else None,
                "rmse_ms": metrics.rmse_ms if metrics.matched_count else None,
                "unmatched_predicted_boundaries": metrics.unmatched_predicted_boundaries,
                "unmatched_gt_boundaries": metrics.unmatched_gt_boundaries,
                "tolerance_ms": metrics.matching_tolerance_ms,
            },
            "covered_frames": int(np.sum(known)),
            "frame_accuracy": float(np.mean(filtered[known] == truth[known])) if np.any(known) else None,
            "false_speech_frames": int(np.sum(known & (filtered == 1) & (truth == 0))),
            "missed_speech_frames": int(np.sum(known & (filtered == 0) & (truth == 1))),
            "mode_ground_truth": modes, "alignment_warnings": warnings,
        })
        if include_noise:
            reports[-1]["background_noise"] = _background_noise_report(audio)
    return {
        "dataset_directory": str(directory), "threshold": model.value,
        "feature": model.feature_type,
        "boundary_policy": "midpoints between frame centers; postprocessed labels",
        "min_silence_ms": config.min_silence_ms,
        "matching_policy": "closest-first, one-to-one, noncrossing, same transition type, within reported tolerance",
        "mode_assignment_policy": "nearest selected peak via midpoint split; diagnostic groups, not guaranteed classes",
        "label_convention": {"silence": 0, "speech": 1, "uncovered": -1}, "files": reports,
    }
