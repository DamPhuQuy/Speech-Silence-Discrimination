# -*- coding: utf-8 -*-
"""
src/features/framing.py
Cac ham dung chung de chia tin hieu thanh cac frame (khung) ngan han,
dung cho ca tinh nang luong (energy.py) va tinh F0 (pitch).
"""

import numpy as np


def frame_params(sr, frame_ms, hop_ms):
    """
    Tinh do dai frame va buoc nhay (hop) theo don vi SO MAU, tu don vi ms.
    Tham so:
        sr (int): tan so lay mau (Hz)
        frame_ms (float): do dai 1 frame (ms)
        hop_ms (float): buoc nhay giua 2 frame (ms)
    Tra ve:
        frame_len (int), hop_len (int): don vi so mau
    """
    frame_len = int(round(sr * frame_ms / 1000))
    hop_len = int(round(sr * hop_ms / 1000))
    return frame_len, hop_len


def frame_centers(signal_len, sr, frame_len, hop_len):
    """
    Tinh so luong frame va thoi diem TAM (giay) cua moi frame, dua tren
    do dai tin hieu, frame_len va hop_len (tat ca dong bo voi energy.py).
    Tham so:
        signal_len (int): tong so mau cua tin hieu
        sr (int): tan so lay mau (Hz)
        frame_len, hop_len (int): xem frame_params()
    Tra ve:
        n_frames (int), centers (np.ndarray): thoi diem tam frame (giay)
    """
    n_frames = max(1, 1 + (signal_len - frame_len) // hop_len)
    centers = np.zeros(n_frames)
    for i in range(n_frames):
        start = i * hop_len
        centers[i] = (start + frame_len / 2.0) / sr
    return n_frames, centers


def get_frame(signal, start_sample, frame_len):
    """
    Lay 1 frame tin hieu bat dau tu start_sample, dai frame_len mau.
    Neu khong du mau (cham cuoi tin hieu), dem (pad) them so 0.
    Tham so:
        signal (np.ndarray): tin hieu goc
        start_sample (int): vi tri mau bat dau frame
        frame_len (int): do dai frame (so mau)
    Tra ve:
        np.ndarray, dai dung frame_len mau
    """
    frame = signal[max(0, start_sample):max(0, start_sample) + frame_len]
    if len(frame) < frame_len:
        frame = np.pad(frame, (0, frame_len - len(frame)))
    return frame
