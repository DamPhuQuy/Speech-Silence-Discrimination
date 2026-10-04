# -*- coding: utf-8 -*-
"""
src/evaluate/metrics.py
Danh gia dinh luong do chinh xac phan doan: RMSE va MAE (ms) giua bien
du doan va bien groundtruth; va uoc luong SNR (dB) cua file tin hieu.
"""

import numpy as np

EPS = 1e-10


def boundary_error_ms(pred_boundaries_s, gt_boundaries_s):
    """
    Voi moi bien groundtruth, tim bien du doan GAN NHAT (tinh theo ms)
    roi tinh RMSE va MAE tren toan bo cac cap bien da ghep.
    Tham so:
        pred_boundaries_s (list[float]): bien (giay) do thuat toan tim ra
        gt_boundaries_s (list[float]): bien (giay) groundtruth (*.lab)
    Tra ve:
        rmse (float|None), mae (float|None) don vi ms; errors_ms (list)
        None, None, [] neu thieu du lieu de so sanh
    """
    if len(pred_boundaries_s) == 0 or len(gt_boundaries_s) == 0:
        return None, None, []
    pred = np.array(pred_boundaries_s)
    errors_ms = []
    for gt in gt_boundaries_s:
        nearest = pred[np.argmin(np.abs(pred - gt))]
        errors_ms.append((nearest - gt) * 1000.0)
    errors_ms = np.array(errors_ms)
    rmse = float(np.sqrt(np.mean(errors_ms ** 2)))
    mae = float(np.mean(np.abs(errors_ms)))
    return rmse, mae, errors_ms.tolist()


def estimate_snr_db(signal, sr, sp_sil_segments):
    """
    Uoc luong SNR (dB) cua 1 file dua tren groundtruth: cong suat trung
    binh cac mau trong vung Speech so voi vung Silence (xem Silence la
    nen nhieu cua moi truong thu am).
    Tham so:
        signal (np.ndarray): tin hieu 1 kenh
        sr (int): tan so lay mau (Hz)
        sp_sil_segments (list[tuple]): [(start, end, 'speech'/'silence'), ...]
    Tra ve:
        float | None: SNR (dB), None neu thieu doan Speech hoac Silence
    """
    x = signal.astype(np.float64)
    speech_samples, silence_samples = [], []
    for s, e, cls in sp_sil_segments:
        i0, i1 = int(s * sr), int(e * sr)
        chunk = x[i0:i1]
        (speech_samples if cls == "speech" else silence_samples).append(chunk)
    if not speech_samples or not silence_samples:
        return None
    speech_power = np.mean(np.concatenate(speech_samples) ** 2)
    noise_power = np.mean(np.concatenate(silence_samples) ** 2) + EPS
    return 10 * np.log10(speech_power / noise_power)
