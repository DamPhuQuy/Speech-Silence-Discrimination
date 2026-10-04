# -*- coding: utf-8 -*-
"""
src/audio/labels.py
Doc va xu ly file groundtruth *.lab (dinh dang mo ta trong README):
    bien_trai <TAB> bien_phai <TAB> nhan(sil/v/uv)
    ...
    F0mean <TAB> gia_tri
    F0std  <TAB> gia_tri
"""


def parse_lab(path):
    """
    Doc 1 file .lab.
    Tham so:
        path (str): duong dan file .lab
    Tra ve:
        segments (list[tuple]): [(start_s, end_s, label), ...]
                                 label thuoc {"sil", "v", "uv"}
        f0mean (float | None): F0 trung binh (Hz) ghi trong file
        f0std  (float | None): do lech chuan cua F0 (Hz)
    """
    segments = []
    f0mean = f0std = None
    with open(path, "r", encoding="utf-8") as f:
        for raw_line in f:
            line = raw_line.strip()
            if not line:
                continue
            # Tach theo TAB, bo cac phan tu rong do co nhieu TAB lien tiep
            parts = [p for p in line.split("\t") if p.strip() != ""]
            if len(parts) < 2:
                continue
            tag = parts[0].strip().lower()
            if tag == "f0mean":
                f0mean = float(parts[1])
            elif tag == "f0std":
                f0std = float(parts[1])
            else:
                start, end, label = float(parts[0]), float(parts[1]), parts[2].strip().lower()
                segments.append((start, end, label))
    return segments, f0mean, f0std


def to_speech_silence(segments):
    """
    Gop nhan 'v' (voiced) va 'uv' (unvoiced) thanh 'speech'; 'sil' -> 'silence'.
    Gop cac doan lien tiep cung nhan thanh 1 doan duy nhat.
    Tham so:
        segments (list[tuple]): dau ra cua parse_lab()
    Tra ve:
        list[tuple]: [(start, end, 'speech'/'silence'), ...]
    """
    merged = []
    for s, e, lab in segments:
        cls = "silence" if lab == "sil" else "speech"
        if merged and merged[-1][2] == cls:
            # Doan moi cung nhan voi doan truoc -> noi dai doan truoc
            merged[-1] = (merged[-1][0], e, cls)
        else:
            merged.append([s, e, cls])
    return [tuple(m) for m in merged]


def boundaries_from_segments(segments):
    """
    Lay cac moc thoi gian (giay) la bien chuyen Speech<->Silence,
    khong tinh bien dau/cuoi tin hieu (t=0 va t=cuoi file).
    Tham so:
        segments (list[tuple]): [(start, end, label), ...] da gop nhan
    Tra ve:
        list[float]: cac moc thoi gian bien (giay)
    """
    return [segments[i][0] for i in range(1, len(segments))]
