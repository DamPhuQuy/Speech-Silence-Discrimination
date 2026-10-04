"""One-to-one speech/silence boundary matching; errors use milliseconds."""
import numpy as np
from src.models import BinaryLabel, EvaluationMetrics, SegmentationResult, AudioSignal
from src.segmentation.postprocess import decisions_to_segments, segment_boundaries
from src.audio.labels import speech_silence_boundaries

DEFAULT_BOUNDARY_TOLERANCE_MS = 100.0


def _boundary_times(values: list[float], name: str) -> list[float]:
    """Validate finite, nonnegative, strictly increasing second-valued times."""
    array = np.asarray(values)
    if array.ndim != 1 or array.dtype.kind not in "iuf":
        raise ValueError(f"{name} must be a 1-D real numeric sequence.")
    array = array.astype(np.float64)
    if not np.all(np.isfinite(array)) or np.any(array < 0) or np.any(array[1:] <= array[:-1]):
        raise ValueError(f"{name} must be finite, nonnegative and strictly increasing.")
    return array.tolist()


def match_boundaries(
    predicted: list[float], ground_truth: list[float], tolerance_ms: float | None = None, *,
    predicted_types: list[BinaryLabel] | None = None,
    ground_truth_types: list[BinaryLabel] | None = None,
) -> tuple[list[tuple[float, float]], list[float], list[float]]:
    """Return (predicted, GT) time pairs and unmatched times, all in seconds.

    Greedily accept the closest candidate pair first, within tolerance (inclusive;
    None means the explicit 100 ms baseline, never unlimited matching). Each
    boundary is used once and accepted pairs cannot cross in chronological order.
    Ties favor earlier predicted then earlier GT indices. This simple greedy
    strategy does not claim to maximize the number of matches. Optional types
    denote the state AFTER a boundary; when supplied, only equal types match.
    Report unmatched counts alongside errors to avoid hiding missed/extra events.
    """
    pred = _boundary_times(predicted, "predicted")
    truth = _boundary_times(ground_truth, "ground_truth")
    limit = DEFAULT_BOUNDARY_TOLERANCE_MS if tolerance_ms is None else tolerance_ms
    if isinstance(limit, (bool, np.bool_)) or not isinstance(limit, (int, float, np.integer, np.floating)):
        raise ValueError("tolerance_ms must be finite and nonnegative.")
    try:
        limit = float(limit)
    except (OverflowError, ValueError) as exc:
        raise ValueError("tolerance_ms must be finite and nonnegative.") from exc
    if not np.isfinite(limit) or limit < 0:
        raise ValueError("tolerance_ms must be finite and nonnegative.")
    if (predicted_types is None) != (ground_truth_types is None):
        raise ValueError("Supply both boundary-type sequences or neither.")
    if predicted_types is not None:
        for types, times in ((predicted_types, pred), (ground_truth_types, truth)):
            if len(types) != len(times) or any(state not in ("speech", "silence") for state in types):
                raise ValueError("Boundary types must match time lengths and use speech/silence.")

    # Candidate errors are converted from seconds; closest valid pairs win.
    candidates = []
    for i, time in enumerate(pred):
        for j, gt in enumerate(truth):
            if predicted_types is not None and predicted_types[i] != ground_truth_types[j]:
                continue
            error_ms = abs(time - gt) * 1000
            if error_ms <= limit or (limit > 0 and np.isclose(error_ms, limit, rtol=0, atol=1e-9)):
                candidates.append((error_ms, i, j))
    accepted = []
    used_pred, used_gt = set(), set()
    for _, i, j in sorted(candidates):
        if i in used_pred or j in used_gt:
            continue
        if any((i - old_i) * (j - old_j) < 0 for old_i, old_j in accepted):
            continue
        accepted.append((i, j))
        used_pred.add(i)
        used_gt.add(j)
    pairs = [(pred[i], truth[j]) for i, j in sorted(accepted)]
    return pairs, [time for i, time in enumerate(pred) if i not in used_pred], [time for j, time in enumerate(truth) if j not in used_gt]


def _errors_ms(matched_pairs: list[tuple[float, float]]) -> np.ndarray:
    """Validate pairs and return signed prediction-minus-GT errors in ms."""
    if len(matched_pairs) == 0:
        return np.empty(0, dtype=np.float64)
    pairs = np.asarray(matched_pairs)
    if pairs.ndim != 2 or pairs.shape[1] != 2 or pairs.dtype.kind not in "iuf":
        raise ValueError("Matched pairs must contain (predicted_seconds, GT_seconds).")
    pairs = pairs.astype(np.float64)
    if not np.all(np.isfinite(pairs)) or np.any(pairs < 0):
        raise ValueError("Matched times must be finite and nonnegative.")
    with np.errstate(over="raise", invalid="raise"):
        try:
            return (pairs[:, 0] - pairs[:, 1]) * 1000
        except FloatingPointError as exc:
            raise ValueError("Boundary errors exceed finite millisecond range.") from exc


def boundary_mae_ms(matched_pairs: list[tuple[float, float]]) -> float:
    """Return mean(abs(predicted-GT)*1000); no matched pairs yields NaN."""
    errors = _errors_ms(matched_pairs)
    return float(np.mean(np.abs(errors))) if errors.size else float("nan")


def boundary_rmse_ms(matched_pairs: list[tuple[float, float]]) -> float:
    """Return sqrt(mean(((predicted-GT)*1000)**2)); no matches yields NaN."""
    errors = _errors_ms(matched_pairs)
    if not errors.size:
        return float("nan")
    scale = float(np.max(np.abs(errors)))
    return scale * float(np.sqrt(np.mean((errors / scale) ** 2))) if scale else 0.0


def evaluate_result(signal: AudioSignal, result: SegmentationResult, tolerance_ms: float | None = None) -> EvaluationMetrics:
    """Score postprocessed transition times; onset/offset types must correspond.

    Re-extract boundaries from filtered labels and frame centers; reject stale
    stored boundaries. GT v/uv transitions are excluded by the LAB helper.
    When GT intervals are available, constrain matching by transition type.
    NaN errors mean no matches; callers exporting JSON should encode them null.
    """
    if signal.name != result.signal_name:
        raise ValueError("Signal and segmentation result names must match.")
    segments = decisions_to_segments(result.filtered_decisions, result.timestamps, signal.duration_sec)
    predicted = segment_boundaries(segments)
    if predicted != list(result.predicted_boundaries):
        raise ValueError("Predicted boundaries must come from postprocessed frame labels.")
    options = {}
    if signal.gt_segments:
        gt = speech_silence_boundaries(signal.gt_segments)
        if gt != list(signal.gt_boundaries):
            raise ValueError("Ground-truth boundaries must reflect speech/silence LAB transitions.")
        pred_types = [current[2] for previous, current in zip(segments, segments[1:])
                      if abs(previous[1] - current[0]) <= 1e-9 and previous[2] != current[2]]
        gt_types = [current.label for previous, current in zip(signal.gt_segments, signal.gt_segments[1:])
                    if abs(previous.end - current.start) <= 1e-9 and previous.label != current.label]
        options = {"predicted_types": pred_types, "ground_truth_types": gt_types}
    pairs, extras, misses = match_boundaries(predicted, signal.gt_boundaries, tolerance_ms, **options)
    return EvaluationMetrics(
        signal_name=signal.name,
        environment="phone" if signal.is_phone else
        "studio" if signal.wav_path.stem.lower().startswith("studio_") else "unknown",
        algorithm=result.algorithm, threshold=result.threshold_used,
        mae_ms=boundary_mae_ms(pairs), rmse_ms=boundary_rmse_ms(pairs),
        predicted_boundaries=predicted, gt_boundaries=list(signal.gt_boundaries),
        matched_count=len(pairs), unmatched_predictions=len(extras), unmatched_ground_truth=len(misses),
        matched_pairs=pairs, errors_ms=_errors_ms(pairs).tolist(),
        unmatched_predicted_boundaries=extras, unmatched_gt_boundaries=misses,
        matching_tolerance_ms=DEFAULT_BOUNDARY_TOLERANCE_MS if tolerance_ms is None else float(tolerance_ms),
    )
