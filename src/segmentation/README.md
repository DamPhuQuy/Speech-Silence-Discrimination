# Module: `src/segmentation`
Cài đặt các thuật toán tìm ngưỡng phân đoạn Speech/Silence, phân loại khung và hậu xử lý lọc nhiễu.

---

## 1. Các tệp thành phần

* **`histogram.py`**: Thuật toán Biểu đồ tần suất Histogram theo tài liệu **Giannakopoulos (2014)**:
  - Xây dựng biểu đồ tần suất năng lượng trên thang logarit `log_ste` với $N_{\text{bins}} = 40$.
  - Áp dụng bộ lọc làm mịn trung bình trượt (*Moving Average*, cửa sổ $k=3$) để triệt tiêu các dao động nhiễu cục bộ.
  - Tìm các đỉnh cực đại địa phương chặt chẽ (*strict local maxima*).
  - Lựa chọn 2 đỉnh chế độ đại diện ($M_1$: Đỉnh khoảng lặng, $M_2$: Đỉnh tiếng nói) dựa trên heuristic khoảng cách tối thiểu và độ cao tương đối.
  - Xác định ngưỡng phân đoạn tối ưu theo công thức:
    $$T = \frac{W \cdot M_1 + M_2}{W + 1} \quad (\text{với } W = 2.0)$$
* **`binary.py`**: Thuật toán Tìm kiếm nhị phân theo tài liệu **CS425 (Hodgkinson, 2012) - Mục 2.1.3**:
  - Dùng tìm kiếm nhị phân để cân bằng diện tích nhầm lẫn (*Area of Confusion*) trên vùng chồng lấn giữa phân bố Speech và Silence:
    $$\Delta = \text{Area}_{\text{sp}}(T) - \text{Area}_{\text{sil}}(T) \approx 0$$
* **`gauss.py`**: Thuật toán mô hình thống kê phân phối chuẩn Gauss (Simple Statistics):
  - Khảo sát các khung Speech và Silence trên tập huấn luyện để ước lượng $(\mu_{\text{sp}}, \sigma_{\text{sp}}, \mu_{\text{sil}}, \sigma_{\text{sil}})$.
  - Giải phương trình bậc hai tìm giao điểm phân tách tối ưu giữa 2 hàm mật độ xác suất Gauss.
* **`threshold.py`**: Điều phối huấn luyện bộ ngưỡng trên tập `TinHieuHuanLuyen`:
  - **Ngưỡng quy chuẩn toàn cục (`global`)**: Tính ngưỡng dùng chung cho cả 4 file huấn luyện theo đúng quy định barem đề bài.
  - **Ngưỡng thích nghi môi trường (`phone`, `studio`)**: Tính riêng cho từng môi trường để đánh giá mức độ ảnh hưởng của SNR.
* **`postprocess.py`**: Hậu xử lý kết quả phân đoạn:
  - **`filter_short_silence`**: Gộp các khoảng lặng ảo $< 200\text{ ms}$ theo đúng quy định đề bài.
  - **`filter_short_speech`**: Loại bỏ các mẩu tiếng nói ngắn $< 30\text{ ms}$ sinh ra do nhiễu xung micro (clicks) hoặc tiếng thở ở môi trường điện thoại.
  - **`extract_boundaries_and_segments`**: Trích xuất các mốc biên thời gian thực với độ chính xác 6 số thập phân (tránh sai số làm tròn $0.0\text{ ms}$).
* **`segment.py`**: Hàm điều phối phân đoạn tín hiệu kiểm thử hoàn chỉnh.

---

## 2. Quy trình luồng làm việc (Pipeline)

### Giai đoạn 1: Hiệu chuẩn ngưỡng (Training)
```
Tập huấn luyện (TinHieuHuanLuyen)
         │
         ▼
[threshold.py: calibrate_thresholds()]
         ├──> [histogram.py: find_threshold_histogram()]   ──► Ngưỡng T_hist (log-STE)
         ├──> [binary.py: find_threshold_binary()]         ──► Ngưỡng T_bin  (norm-STE)
         └──> [gauss.py: find_threshold_gaussian()]        ──► Ngưỡng T_gauss(norm-STE)
         │
         ▼
Đối tượng Threshold (Chứa các bộ tham số tối ưu dùng chung và theo môi trường)
```

### Giai đoạn 2: Phân đoạn tín hiệu kiểm thử (Inference)
```
AudioSignal (File test) + Ngưỡng T
         │
         ▼
[segment.py: segment_signal()]
         │
         ├──> Quyết định sơ bộ: Feature[i] >= T ? (1: Speech, 0: Silence)
         │
         ├──> [postprocess.py: filter_short_silence()]  --> Lọc khoảng lặng < 200ms
         │
         ├──> [postprocess.py: filter_short_speech()]   --> Lọc xung tiếng nói < 30ms
         │
         └──> [postprocess.py: extract_boundaries_and_segments()]
         │
         ▼
Đối tượng SegmentationResult (Biên dự đoán độ chính xác cao + Phân đoạn)
```
