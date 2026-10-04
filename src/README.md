# Kiến trúc Mã nguồn Dự án (`src/`)

Thư mục `src/` chứa toàn bộ kiến trúc phân đoạn tiếng nói và khoảng lặng (VAD - Voice Activity Detection) thuần NumPy theo cấu trúc module hướng đối tượng và dataclass sạch sẽ.

---

## 1. Cấu trúc các gói thành phần

```
src/
├── audio/          # Nạp file âm thanh .wav và phân tích file nhãn chuẩn .lab
│   ├── dataset.py  # Quét và ghép cặp các file tín hiệu và nhãn
│   ├── labels.py   # Phân tích cú pháp .lab, trích xuất biên chuẩn GT
│   └── loader.py   # Đọc tín hiệu âm thanh và chuẩn hóa biên độ
├── features/       # Phân khung và trích xuất đặc trưng âm học ngắn hạn
│   ├── extraction.py # Tính toán STE chuẩn hóa và log(STE)
│   ├── framing.py    # Phân khung ngắn hạn (25ms, shift 10ms, Hamming)
│   └── pitch.py      # Ước lượng tần số cơ bản F0 bằng tự tương quan
├── segmentation/   # Thuật toán tìm ngưỡng, phân đoạn và hậu xử lý
│   ├── binary.py     # Thuật toán Tìm kiếm nhị phân (Hodgkinson, 2012)
│   ├── gauss.py      # Thuật toán Thống kê Gauss (Simple Statistics)
│   ├── histogram.py  # Thuật toán Biểu đồ tần suất (Giannakopoulos, 2014)
│   ├── threshold.py  # Điều phối hiệu chuẩn bộ ngưỡng (Toàn cục & Môi trường)
│   ├── segment.py    # Phân đoạn khung tín hiệu theo ngưỡng
│   └── postprocess.py # Lọc khoảng lặng < 200ms, lọc xung nhiễu < 30ms
├── evaluate/       # Đo lường sai số định lượng và ước lượng SNR
│   └── metrics.py    # Tính MAE, RMSE (độ chính xác 6 số thập phân), SNR (dB)
├── visualization/  # Trực quan hóa và xuất biểu đồ kỹ thuật
│   └── plotting.py   # Vẽ đồ thị 2 tầng (Sóng âm + STE/log-STE) và so sánh xếp chồng
├── models.py       # Định nghĩa các Dataclass cấu trúc dữ liệu chính
└── pipeline.py     # Lớp bọc quy trình thực thi đồng bộ
```

---

## 2. Mô hình Dữ liệu (`models.py`)

* **`AudioSignal`**: Đại diện tín hiệu âm thanh (`name`, `signal`, `fs`, `duration_sec`, `is_phone`, `gt_boundaries`, `gt_segments`).
* **`FrameSignal`**: Mảng các khung tín hiệu ngắn hạn và mốc thời gian tâm khung (`frames`, `timestamps`, `raw_frames`).
* **`ShortTimeFeatures`**: Tập đặc trưng trích xuất theo khung (`ste_raw`, `ste_norm`, `log_ste`).
* **`Threshold`**: Bộ ngưỡng phân đoạn đã hiệu chuẩn của 3 thuật toán cho cả mức Toàn cục (`global`) và theo Môi trường (`phone`, `studio`).
* **`SegmentationResult`**: Kết quả phân đoạn (`predicted_boundaries`, `raw_decisions`, `filtered_decisions`, `segments`).
* **`EvaluationMetrics`**: Bộ chỉ số đánh giá độ chính xác (`mae_ms`, `rmse_ms`, `snr_db`, `matched_pairs`).

---

## 3. Luồng hoạt động tổng thể (Pipeline)

```
1. Tập dữ liệu Huấn luyện (TinHieuHuanLuyen)
   │
   ▼
[calibrate_thresholds()] ───────────────► Tính ngưỡng chuẩn hóa:
   │                                       • Histogram (log-STE)
   │                                       • Binary (norm-STE)
   │                                       • Gaussian (norm-STE)
   ▼
2. Tập dữ liệu Kiểm thử (TinHieuKiemThu)
   │
   ▼
[segment_signal()] ─────────────────────► 1. So sánh đặc trưng với ngưỡng
   │                                      2. Lọc khoảng lặng ngắn < 200ms
   │                                      3. Lọc xung tiếng nói ngắn < 30ms
   │                                      4. Trích xuất biên (độ phân giải 6 số thập phân)
   ▼
3. Đánh giá & Báo cáo
   │
   ├──> [evaluate_signal()] ────────────► Tính MAE / RMSE (ms) & SNR (dB)
   ├──> [visualize_test_dataset()] ─────► Lưu 12 biểu đồ từng thuật toán
   ├──> [plot_comparison_all_algorithms()] ──► Lưu 4 biểu đồ so sánh xếp chồng
   └──> [main.py] ──────────────────────► In bảng tổng hợp & xuất JSON báo cáo
```
