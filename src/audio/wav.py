"""Read uncompressed integer PCM WAVs without changing dataset files."""
from pathlib import Path
import wave
import numpy as np


def read_wav(path: Path) -> tuple[int, np.ndarray]:
    """Return actual Fs and float64 mono PCM samples scaled to [-1, 1).

    Supports 8/16/24/32-bit integer PCM. Channel averaging follows scaling;
    no per-recording peak normalization is applied, preserving silence.
    """
    with wave.open(str(path), "rb") as wav:
        fs = wav.getframerate()
        channels = wav.getnchannels()
        width = wav.getsampwidth()
        count = wav.getnframes()
        if wav.getcomptype() != "NONE":
            raise ValueError("Only uncompressed integer PCM WAV is supported.")
        data = wav.readframes(count)
    if len(data) != count * channels * width:
        raise ValueError("WAV sample data is truncated.")

    # Convert unsigned 8-bit or signed little-endian PCM before channel mixing.
    if width == 1:
        samples = (np.frombuffer(data, dtype=np.uint8).astype(np.float64) - 128) / 128
    elif width in (2, 4):
        samples = np.frombuffer(data, dtype=f"<i{width}").astype(np.float64)
        samples /= 2 ** (8 * width - 1)
    elif width == 3:
        octets = np.frombuffer(data, dtype=np.uint8).reshape(-1, 3).astype(np.int32)
        integers = octets[:, 0] | (octets[:, 1] << 8) | (octets[:, 2] << 16)
        integers = (integers ^ 0x800000) - 0x800000
        samples = integers.astype(np.float64) / 2 ** 23
    else:
        raise ValueError(f"Unsupported PCM sample width: {width} bytes.")
    return fs, samples.reshape(-1, channels).mean(axis=1)
