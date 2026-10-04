# -*- coding: utf-8 -*-
"""
src/models.py
Cac kieu du lieu (dataclass) dung chung giua cac module, giup code ro
nghia hon so vi dung tuple/dict "tran" khi truyen qua lai giua cac ham.
"""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class ThresholdResult:
    """Ket qua cua buoc TRAINING: nguong T va cac thong tin lien quan."""
    T: float                       # nguong toi uu tim duoc (Binary Search)
    lower_name: str                # 'speech' hoac 'silence' - trang thai thap hon
    frame_ms: float = 25
    hop_ms: float = 10
    min_silence_ms: float = 200
    train_snr_db: dict = field(default_factory=dict)  # {ten_file: SNR}


@dataclass
class FileTestResult:
    """Ket qua kiem thu tren 1 file tin hieu test."""
    name: str
    snr_db: Optional[float]
    n_gt_boundaries: int
    n_pred_boundaries: int
    rmse_ms: Optional[float]
    mae_ms: Optional[float]
    pred_boundaries: List[float] = field(default_factory=list)
    gt_boundaries: List[float] = field(default_factory=list)
