# -*- coding: utf-8 -*-
"""
src/features/energy.py
Dac trung nang luong: Short-Time Energy (STE) - cong thuc (2.1) trong
CS425 Audio and Speech Processing - Hodgkinson 2012, muc 2.1.2.
"""

import numpy as np

from .framing import frame_params, frame_centers, get_frame

EPS = 1e-10  # tranh log(0) hoac chia cho 0


def compute_log_ste(signal, sr, frame_ms=25, hop_ms=10):
    """
    Tinh dac trung log-STE (log Short-Time Energy) chuan hoa cho tung frame:
        STE[n] = sum_{m=0}^{N-1} x[n-m]^2            (cong thuc 2.1)
    Sau do chuan hoa STE theo gia tri max cua ca file (STE_norm in [0,1])
    roi lay log10 de nen bien do (giup tach biet 2 lop Speech/Silence
    ro hon, giong truc log(MA) trong Figure 2.3/2.5 cua Hodgkinson).

    Tham so:
        signal (np.ndarray): tin hieu 1 kenh
        sr (int): tan so lay mau (Hz)
        frame_ms, hop_ms (float): kich thuoc frame / buoc nhay (ms)
    Tra ve:
        log_ste (np.ndarray): dac trung log-STE, 1 gia tri / frame
        centers (np.ndarray): thoi diem tam moi frame (giay)
        frame_len, hop_len (int): kich thuoc frame theo so mau
    """
    frame_len, hop_len = frame_params(sr, frame_ms, hop_ms)
    n_frames, centers = frame_centers(len(signal), sr, frame_len, hop_len)

    ste = np.zeros(n_frames)
    x = signal.astype(np.float64)
    for i in range(n_frames):
        start = i * hop_len
        frame = get_frame(x, start, frame_len)
        ste[i] = np.sum(frame ** 2)  # cong thuc (2.1)

    ste_norm = ste / (np.max(ste) + EPS)
    log_ste = np.log10(ste_norm + EPS)
    return log_ste, centers, frame_len, hop_len
