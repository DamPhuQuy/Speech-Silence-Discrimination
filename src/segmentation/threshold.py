# -*- coding: utf-8 -*-
"""
src/segmentation/threshold.py
Thuat toan BINARY SEARCH tim nguong phan biet Speech/Silence, dung dung
muc 2.1.3 "Algorithm" cua CS425 Audio and Speech Processing - Hodgkinson
2012 (cong thuc 2.8 - can bang "area of confusion" giua 2 trang thai).
"""

import numpy as np


def label_frames(centers_s, sp_sil_segments):
    """
    Gan nhan speech/silence cho tung frame dua vao thoi diem tam frame
    va danh sach doan groundtruth (dau ra cua to_speech_silence()).
    Tham so:
        centers_s (np.ndarray): thoi diem tam cac frame (giay)
        sp_sil_segments (list[tuple]): [(start, end, 'speech'/'silence'), ...]
    Tra ve:
        np.ndarray(dtype=object): nhan 'speech'/'silence' cho tung frame
    """
    labels = np.empty(len(centers_s), dtype=object)
    labels[:] = "silence"
    for s, e, cls in sp_sil_segments:
        mask = (centers_s >= s) & (centers_s < e)
        labels[mask] = cls
    # Frame cuoi cung co the roi ngoai doan cuoi do lam tron -> gan theo
    # doan groundtruth cuoi cung de khong bi sot nhan.
    if len(sp_sil_segments) > 0:
        last_s, last_e, last_cls = sp_sil_segments[-1]
        labels[centers_s >= last_e - 1e-9] = last_cls
    return labels


def find_threshold_binary_search(silence_vals, speech_vals, verbose=True):
    """
    Tim nguong T bang BINARY SEARCH, dung 10 buoc trong muc 2.1.3:
      - f = tap gia tri cua trang thai THAP hon (thuong la Silence)
      - g = tap gia tri cua trang thai CAO hon (thuong la Speech)
      - Chi giu lai phan CHONG LAP (overlap) cua f va g
      - Lap: tinh ve trai cong thuc (2.8); >0 -> Tmin=T; else Tmax=T
      - Dung khi so diem f<T va g>T khong doi giua 2 vong lap lien tiep

    Tham so:
        silence_vals (np.ndarray): gia tri dac trung (vd log-STE) cac
                                    frame Silence (training)
        speech_vals (np.ndarray): gia tri dac trung cac frame Speech
        verbose (bool): co in thong tin qua trinh hoi tu hay khong
    Tra ve:
        T (float): nguong toi uu
        lower_name (str): ten trang thai co gia tri THAP hon ('speech'
                           hoac 'silence') - dung de biet chieu so sanh
    """
    if np.mean(silence_vals) <= np.mean(speech_vals):
        f_all, g_all = np.sort(silence_vals), np.sort(speech_vals)
        lower_name = "silence"
    else:
        f_all, g_all = np.sort(speech_vals), np.sort(silence_vals)
        lower_name = "speech"

    # Buoc 1: chi giu lai phan f, g nam trong vung chong lap
    f = f_all[f_all >= g_all.min()]
    g = g_all[g_all <= f_all.max()]
    if len(f) == 0 or len(g) == 0:
        # Khong co overlap (2 phan bo tach biet hoan toan) -> lay trung diem
        T = (f_all.max() + g_all.min()) / 2.0
        if verbose:
            print("  [!] Khong phat hien overlap -> T = trung diem 2 phan bo")
        return T, lower_name

    Nf, Ng = len(f), len(g)

    # Buoc 2-3: khoi tao Tmin, Tmax, T
    Tmin, Tmax = min(f.min(), g.min()), max(f.max(), g.max())
    T = 0.5 * (Tmin + Tmax)

    # Buoc 4-5: khoi tao bo dem i, p va j, q
    i = np.sum(f < T)
    p = np.sum(g > T)
    j, q = -1, -1

    # Buoc 6-10: lap binary search den khi hoi tu (i, p khong doi)
    n_iter = 0
    while i != j or p != q:
        lhs = (1.0 / Nf) * np.sum(np.maximum(f - T, 0)) - (1.0 / Ng) * np.sum(np.maximum(T - g, 0))
        if lhs > 0:
            Tmin = T
        else:
            Tmax = T
        T = 0.5 * (Tmin + Tmax)
        j, q = i, p
        i = np.sum(f < T)
        p = np.sum(g > T)
        n_iter += 1
        if n_iter > 200:  # chong vong lap vo han do sai so dau phay dong
            break

    if verbose:
        print(f"  Binary search hoi tu sau {n_iter} vong lap. "
              f"Nf(overlap {lower_name})={Nf}, Ng(overlap khac)={Ng}")

    return T, lower_name
