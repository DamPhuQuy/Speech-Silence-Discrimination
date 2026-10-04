# -*- coding: utf-8 -*-
"""
src/features/pitch.py
Uoc luong F0 (pitch) theo tung frame bang phuong phap tu tuong quan
(autocorrelation). Chi dung ham built-in numpy (correlate, argmax, mean).
"""

import numpy as np

from .framing import get_frame

EPS = 1e-10


def estimate_f0_track(signal, sr, centers_s, frame_len,
                       f0_min=60, f0_max=400, voicing_thresh=0.35):
    """
    Voi moi frame (tam tai centers_s), uoc luong F0 (Hz) bang tu tuong quan:
      1) Lay 1 frame tin hieu quanh tam, tru trung binh (loai thanh phan DC).
      2) Tinh tu tuong quan r[k] = sum_n x[n]*x[n-k] (np.correlate).
      3) Tim dinh lon nhat cua r trong khoang lag ung voi [f0_min, f0_max].
      4) "Do tin cay giong" (voicing confidence) = r[peak] / r[0].
         Neu confidence < voicing_thresh -> frame khong co pitch ro rang
         (vd unvoiced/silence) -> gan F0 = NaN (khong ve len do thi).

    Tham so:
        signal (np.ndarray): tin hieu 1 kenh
        sr (int): tan so lay mau (Hz)
        centers_s (np.ndarray): thoi diem tam cac frame (giay), tu energy.py
        frame_len (int): do dai frame (so mau), dong bo voi energy.py
        f0_min, f0_max (float): khoang tan so F0 hop ly (Hz)
        voicing_thresh (float): nguong do tin cay de coi la co pitch
    Tra ve:
        f0_hz (np.ndarray): F0 (Hz), NaN tai frame khong xac dinh duoc pitch
    """
    f0_hz = np.full(len(centers_s), np.nan)
    min_lag = int(sr / f0_max)
    max_lag = int(sr / f0_min)
    x = signal.astype(np.float64)

    for i, t in enumerate(centers_s):
        start = int(round(t * sr - frame_len / 2))
        frame = get_frame(x, start, frame_len)
        frame = frame - np.mean(frame)
        if np.max(np.abs(frame)) < 1e-6:
            continue

        corr = np.correlate(frame, frame, mode="full")
        corr = corr[len(corr) // 2:]  # chi giu lag >= 0
        max_lag_local = min(max_lag, len(corr) - 1)
        if max_lag_local <= min_lag:
            continue

        search_zone = corr[min_lag:max_lag_local]
        peak_idx = np.argmax(search_zone) + min_lag
        confidence = corr[peak_idx] / (corr[0] + EPS)
        if confidence >= voicing_thresh and peak_idx > 0:
            f0_hz[i] = sr / peak_idx

    return f0_hz
