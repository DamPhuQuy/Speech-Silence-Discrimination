"""Manual feature-only Histogram training and Speech/Silence prediction."""
import numpy as np
from src.models import FeatureType, Threshold

def build_histogram(feature_values, num_bins: int) -> tuple[np.ndarray, np.ndarray]:
    """Return integer counts and feature-valued centers for equal-width bins.

    Input must be a nonempty finite 1-D real numeric sequence and a positive
    integer bin count (booleans are rejected). Bins are left-inclusive and
    right-exclusive, except the final bin includes the maximum value.
    For constant input, place all counts in bin zero and repeat that value
    as every center; no artificial feature range is introduced.
    Raise ValueError for invalid input or an unrepresentable float64 range.
    """
    if isinstance(num_bins, (bool, np.bool_)) or not isinstance(num_bins, (int, np.integer)) or num_bins <= 0:
        raise ValueError("num_bins must be a positive integer.")
    values = np.asarray(feature_values)
    if values.ndim != 1 or values.size == 0 or values.dtype.kind not in "iuf":
        raise ValueError("feature_values must be a nonempty 1-D real numeric sequence.")
    values = values.astype(np.float64)
    if not np.all(np.isfinite(values)):
        raise ValueError("feature_values must contain only finite values.")

    xmin, xmax = float(np.min(values)), float(np.max(values))
    hist = np.zeros(num_bins, dtype=np.int64)
    if xmin == xmax:
        hist[0] = values.size
        return hist, np.full(num_bins, xmin, dtype=np.float64)
    bin_width = (xmax - xmin) / num_bins
    if not np.isfinite(bin_width) or bin_width <= 0:
        raise ValueError("Feature range cannot form finite positive float64 bins.")

    # Assign values manually; clamping also handles roundoff near the maximum.
    for x in values:
        index = num_bins - 1 if x == xmax else int(np.floor((float(x) - xmin) / bin_width))
        hist[min(max(index, 0), num_bins - 1)] += 1
    bin_centers = xmin + (np.arange(num_bins, dtype=np.float64) + 0.5) * bin_width
    return hist, bin_centers

def smooth_histogram(histogram, window_size: int) -> np.ndarray:
    """Return a new float64 moving average with the same length as histogram.

    window_size must be a positive odd integer. At bin i, average only bins
    from max(0, i-r) through min(n-1, i+r), where r = window_size // 2.
    No padding is used. Empty input returns an empty array; counts must be
    a finite, nonnegative, one-dimensional real numeric sequence.
    """
    if isinstance(window_size, (bool, np.bool_)) or not isinstance(window_size, (int, np.integer)) or window_size <= 0 or window_size % 2 == 0:
        raise ValueError("window_size must be a positive odd integer.")
    counts = np.asarray(histogram)
    if counts.ndim != 1 or counts.dtype.kind not in "iuf":
        raise ValueError("histogram must be a one-dimensional real numeric sequence.")
    counts = counts.astype(np.float64)
    if not np.all(np.isfinite(counts)) or np.any(counts < 0):
        raise ValueError("histogram counts must be finite and nonnegative.")

    # Truncate each window at the array edges and divide by its actual size.
    radius = int(window_size) // 2
    smoothed = np.empty(len(counts), dtype=np.float64)
    for i in range(len(counts)):
        start = max(0, i - radius)
        stop = min(len(counts), i + radius + 1)
        total = 0.0
        for j in range(start, stop):
            total += counts[j] / (stop - start)
        smoothed[i] = total
    return smoothed

def find_local_maxima(histogram) -> np.ndarray:
    """Return all strict interior peak indices in ascending order.

    A peak is greater than both immediate neighbors. Endpoints and flat
    plateaus are excluded. Inputs shorter than three bins, monotonic inputs
    and flat histograms return an empty integer array. Input must be a finite,
    nonnegative 1-D real numeric sequence and is never modified.
    """
    counts = np.asarray(histogram)
    if counts.ndim != 1 or counts.dtype.kind not in "iuf":
        raise ValueError("histogram must be a one-dimensional real numeric sequence.")
    if not np.all(np.isfinite(counts)) or np.any(counts < 0):
        raise ValueError("histogram counts must be finite and nonnegative.")

    # Compare original counts directly; equal neighbors do not form a peak.
    peaks = []
    for i in range(1, len(counts) - 1):
        if counts[i] > counts[i - 1] and counts[i] > counts[i + 1]:
            peaks.append(i)
    return np.asarray(peaks, dtype=np.int64)

def select_two_peaks(
    histogram, bin_centers, peak_indices, *,
    min_peak_distance: int = 2, min_relative_height: float = 0.1,
) -> tuple[float, float]:
    """Return ordered feature positions (M1, M2), never histogram heights.

    Reject peaks below min_relative_height times the strongest supplied peak.
    Among pairs at least min_peak_distance bins apart, maximize combined
    height; ties favor greater bin distance, then the lower index pair.
    Defaults exclude adjacent bins and peaks below 10% of the strongest.
    These are configurable heuristics, not proof of two speech/silence modes.
    Centers must be finite and strictly increasing; supplied indices must be
    unique strict interior maxima. Raise ValueError if no eligible pair exists.
    """
    if isinstance(min_peak_distance, (bool, np.bool_)) or not isinstance(min_peak_distance, (int, np.integer)) or min_peak_distance < 1:
        raise ValueError("min_peak_distance must be a positive integer in bins.")
    if isinstance(min_relative_height, (bool, np.bool_)) or not isinstance(min_relative_height, (int, float, np.integer, np.floating)) or not np.isfinite(min_relative_height) or not 0 <= min_relative_height <= 1:
        raise ValueError("min_relative_height must be a finite number in [0, 1].")
    counts, centers, peaks = map(np.asarray, (histogram, bin_centers, peak_indices))
    for name, values in (("histogram", counts), ("bin_centers", centers)):
        if values.ndim != 1 or values.dtype.kind not in "iuf" or not np.all(np.isfinite(values)):
            raise ValueError(f"{name} must be a finite 1-D real numeric sequence.")
    if counts.shape != centers.shape or np.any(counts < 0):
        raise ValueError("Counts must be nonnegative and match bin_centers length.")
    centers = centers.astype(np.float64)
    if not np.all(centers[1:] > centers[:-1]):
        raise ValueError("bin_centers must be strictly increasing.")
    if peaks.ndim != 1 or (peaks.size and peaks.dtype.kind not in "iu"):
        raise ValueError("peak_indices must be a 1-D integer sequence.")
    indices = sorted(int(p) for p in peaks)
    if len(set(indices)) != len(indices):
        raise ValueError("peak_indices must be unique.")
    for p in indices:
        if p <= 0 or p >= len(counts) - 1 or not (counts[p] > counts[p - 1] and counts[p] > counts[p + 1]):
            raise ValueError("peak_indices must refer to strict interior local maxima.")
    if len(indices) < 2:
        raise ValueError("At least two detected peaks are required.")

    # Project extension: robust peak selection.
    # This is not part of the basic histogram formula itself.
    strongest = float(max(counts[p] for p in indices))
    eligible = [p for p in indices if counts[p] / strongest >= min_relative_height]
    best_pair, best_score = None, None
    for i, left in enumerate(eligible):
        for right in eligible[i + 1:]:
            distance = right - left
            if distance < min_peak_distance:
                continue
            # Scaling avoids overflow while preserving the strength ranking.
            score = (float(counts[left] / strongest + counts[right] / strongest), distance)
            if best_score is None or score > best_score:
                best_pair, best_score = (left, right), score
    if best_pair is None:
        raise ValueError("No two peaks satisfy the relative-height and minimum-distance rules.")
    return float(centers[best_pair[0]]), float(centers[best_pair[1]])

def calculate_threshold(m1: float, m2: float, weight: float) -> float:
    """Return T = (weight*M1 + M2)/(weight + 1) for finite M1 < M2.

    Require finite weight > 0 and a representable result strictly between
    the feature-space peaks. Raise ValueError for invalid parameters or
    overflow/rounding that prevents a strictly interior threshold.
    """
    for name, value in (("m1", m1), ("m2", m2), ("weight", weight)):
        if isinstance(value, (bool, np.bool_)) or not isinstance(value, (int, float, np.integer, np.floating)):
            raise ValueError(f"{name} must be a finite real scalar.")
    try:
        m1, m2, weight = float(m1), float(m2), float(weight)
    except (OverflowError, ValueError) as exc:
        raise ValueError("Parameters must be representable finite real scalars.") from exc
    if not all(np.isfinite(value) for value in (m1, m2, weight)):
        raise ValueError("m1, m2 and weight must be finite.")
    if weight <= 0:
        raise ValueError("weight must be greater than zero.")
    if m1 >= m2:
        raise ValueError("Peak feature positions must satisfy m1 < m2.")
    threshold = (weight * m1 + m2) / (weight + 1)
    if not np.isfinite(threshold) or not m1 < threshold < m2:
        raise ValueError("Calculated threshold must be finite and satisfy m1 < T < m2.")
    return threshold

def train_histogram(
    feature_values: np.ndarray | list[float] | tuple[float, ...],
    num_bins: int, smooth_window: int, weight: float, *,
    feature_type: FeatureType = "ste",
    min_peak_distance: int = 2, min_relative_height: float = 0.1,
) -> Threshold:
    """Estimate a threshold by composing the existing Histogram functions.

    Receives only training feature values and caller-selected parameters;
    feature_type records their identity and does not transform them. No data
    loading, plotting or parameter tuning occurs here. Returns Threshold.value
    and debug arrays (histogram, smoothed_histogram, bin_centers, peak_indices)
    plus feature-space m1/m2. Use predict(feature_values, result.value).
    Invalid inputs or insufficient eligible modes propagate ValueError.
    """
    if feature_type not in ("ste", "ma", "logste", "logma"):
        raise ValueError("feature_type must be ste, ma, logste or logma.")
    hist, centers = build_histogram(feature_values, num_bins)
    smoothed = smooth_histogram(hist, smooth_window)
    peaks = find_local_maxima(smoothed)
    m1, m2 = select_two_peaks(
        smoothed, centers, peaks,
        min_peak_distance=min_peak_distance,
        min_relative_height=min_relative_height,
    )
    threshold = calculate_threshold(m1, m2, weight)
    return Threshold(
        algorithm="histogram", feature_type=feature_type, value=threshold,
        debug={
            "histogram": hist, "smoothed_histogram": smoothed,
            "bin_centers": centers, "peak_indices": peaks, "m1": m1, "m2": m2,
        },
    )

def predict(feature_values, threshold: float) -> np.ndarray:
    """Return one integer label per finite 1-D feature value: 0=silence, 1=speech.

    Only values strictly greater than the finite scalar threshold are speech;
    equality is silence. Empty input returns an empty integer array.
    """
    if isinstance(threshold, (bool, np.bool_)) or not isinstance(threshold, (int, float, np.integer, np.floating)):
        raise ValueError("threshold must be a finite real scalar.")
    try:
        threshold = float(threshold)
    except (OverflowError, ValueError) as exc:
        raise ValueError("threshold must be a representable finite real scalar.") from exc
    if not np.isfinite(threshold):
        raise ValueError("threshold must be finite.")
    values = np.asarray(feature_values)
    if values.ndim != 1 or values.dtype.kind not in "iuf" or not np.all(np.isfinite(values)):
        raise ValueError("feature_values must be a finite 1-D real numeric sequence.")
    return (values > threshold).astype(np.int64)
