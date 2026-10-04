# -*- coding: utf-8 -*-
"""
main.py
========
DIEM KHOI CHAY DUY NHAT cua chuong trinh (theo dung yeu cau nop bai: CT
phai duoc khoi chay tu file main.py, chi chay 1 lan duy nhat).

Thuat toan cai dat: Energy-based Speech/Silence discrimination dung
BINARY SEARCH tim nguong (CS425 Audio and Speech Processing - Hodgkinson
2012, muc 2.1).

Cau truc thu muc:
    data/TinHieuHuanLuyen/   - tin hieu + *.lab dung de TRAIN (tim nguong T)
    data/TinHieuKiemThu/     - tin hieu + *.lab dung de TEST (bao cao)
    src/audio/               - doc file .wav, .lab
    src/features/             - tinh dac trung: log-STE (energy.py), F0 (pitch.py)
    src/segmentation/         - Binary Search tim nguong (threshold.py),
                                 phan loai + hau xu ly (segmenter.py)
    src/evaluate/              - RMSE/MAE, uoc luong SNR (metrics.py)
    src/models.py               - cac dataclass dung chung
    src/pipeline.py              - dieu phoi toan bo quy trinh + ve hinh
    outputs/                     - 4 figure (.png) + file ket qua .json

Cach chay:
    python3 main.py
"""

from src.pipeline import run

if __name__ == "__main__":
    run(
        train_dir="data/TinHieuHuanLuyen",
        test_dir="data/TinHieuKiemThu",
        out_dir="outputs",
    )
