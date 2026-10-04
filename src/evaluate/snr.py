"""LAB-based noise analysis, independent of Histogram training and prediction.

The repository does not fix an operational SNR definition. The explicitly
selected speech_to_silence_power convention reports observed power contrast,
not clean-speech SNR: speech intervals contain speech plus recording noise.
"""
from typing import Literal
import numpy as np
from src.models import AudioSignal
from src.audio.labels import labels_at_timestamps, to_binary_label

POWER_CONTRAST_NAME = "Speech/Silence Power Contrast (dB)"
POWER_CONTRAST_DEFINITION = (
    "10*log10(P_observed_speech/P_silence); LAB-based sample-weighted mean-square powers; "
    "observed speech includes background noise; not clean-speech SNR"
)

def estimate_snr_db(
    signal: AudioSignal, *, definition: Literal["speech_to_silence_power"] | None = None,
) -> float:
    """Return Speech/Silence Power Contrast (dB), using a legacy API name.

    definition='speech_to_silence_power' means 10*log10(P_observed_speech /
    P_silence), using sample-weighted mean-square powers over LAB intervals.
    No noise subtraction, DC removal or clean-speech assumption is made.
    Omitted/unknown definition or missing classes raises ValueError. Zero noise
    with positive speech yields +inf; zero speech with positive noise yields
    -inf; both zero is undefined and raises ValueError. No epsilon hides zeros.
    The function name is retained for compatibility; this is not clean SNR.
    """
    if definition != "speech_to_silence_power":
        raise ValueError("No SNR convention is fixed by this project; explicitly select definition='speech_to_silence_power' for observed power contrast.")
    analysis = analyze_background_noise(signal)
    speech, noise = analysis["observed_speech_power"], analysis["silence_noise_power"]
    if speech is None or noise is None:
        raise ValueError("Both LAB speech and silence must contain sampled audio for a power ratio.")
    if speech == 0 and noise == 0:
        raise ValueError("Speech/silence power ratio is undefined when both powers are zero.")
    if noise == 0:
        return float("inf")
    if speech == 0:
        return float("-inf")
    return float(10 * (np.log10(speech) - np.log10(noise)))

def estimate_noise_power(samples: np.ndarray) -> float:
    """Return mean(x[n]**2) over supplied finite 1-D silence samples.

    PCM-scaled input gives squared normalized-amplitude units, not watts.
    Include DC; do not reinterpret power as variance. Reject empty/nonfinite
    input or float64 power overflow; integer samples convert before squaring.
    """
    values = np.asarray(samples)
    if values.ndim != 1 or not values.size or values.dtype.kind not in "iuf":
        raise ValueError("Power requires a nonempty one-dimensional real numeric array.")
    values = values.astype(np.float64)
    if not np.all(np.isfinite(values)):
        raise ValueError("Power samples must be finite.")
    with np.errstate(over="raise", invalid="raise"):
        try:
            power = float(np.mean(values ** 2))
        except FloatingPointError as exc:
            raise ValueError("Mean-square power exceeds finite float64 range.") from exc
    return power


def analyze_background_noise(signal: AudioSignal) -> dict[str, float | int | None | str]:
    """Report LAB-class sample counts and mean-square powers for noise analysis.

    Align sample n at n/Fs seconds using the shared half-open LAB mapper.
    Pool all sil samples for noise; v and uv are observed speech. Uncovered
    samples are counted and excluded, including gaps and rounded LAB tails.
    Missing classes have None power, never a fabricated zero. No file loading,
    label inference, Histogram calls or per-recording normalization occurs here.
    """
    samples = np.asarray(signal.signal)
    if samples.ndim != 1 or not samples.size or samples.dtype.kind not in "iuf" or not np.all(np.isfinite(samples)):
        raise ValueError("Audio must be a nonempty finite one-dimensional real array.")
    if isinstance(signal.fs, (bool, np.bool_)) or not isinstance(signal.fs, (int, np.integer)) or signal.fs <= 0:
        raise ValueError("Audio Fs must be a positive integer.")
    if not signal.gt_segments:
        raise ValueError("LAB ground-truth intervals are required for noise analysis.")
    for segment in signal.gt_segments:
        if segment.label != to_binary_label(segment.original_label):
            raise ValueError("Ground-truth labels must map sil to silence and v/uv to speech.")
    labels = labels_at_timestamps(signal.gt_segments, np.arange(len(samples), dtype=np.float64) / signal.fs)
    silence, speech = samples[labels == 0], samples[labels == 1]
    return {
        "power_definition": "sample-weighted mean(x[n]**2); squared normalized-amplitude units for PCM-scaled audio; DC included",
        "silence_noise_power": estimate_noise_power(silence) if silence.size else None,
        "observed_speech_power": estimate_noise_power(speech) if speech.size else None,
        "silence_samples": int(silence.size), "speech_samples": int(speech.size),
        "uncovered_samples": int(np.sum(labels == -1)), "total_samples": len(samples),
    }

def report_snr(
    signals: list[AudioSignal], *, definition: Literal["speech_to_silence_power"] | None = None,
) -> dict[str, float]:
    """Return per-name dB contrasts for an explicitly selected convention.

    Works on already loaded train/test recordings later, without reading data
    or routing/tuning thresholds. Reject duplicate names instead of overwriting.
    Per-recording failures propagate; callers can use analyze_background_noise
    when one LAB class is absent. Infinite results are intentional zero-power cases.
    """
    if definition != "speech_to_silence_power":
        raise ValueError("Explicitly select definition='speech_to_silence_power' for observed power contrast.")
    if len({signal.name for signal in signals}) != len(signals):
        raise ValueError("Recording names must be unique for noise reporting.")
    return {signal.name: estimate_snr_db(signal, definition=definition) for signal in signals}
