"""Sampling-rate-aware framing with complete frames and no windowing."""
import numpy as np
from src.models import AudioSignal, FrameSignal


def ms_to_samples(duration_ms: float, fs: int) -> int:
    """Return round(duration_ms * Fs / 1000), using Python ties-to-even.

    Reject nonpositive/nonfinite durations, invalid Fs and sub-sample results.
    """
    if not np.isfinite(duration_ms) or duration_ms <= 0:
        raise ValueError("Duration must be finite and positive.")
    if not isinstance(fs, (int, np.integer)) or fs <= 0:
        raise ValueError("Fs must be a positive integer.")
    samples = round(duration_ms * fs / 1000)
    if samples < 1:
        raise ValueError("Duration rounds to fewer than one sample.")
    return samples


def frame_signal(signal: AudioSignal, frame_duration_ms: float, frame_shift_ms: float) -> FrameSignal:
    """Return float64 frames and center times from mono AudioSignal.

    Drop incomplete trailing frames; a short/empty signal yields (0, frame_len).
    Frames are unwindowed and unpadded; raw_frames retains the same samples.
    """
    frame_len = ms_to_samples(frame_duration_ms, signal.fs)
    shift = ms_to_samples(frame_shift_ms, signal.fs)
    samples = np.asarray(signal.signal, dtype=np.float64)
    if samples.ndim != 1 or not np.all(np.isfinite(samples)):
        raise ValueError("Signal must be a finite one-dimensional mono array.")
    n_frames = max(0, 1 + (len(samples) - frame_len) // shift)
    frames = np.empty((n_frames, frame_len), dtype=np.float64)
    for i in range(n_frames):
        start = i * shift
        frames[i] = samples[start:start + frame_len]
    return FrameSignal(
        frames=frames, raw_frames=frames.copy(),
        timestamps=frame_centers(n_frames, frame_len, shift, signal.fs),
        frame_len=frame_len, frame_shift=shift, fs=signal.fs,
    )


def frame_centers(n_frames: int, frame_len: int, frame_shift: int, fs: int) -> np.ndarray:
    """Return seconds at each frame interval midpoint: (i*shift + len/2)/Fs."""
    if any(not isinstance(v, (int, np.integer)) for v in (n_frames, frame_len, frame_shift, fs)):
        raise ValueError("Frame counts, lengths, shift and Fs must be integers.")
    if n_frames < 0 or min(frame_len, frame_shift, fs) <= 0:
        raise ValueError("Count must be nonnegative; length, shift and Fs positive.")
    return (np.arange(n_frames, dtype=np.float64) * frame_shift + frame_len / 2) / fs
