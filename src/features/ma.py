"""MA feature using sum of magnitudes, rather than their mean."""
import numpy as np


def compute_ma(frames: np.ndarray) -> np.ndarray:
    """Return sum(abs(x[n])) per row of a finite (n_frames, frame_len) array."""
    frames = np.asarray(frames, dtype=np.float64)
    if frames.ndim != 2 or not np.all(np.isfinite(frames)):
        raise ValueError("Frames must be a finite two-dimensional array.")
    return np.sum(np.abs(frames), axis=1)
