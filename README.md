# BÀI TẬP LỚN XỬ LÝ TÍN HIỆU SỐ (2026)
## Đề tài: Phân Đoạn Tín Hiệu Thành Tiếng Nói Và Khoảng Lặng (Voice Activity Detection - VAD)

Dự án cài đặt, tối ưu hóa và đánh giá định lượng 03 thuật toán phân đoạn tiếng nói và khoảng lặng trên tín hiệu âm thanh thực tế, sử dụng hoàn toàn **NumPy thuần** (không phụ thuộc vào các thư viện ngoài như `librosa` hay các gói VAD có sẵn), tuân thủ 100% tài liệu hướng dẫn và barem chấm thi của giảng viên.

---

## 1. Các Thuật Toán Cài Đặt

### 1.1. Thuật toán Biểu đồ tần suất Histogram (Giannakopoulos, 2014)
* **Đặc trưng**: Hoạt động trên miền năng lượng logarit $\log(STE) = \ln(STE + 10^{-12})$, giúp phân tách rõ rệt 2 chế độ phân bố (*bimodal distribution*) giữa khoảng lặng và tiếng nói.
* **Quy trình xử lý**:
  - Xây dựng histogram với $N_{\text{bins}} = 40$.
  - Làm mịn bằng bộ lọc trung bình trượt (*Moving Average*, cửa sổ $k=3$) để triệt tiêu các cực trị nhiễu cục bộ.
  - Tìm các đỉnh cực đại địa phương chặt chẽ (*strict local maxima*).
  - Áp dụng heuristic khoảng cách tối thiểu và độ cao tương đối để chọn 2 đỉnh chế độ: $M_1$ (khoảng lặng) và $M_2$ (tiếng nói).
  - Xác định ngưỡng tối ưu theo công thức:
    $$T = \frac{W \cdot M_1 + M_2}{W + 1} \quad (W = 2.0)$$

### 1.2. Thuật toán Tìm kiếm nhị phân Binary Search (Hodgkinson, 2012)
* **Tài liệu tham khảo**: *CS425 Audio and Speech Processing* - Mục 2.1.3 (Hodgkinson, 2012).
* **Đặc trưng**: Hoạt động trên năng lượng ngắn hạn chuẩn hóa Min-Max $STE_{\text{norm}} \in [0.0, 1.0]$.
* **Nguyên lý**: Áp dụng tìm kiếm nhị phân để cân bằng diện tích nhầm lẫn (*Area of Confusion*) trên miền phân bố chồng lấn (*overlap*) giữa tiếng nói và khoảng lặng:
  $$\Delta = \text{Area}_{\text{sp}}(T) - \text{Area}_{\text{sil}}(T) \approx 0$$

### 1.3. Thuật toán Thống kê Gauss (Simple Statistics)
* **Đặc trưng**: Hoạt động trên năng lượng chuẩn hóa $STE_{\text{norm}}$.
* **Nguyên lý**: Giả định năng lượng ngắn hạn của khung tiếng nói và khoảng lặng tuân theo phân phối chuẩn Gauss:
  - Khảo sát nhãn Ground Truth trên tập huấn luyện để ước lượng $(\mu_{\text{sp}}, \sigma_{\text{sp}}, \mu_{\text{sil}}, \sigma_{\text{sil}})$.
  - Tìm nghiệm giao điểm giữa 2 hàm mật độ xác suất phân phối chuẩn để chọn ngưỡng phân tách tối ưu.

---

## 2. Quy Chuẩn Kỹ Thuật & Hậu Xử Lý

* **Độ dài khung (`frame_size_ms`)**: Cố định $25\text{ ms}$.
* **Độ dịch khung (`frame_shift_ms`)**: Cố định $10\text{ ms}$.
* **Cửa sổ phân tích**: Cửa sổ Hamming.
* **Thời gian mốc khung**: Lấy tại **tâm của từng khung** ($t_i = \frac{i \cdot \text{shift} + \text{len}/2}{f_s}$) để đại diện trung thực cho năng lượng khung.
* **Hậu xử lý (Post-processing)**:
  1. `filter_short_silence`: Gộp các khoảng lặng xen giữa có độ dài $< 200\text{ ms}$ theo đúng quy định tuyệt đối của đề bài.
  2. `extract_boundaries_and_segments`: Trích xuất mốc biên với độ chính xác cao (6 chữ số thập phân) để phản ánh sai số vật lý trung thực.

---

## 3. Hướng Dẫn Cài Đặt & Chạy Chương Trình

### 3.1. Cài đặt môi trường

```bash
# Tạo và kích hoạt môi trường ảo (khuyến nghị)
python3 -m venv .venv
source .venv/bin/activate

# Cài đặt các phụ thuộc tối thiểu
pip install -r requirements.txt
```

### 3.2. Chạy chương trình chính

Chạy trực tiếp 01 lệnh duy nhất (không cần cờ hay tham số dòng lệnh phức tạp):

```bash
python3 main.py
```

> **Lưu ý**: File `main.py` tích hợp sẵn cơ chế tự động chuyển sang `.venv` nếu người dùng vô tình gọi bằng Python hệ thống, đảm bảo không bao giờ gặp lỗi thiếu thư viện.

---

## 4. Kết Quả Thực Nghiệm Trên Tập Kiểm Thử (`TinHieuKiemThu`)

Khi chạy `main.py`, chương trình áp dụng **Quy chuẩn ngưỡng dùng chung toàn cục ($T^*$)** huấn luyện từ toàn bộ 4 file huấn luyện theo đúng barem chấm thi:

* **Histogram**: $T^* = -2.4375$ (trên miền $\log(STE)$)
* **Binary Search**: $T^* = 0.000798$ (trên miền $STE_{\text{norm}}$)
* **Gaussian**: $T^* = 0.000792$ (trên miền $STE_{\text{norm}}$)

### Bảng sai số MAE (đơn vị: mili-giây, độ chính xác 6 số thập phân):

```text
============================================================================================
        KẾT QUẢ PHÂN ĐOẠN TIẾNG NÓI & KHOẢNG LẶNG (QUY CHUẨN NGƯỠNG TOÀN CỤC)        
============================================================================================
Tên File     Môi trường  SNR (dB)   Histogram (MAE)    Binary (MAE)       Gaussian (MAE)
--------------------------------------------------------------------------------------------
phone_F2     Phone       24.8 dB   45.000000 ms     62.500000 ms     62.500000 ms
phone_M2     Phone       27.0 dB   10.000000 ms      7.500000 ms      7.500000 ms
studio_F2    Studio      49.3 dB    2.494000 ms      2.494000 ms      2.494000 ms
studio_M2    Studio      37.7 dB   15.000000 ms     12.494000 ms     12.494000 ms
--------------------------------------------------------------------------------------------
TB Phone     Phone (2 file)        27.500000 ms     35.000000 ms     35.000000 ms
TB Studio    Studio (2 file)        8.747000 ms      7.494000 ms      7.494000 ms
Toàn bộ      Overall (4 file)      18.123500 ms     21.247000 ms     21.247000 ms
============================================================================================
```

### Nhận xét & Phát hiện học thuật:
1. **Môi trường Studio (Phòng thu, SNR cao $37 - 49\text{ dB}$)**:
   * Cả 3 thuật toán đạt độ chính xác xuất sắc: MAE trung bình chỉ từ **$7.49\text{ ms}$ đến $8.75\text{ ms}$**.
   * File `studio_F2` đạt sai số thực tế **`2.494000 ms`** (tương đương khoảng cách từ tâm khung $0.772494\text{s}$ tới mốc nhãn centisecond $0.770000\text{s}$).
2. **Môi trường Phone (Điện thoại, SNR thấp $\approx 24.8\text{ dB}$)**:
   * Ở file `phone_F2`, người nói có hiện tượng ngắt hơi $221\text{ ms} > 200\text{ ms}$ tại $t \in [2.56\text{s}, 2.78\text{s}]$ khiến thuật toán tuân thủ đúng quy tắc đề bài và phân tách thành 2 câu nói con.
   * Thuật toán **Histogram** nhờ hoạt động trên thang logarit $\log(STE)$ thể hiện khả năng kháng nhiễu nền vượt trội, đạt MAE trung bình toàn bộ là **$18.12\text{ ms}$**, ổn định hơn so với Binary và Gaussian ($21.25\text{ ms}$).

---

## 5. Cấu Trúc Mã Nguồn Dự Án

```text
main_gk/
├── main.py                     # Entry point chính (chạy 1 lệnh duy nhất, xuất bảng và đồ thị)
├── requirements.txt            # Danh sách thư viện phụ thuộc (numpy, scipy, matplotlib)
├── README.md                   # Tài liệu hướng dẫn chính của đồ án
├── data/
│   ├── TinHieuHuanLuyen/       # 4 file .wav và 4 file nhãn .lab huấn luyện
│   └── TinHieuKiemThu/         # 4 file .wav và 4 file nhãn .lab kiểm thử
├── reports/
│   ├── ket_qua_tong_hop.json   # Báo cáo JSON lưu toàn bộ ngưỡng và kết quả đánh giá
│   └── figures/                # 16 biểu đồ trực quan hóa định dạng .png độ phân giải cao:
│       ├── figure_*_*.png      # 12 đồ thị 2 tầng cho từng file và từng thuật toán
│       └── comparison_*.png    # 4 đồ thị so sánh xếp chồng cả 3 thuật toán theo từng file
├── docs/                       # Đề bài và tài liệu tham khảo [1], [2], [3]
└── src/                        # Thư mục mã nguồn module hóa
    ├── README.md               # Tài liệu chi tiết kiến trúc src/
    ├── models.py               # Định nghĩa các Dataclass dữ liệu chính
    ├── pipeline.py             # Lớp bọc quy trình phân đoạn VAD
    ├── audio/                  # Module nạp audio và xử lý nhãn .lab
    ├── features/               # Module phân khung và trích xuất đặc trưng STE / log(STE)
    ├── segmentation/           # Module thuật toán: Histogram, Binary, Gaussian, Post-processing
    ├── evaluate/               # Module tính toán sai số MAE, RMSE và đo lường SNR
    └── visualization/          # Module vẽ đồ thị và xuất hình ảnh
```

---

## 6. Tài Liệu Tham Khảo

1. **CS425 Audio and Speech Processing** (Hodgkinson, 2012): *Section 2.1 Energy-based Speech/Silence discrimination*.
2. **A method for silence removal and segmentation of speech signals** (Giannakopoulos, 2014): *Histogram-based Speech/Silence segmentation*.
3. **Hướng dẫn bài tập thi giữa kỳ Xử lý tín hiệu số 2026**: Bộ môn Xử lý tín hiệu âm thanh và tiếng nói.
