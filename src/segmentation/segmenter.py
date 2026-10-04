# -*- coding: utf-8 -*-
"""
src/segmentation/segmenter.py
Ap dung nguong T de phan loai frame Speech/Silence, chuyen chuoi nhan
frame-by-frame thanh danh sach doan, va hau xu ly loai khoang lang
"ao" co do dai < 200ms (yeu cau cua bai tap).
"""

import numpy as np

MIN_SIL_MS_DEFAULT = 200


def classify_frames(log_ste, T, lower_name):
    """
    Phan loai tung frame Speech/Silence dua tren nguong T.
    Tham so:
        log_ste (np.ndarray): dac trung log-STE cua tin hieu can phan doan
        T (float): nguong (tu threshold.find_threshold_binary_search)
        lower_name (str): 'silence' neu Silence la trang thai co gia tri
                           thap hon, nguoc lai la 'speech'
    Tra ve:
        np.ndarray(dtype=str): nhan 'speech'/'silence' cho tung frame
    """
    if lower_name == "silence":
        labels = np.where(log_ste >= T, "speech", "silence")
    else:
        labels = np.where(log_ste >= T, "silence", "speech")
    return labels


def frames_to_segments(labels, centers_s, hop_ms):
    """
    Chuyen chuoi nhan frame-by-frame thanh danh sach doan (start, end, label).
    Bien giua 2 doan duoc lay la trung diem giua 2 frame lien ke co nhan khac nhau.
    Tham so:
        labels (array-like): nhan 'speech'/'silence' moi frame
        centers_s (np.ndarray): thoi diem tam moi frame (giay)
        hop_ms (float): buoc nhay giua 2 frame (ms), dung de uoc luong
                         diem bat dau/ket thuc tin hieu
    Tra ve:
        list[list]: [[start, end, label], ...]
    """
    hop_s = hop_ms / 1000.0
    segments = []
    start_t = centers_s[0] - hop_s / 2
    cur_label = labels[0]
    for i in range(1, len(labels)):
        if labels[i] != cur_label:
            end_t = (centers_s[i - 1] + centers_s[i]) / 2
            segments.append([start_t, end_t, cur_label])
            start_t = end_t
            cur_label = labels[i]
    end_t = centers_s[-1] + hop_s / 2
    segments.append([start_t, end_t, cur_label])
    return segments


def remove_short_silences(segments, min_sil_ms=MIN_SIL_MS_DEFAULT):
    """
    Loai bo cac khoang LANG "ao" co do dai < min_sil_ms (mac dinh 200ms):
    doi nhan thanh 'speech' roi gop voi doan speech lien ke, lap lai
    den khi danh sach doan on dinh (khong con khoang lang nao qua ngan).
    Tham so:
        segments (list): [(start, end, label), ...] - vd dau ra cua
                          frames_to_segments()
        min_sil_ms (float): do dai toi thieu (ms) cua 1 khoang lang hop le
    Tra ve:
        list[tuple]: danh sach doan sau hau xu ly
    """
    min_sil_s = min_sil_ms / 1000.0
    segs = [list(s) for s in segments]
    changed = True
    while changed:
        changed = False
        for seg in segs:
            if seg[2] == "silence" and (seg[1] - seg[0]) < min_sil_s:
                seg[2] = "speech"
                changed = True
        # Gop cac doan lien tiep cung nhan sau khi doi nhan
        merged = [segs[0]]
        for seg in segs[1:]:
            if seg[2] == merged[-1][2]:
                merged[-1][1] = seg[1]
            else:
                merged.append(seg)
        segs = merged
    return [tuple(s) for s in segs]
