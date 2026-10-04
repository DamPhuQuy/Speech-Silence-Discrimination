# Module: `src/features`
Chia khung tín hiệu ngắn hạn và trích xuất các đặc trưng âm học.

---

## 1. Các tệp thành phần

* **`framing.py`**: Chia tín hiệu âm thanh liên tục thành các khung ngắn hạn (Short-Time Frames):
  - Kích thước khung cố định theo đề bài: $25\text{ ms}$ (`frame_size_ms`).
  - Bước dịch khung cố định: $10\text{ ms}$ (`frame_shift_ms`).
  - Hàm cửa sổ áp dụng (`window_type`, mặc định là `hamming`).
  - Tọa độ thời gian tại tâm từng khung (`timestamps`):
    $$t_i = \frac{i \times \text{frame\_shift} + \frac{\text{frame\_len}}{2}}{f_s}$$
  - Trả về đối tượng `FrameSignal` chứa cả khung đã nhân cửa sổ (`frames`) và khung thô (`raw_frames`).
* **`extraction.py`**: Trích xuất các đặc trưng năng lượng ngắn hạn (Short-Time Energy - STE):
  - **Năng lượng thô (`ste_raw`)**:
    $$STE_i = \sum_{m=0}^{N-1} x_i^2[m]$$
  - **Năng lượng chuẩn hóa Min-Max (`ste_norm`)**: Dùng cho thuật toán Binary Search và Gaussian:
    $$STE_{\text{norm}, i} = \frac{STE_i - \min(STE)}{\max(STE) - \min(STE)}$$
  - **Năng lượng logarit (`log_ste`)**: Dùng cho thuật toán Histogram (Giannakopoulos, 2014) giúp tách rõ 2 chế độ phân bố bimodal giữa tiếng nói và nhiễu nền:
    $$\log STE_i = \ln(STE_i + 10^{-12})$$
  - Đóng gói kết quả vào đối tượng `ShortTimeFeatures`.
* **`pitch.py`**: Ước lượng đường cong cao độ $F_0$ (Pitch Tracking):
  - Sử dụng hàm tự tương quan (*Autocorrelation Function - ACF*).
  - Tìm đỉnh cực đại trong dải tần số cơ bản con người $[60\text{ Hz}, 400\text{ Hz}]$.
  - Gán `NaN` cho các khung vô thanh hoặc khoảng lặng dựa trên ngưỡng độ tin cậy (*voicing confidence*).

---

## 2. Quy trình luồng làm việc (Pipeline)

```
AudioSignal (Mảng sóng âm + fs)
         │
         ▼
[framing.py: apply_framing()]
         │  --> Chia khung (25ms, bước nhảy 10ms, tâm khung chính xác)
         ▼
FrameSignal (Ma trận khung + timestamps)
         │
         ▼
[extraction.py: extract_features()]
         │  ├──> ste_norm: [0.0, 1.0]  (Dùng cho Binary & Gaussian)
         │  └──> log_ste: ln(STE + ε)   (Dùng cho Histogram)
         ▼
ShortTimeFeatures
```
