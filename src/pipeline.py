# -*- coding: utf-8 -*-
"""
src/pipeline.py
Dieu phoi toan bo quy trinh:
    TRAINING (tim nguong T tren data/TinHieuHuanLuyen)
    -> TESTING (ap dung T len data/TinHieuKiemThu, ve 4 figure)
    -> xuat ket qua (JSON) de lam slide bao cao.
Day la module "driver" duy nhat goi den cac package con (audio, features,
segmentation, evaluate); main.py o thu muc goc chi goi ham run() o day.
"""

import glob
import json
import os

import numpy as np
import matplotlib.pyplot as plt

from .audio.io import read_wav
from .audio.labels import parse_lab, to_speech_silence, boundaries_from_segments
from .features.energy import compute_log_ste, EPS
from .features.pitch import estimate_f0_track
from .segmentation.threshold import label_frames, find_threshold_binary_search
from .segmentation.segmenter import classify_frames, frames_to_segments, remove_short_silences
from .evaluate.metrics import boundary_error_ms, estimate_snr_db
from .models import ThresholdResult, FileTestResult

FRAME_MS = 25
HOP_MS = 10
MIN_SIL_MS = 200


# --------------------------------------------------------------------- #
# GIAI DOAN 1: TRAINING - gom du lieu log-STE va tim nguong T
# --------------------------------------------------------------------- #
def train_threshold(train_dir, verbose=True):
    """
    Doc toan bo file training (.wav + .lab), tinh log-STE, gom cac frame
    Speech/Silence theo groundtruth, roi chay Binary Search de tim nguong T.
    Tham so:
        train_dir (str): thu muc chua cac file training
        verbose (bool): co in log qua trinh hay khong
    Tra ve:
        ThresholdResult: nguong T + cac thong tin training lien quan
    """
    train_wavs = sorted(glob.glob(os.path.join(train_dir, "*.wav")))
    all_speech_vals, all_silence_vals = [], []
    train_snr = {}

    for wav_path in train_wavs:
        name = os.path.splitext(os.path.basename(wav_path))[0]
        lab_path = os.path.join(train_dir, name + ".lab")

        signal, sr = read_wav(wav_path)
        raw_segs, f0mean, f0std = parse_lab(lab_path)
        sp_sil_segs = to_speech_silence(raw_segs)

        log_ste, centers, frame_len, hop_len = compute_log_ste(signal, sr, FRAME_MS, HOP_MS)
        labels = label_frames(centers, sp_sil_segs)

        all_speech_vals.append(log_ste[labels == "speech"])
        all_silence_vals.append(log_ste[labels == "silence"])

        snr = estimate_snr_db(signal, sr, sp_sil_segs)
        train_snr[name] = snr
        if verbose:
            print(f"  {name:12s} | sr={sr:6d}Hz | frames={len(log_ste):4d} | "
                  f"SNR~{snr:5.1f} dB | F0mean={f0mean}")

    speech_vals = np.concatenate(all_speech_vals)
    silence_vals = np.concatenate(all_silence_vals)
    if verbose:
        print(f"\n  Tong so frame SPEECH (training) : {len(speech_vals)}")
        print(f"  Tong so frame SILENCE (training): {len(silence_vals)}")

    T, lower_name = find_threshold_binary_search(silence_vals, speech_vals, verbose=verbose)
    if verbose:
        print(f"\n  >>> NGUONG TOI UU (Binary Search) T = {T:.4f} "
              f"(trang thai thap hon = '{lower_name}')")

    return ThresholdResult(T=T, lower_name=lower_name, frame_ms=FRAME_MS,
                            hop_ms=HOP_MS, min_silence_ms=MIN_SIL_MS,
                            train_snr_db=train_snr)


# --------------------------------------------------------------------- #
# GIAI DOAN 2: TESTING - ap dung T cho 1 file, tra ve ket qua + du lieu ve hinh
# --------------------------------------------------------------------- #
def test_one_file(wav_path, test_dir, thr: ThresholdResult):
    """
    Ap dung nguong T (cua doi tuong ThresholdResult) cho 1 file test:
    phan loai frame, hau xu ly, so sanh voi groundtruth, uoc luong F0.
    Tham so:
        wav_path (str): duong dan file .wav can kiem thu
        test_dir (str): thu muc chua file .lab tuong ung
        thr (ThresholdResult): nguong T tu buoc training
    Tra ve:
        FileTestResult, va cac mang du lieu trung gian de ve hinh:
        (result, signal, sr, log_ste, centers, f0_track)
    """
    name = os.path.splitext(os.path.basename(wav_path))[0]
    lab_path = os.path.join(test_dir, name + ".lab")

    signal, sr = read_wav(wav_path)
    raw_segs, f0mean, f0std = parse_lab(lab_path)
    gt_segs = to_speech_silence(raw_segs)
    gt_boundaries = boundaries_from_segments(gt_segs)

    log_ste, centers, frame_len, hop_len = compute_log_ste(signal, sr, thr.frame_ms, thr.hop_ms)
    frame_labels = classify_frames(log_ste, thr.T, thr.lower_name)
    raw_pred_segs = frames_to_segments(frame_labels, centers, thr.hop_ms)
    pred_segs = remove_short_silences(raw_pred_segs, thr.min_silence_ms)
    pred_boundaries = boundaries_from_segments(pred_segs)

    rmse, mae, _errs = boundary_error_ms(pred_boundaries, gt_boundaries)
    snr = estimate_snr_db(signal, sr, gt_segs)

    f0_track = estimate_f0_track(signal, sr, centers, frame_len)
    # Chi giu F0 tai cac frame thuat toan gan nhan la SPEECH (sau hau xu ly)
    # - tranh hien F0 "ao" trong vung Silence do nhieu nen co tinh chu ky.
    is_speech = np.array([
        any(s <= t < e and lab == "speech" for s, e, lab in pred_segs)
        for t in centers
    ])
    f0_track = np.where(is_speech, f0_track, np.nan)

    result = FileTestResult(
        name=name, snr_db=snr,
        n_gt_boundaries=len(gt_boundaries), n_pred_boundaries=len(pred_boundaries),
        rmse_ms=rmse, mae_ms=mae,
        pred_boundaries=pred_boundaries, gt_boundaries=gt_boundaries,
    )
    return result, signal, sr, log_ste, centers, f0_track


# --------------------------------------------------------------------- #
# VE FIGURE: ket qua trung gian (log-STE) + ket qua cuoi (bien + F0)
# --------------------------------------------------------------------- #
def plot_result(result: FileTestResult, signal, sr, log_ste, centers, T, f0_track, out_dir):
    """
    Ve 1 figure gom: waveform + log-STE (ket qua trung gian), duong F0,
    bien du doan (xanh) va bien groundtruth (do) (ket qua cuoi cung).
    Luu file PNG vao out_dir va tra ve doi tuong Figure (de demo truc tiep).
    """
    t_signal = np.arange(len(signal)) / sr
    sig_norm = signal / (np.max(np.abs(signal)) + EPS)

    lo, hi = log_ste.min(), log_ste.max()
    ste_scaled = 2 * (log_ste - lo) / (hi - lo + EPS) - 1
    T_scaled = 2 * (T - lo) / (hi - lo + EPS) - 1

    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(t_signal, sig_norm, color="0.75", linewidth=0.6, label="Waveform (chuan hoa)")
    ax.plot(centers, ste_scaled, color="tab:blue", linewidth=1.3, label="log-STE (dac trung, chuan hoa)")
    ax.axhline(T_scaled, color="black", linestyle=":", linewidth=1, label="Nguong T (tu training)")

    for i, b in enumerate(result.pred_boundaries):
        ax.axvline(b, color="green", linewidth=1.5, alpha=0.9,
                    label="Bien du doan (thuat toan)" if i == 0 else None)
    for i, b in enumerate(result.gt_boundaries):
        ax.axvline(b, color="red", linestyle="--", linewidth=1.2, alpha=0.9,
                    label="Bien groundtruth (*.lab)" if i == 0 else None)

    ax.set_xlabel("Thoi gian (s)")
    ax.set_ylabel("Bien do / log-STE (chuan hoa)")
    ax.set_yticks([])
    ax.set_xlim(0, t_signal[-1])

    ax2 = ax.twinx()
    ax2.plot(centers, f0_track, "o", color="purple", markersize=3, label="F0 (Hz)")
    ax2.set_ylabel("F0 (Hz)", color="purple")
    ax2.tick_params(axis="y", colors="purple")
    ax2.set_ylim(0, 450)

    title = f"{result.name}   |   SNR~{result.snr_db:.1f} dB"
    if result.rmse_ms is not None:
        title += f"   |   RMSE={result.rmse_ms:.1f} ms, MAE={result.mae_ms:.1f} ms"
    ax.set_title(title, fontsize=13)

    lines1, labels1 = ax.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax.legend(lines1 + lines2, labels1 + labels2, loc="upper right", fontsize=8, ncol=2)
    fig.tight_layout()

    os.makedirs(out_dir, exist_ok=True)
    fig.savefig(os.path.join(out_dir, f"figure_{result.name}.png"), dpi=150)
    return fig


def arrange_figures_four_corners(figs):
    """
    Sap xep 4 cua so figure vao 4 goc man hinh - CHI dung khi demo truc
    tiep tren may co giao dien do hoa (backend TkAgg). Neu chay headless
    (vd server, khong co man hinh), bo qua trong im lang, khong crash CT.
    """
    try:
        mngr0 = figs[0].canvas.manager
        screen_w = mngr0.window.winfo_screenwidth()
        screen_h = mngr0.window.winfo_screenheight()
        w, h = screen_w // 2, screen_h // 2
        positions = [(0, 0), (w, 0), (0, h), (w, h)]
        for fig, (x, y) in zip(figs, positions):
            fig.canvas.manager.window.wm_geometry(f"{w}x{h}+{x}+{y}")
    except Exception:
        pass


# --------------------------------------------------------------------- #
# HAM CHINH: goi tu main.py o thu muc goc
# --------------------------------------------------------------------- #
def run(train_dir="data/TinHieuHuanLuyen", test_dir="data/TinHieuKiemThu", out_dir="outputs"):
    """
    Chay toan bo pipeline 1 lan duy nhat: TRAINING -> TESTING -> ve 4
    figure -> in/luu ket qua tong hop (RMSE/MAE theo SNR).
    """
    print("=" * 70)
    print("BUOC 1: TRAINING - tim nguong T toi uu tren du lieu huan luyen")
    print("=" * 70)
    thr = train_threshold(train_dir)

    print("\n" + "=" * 70)
    print("BUOC 2: KIEM THU - ap dung nguong T len cac file kiem thu")
    print("=" * 70)

    test_wavs = sorted(glob.glob(os.path.join(test_dir, "*.wav")))
    results, figs = [], []

    for wav_path in test_wavs:
        result, signal, sr, log_ste, centers, f0_track = test_one_file(wav_path, test_dir, thr)
        results.append(result)

        print(f"\n  --- {result.name} ---")
        print(f"    SNR uoc luong        : {result.snr_db:.1f} dB")
        print(f"    So bien groundtruth  : {result.n_gt_boundaries}")
        print(f"    So bien du doan      : {result.n_pred_boundaries}")
        if result.rmse_ms is not None:
            print(f"    RMSE                 : {result.rmse_ms:.1f} ms")
            print(f"    MAE                  : {result.mae_ms:.1f} ms")

        fig = plot_result(result, signal, sr, log_ste, centers, thr.T, f0_track, out_dir)
        figs.append(fig)

    # ---- Luu summary JSON (dung cho slide bao cao) -----------------------
    summary = {
        "threshold_T": thr.T, "lower_state": thr.lower_name,
        "frame_ms": thr.frame_ms, "hop_ms": thr.hop_ms, "min_silence_ms": thr.min_silence_ms,
        "train_snr_db": thr.train_snr_db,
        "test_results": [r.__dict__ for r in results],
    }
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "ket_qua_binary_search.json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    print("\n" + "=" * 70)
    print("TONG KET (dung cho slide):")
    print("=" * 70)
    valid = [r for r in results if r.rmse_ms is not None]
    if valid:
        print(f"  RMSE trung binh : {np.mean([r.rmse_ms for r in valid]):.1f} ms")
        print(f"  MAE  trung binh : {np.mean([r.mae_ms for r in valid]):.1f} ms")
    for r in sorted(results, key=lambda x: x.snr_db):
        print(f"    {r.name:12s} SNR={r.snr_db:5.1f} dB  ->  RMSE={r.rmse_ms:.1f} ms  MAE={r.mae_ms:.1f} ms")

    # ---- Demo truc tiep: xep 4 figure vao 4 goc man hinh va hien thi -----
    arrange_figures_four_corners(figs)
    try:
        plt.show()
    except Exception:
        pass
    for f in figs:
        plt.close(f)
