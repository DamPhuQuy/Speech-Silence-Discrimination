"""Shared settings and the training-only frozen Histogram configuration."""
from dataclasses import asdict, dataclass
import hashlib
import json
import math
from pathlib import Path
from typing import Any

import numpy as np
from src.models import FeatureType, Threshold

@dataclass
class Config:
    """Initial defaults to be reviewed using training data only."""
    frame_duration_ms: float = 25.0
    frame_shift_ms: float = 10.0
    min_silence_ms: float = 200.0
    feature_type: FeatureType = "ste"
    epsilon: float = 1e-12
    # Final demonstrations load these choices from the training lock.
    histogram_bins: int | None = None
    histogram_smoothing_window: int | None = None


def load_frozen_histogram(path: Path) -> tuple[Config, Threshold, dict[str, Any]]:
    """Load Config, the frozen Threshold and its saved training information.

    Only read the existing lock: never load WAV/LAB, fit a Histogram, or
    recalculate T*. Validate the saved choices and retain a configuration
    snapshot and file hash for the evaluation pipeline's freeze checks.
    Missing files or invalid locks fail explicitly; there is no refit fallback.
    """
    path = Path(path).resolve()
    before = path.read_bytes()
    saved = json.loads(before)
    if not isinstance(saved, dict):
        raise ValueError("Frozen Histogram configuration must be a JSON object.")
    if saved.get("locked") is not True or saved.get("algorithm") != "histogram":
        raise ValueError("Expected a locked Histogram configuration.")
    if saved.get("selection_scope") != "training_only":
        raise ValueError("Final model must have been selected from training data only.")
    try:
        params = saved["parameters"]
        if not isinstance(params, dict):
            raise ValueError("Saved parameters must be a JSON object.")
        if not isinstance(saved["histogram_debug"], dict):
            raise ValueError("Saved histogram_debug must be a JSON object.")
        if saved["feature"] not in ("ste", "ma", "logste", "logma"):
            raise ValueError("Unsupported frozen feature type.")
        for name in ("num_bins", "smooth_window"):
            value = params[name]
            if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
                raise ValueError(f"Saved {name} must be a positive integer.")
        if params["smooth_window"] % 2 == 0:
            raise ValueError("Saved smooth_window must be odd.")
        for name in ("weight", "frame_duration_ms", "frame_shift_ms", "min_silence_ms", "epsilon"):
            value = params[name]
            if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or value <= 0:
                raise ValueError(f"Saved {name} must be finite and positive.")
        for name in ("m1", "m2", "threshold", "evaluation_tolerance_ms"):
            value = saved[name]
            if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
                raise ValueError(f"Saved {name} must be finite and numeric.")
        if not saved["m1"] < saved["threshold"] < saved["m2"]:
            raise ValueError("Saved threshold must be finite and strictly between its selected peaks.")
        if saved["evaluation_tolerance_ms"] < 0:
            raise ValueError("Saved evaluation tolerance must be nonnegative.")
        config = Config(
            feature_type=saved["feature"], frame_duration_ms=params["frame_duration_ms"],
            frame_shift_ms=params["frame_shift_ms"], min_silence_ms=params["min_silence_ms"],
            epsilon=params["epsilon"], histogram_bins=params["num_bins"],
            histogram_smoothing_window=params["smooth_window"],
        )
        debug = {name: np.asarray(value) if isinstance(value, list) else value
                 for name, value in saved["histogram_debug"].items()}
    except KeyError as exc:
        raise ValueError(f"Frozen Histogram configuration is missing {exc.args[0]}.") from exc
    model = Threshold("histogram", config.feature_type, float(saved["threshold"]), debug)
    information = {**saved, "lock_file": str(path), "lock_sha256": hashlib.sha256(before).hexdigest(),
                   "config_snapshot": asdict(config)}
    return config, model, information


def load_locked_histogram(path: Path) -> tuple[Config, Threshold]:
    """Compatibility API returning the saved configuration and threshold only."""
    config, model, _ = load_frozen_histogram(path)
    return config, model
