"""Short-Time Energy using the project's sum definition."""
import numpy as np


def compute_ste(frames: np.ndarray) -> np.ndarray:
    """Return sum(x[n]**2) per row of a finite (n_frames, frame_len) array."""
    frames = np.asarray(frames, dtype=np.float64)
    if frames.ndim != 2 or not np.all(np.isfinite(frames)):
        raise ValueError("Frames must be a finite two-dimensional array.")
    return np.sum(frames ** 2, axis=1)
