# -*- coding: utf-8 -*-
"""
src/audio/io.py
Doc du lieu am thanh (*.wav). Chi dung ham doc file (I/O), KHONG xu ly
tin hieu o day - viec xu ly (framing, STE, F0...) nam o src/features/.
"""

import soundfile as sf


def read_wav(path):
    """
    Doc 1 file .wav va tra ve tin hieu mono + tan so lay mau.
    Tham so:
        path (str): duong dan file .wav
    Tra ve:
        signal (np.ndarray, float): tin hieu 1 kenh (mono)
        sr (int): tan so lay mau (Hz)
    """
    # sf.read() la ham built-in cua thu vien doc file, khong phai ham
    # xu ly tin hieu -> duoc phep su dung theo quy dinh cua bai tap.
    signal, sr = sf.read(path)
    if signal.ndim > 1:
        # Neu file stereo, gop cac kenh thanh 1 kenh mono bang trung binh.
        signal = signal.mean(axis=1)
    return signal, sr
