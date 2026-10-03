"""Logarithmic transforms of the existing STE/MA feature values."""
import numpy as np

def log_transform(values: np.ndarray, epsilon: float = 1e-12) -> np.ndarray:
    """Return natural log(values + epsilon) for finite nonnegative features."""
    values = np.asarray(values, dtype=np.float64)
    if not np.isfinite(epsilon) or epsilon <= 0:
        raise ValueError("Epsilon must be finite and positive.")
    if not np.all(np.isfinite(values)) or np.any(values < 0):
        raise ValueError("Log input must be finite and nonnegative.")
    with np.errstate(over="raise", invalid="raise"):
        result = np.log(values + epsilon)
    if not np.all(np.isfinite(result)):
        raise ValueError("Log transform must produce finite values.")
    return result
