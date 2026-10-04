# Module: `src/visualization`
Trực quan hóa kết quả phân đoạn tín hiệu và xuất các hình vẽ báo cáo kỹ thuật.

---

## 1. Các tệp thành phần

* **`plotting.py`**:
  - **`plot_signal_segmentation`**: Vẽ đồ thị kết quả 2 tầng cho một file kiểm thử:
    - **Tầng 1 (Trên - Dạng sóng âm thanh)**:
      * Dạng sóng biên độ $x(t)$.
      * Vùng tiếng nói chuẩn Ground Truth (tô màu nền xanh lá nhạt).
      * Các mốc biên chuẩn Ground Truth (đường dọc màu đỏ nét đứt).
      * Các mốc biên thuật toán tìm được (đường dọc màu xanh dương nét liền).
      * Tiêu đề hiển thị đầy đủ: Tên file, Môi trường, SNR (dB), Thuật toán, Ngưỡng $T$, MAE và RMSE (độ chính xác cao, tránh hiển thị `0.0ms`).
    - **Tầng 2 (Dưới - Hàm đặc trưng & Ngưỡng)**:
      * Với thuật toán **Histogram**: Hiển thị đường đặc trưng $\log(STE)$ màu cam và đường ngưỡng ngang $T_{\text{hist}}$.
      * Với thuật toán **Binary / Gaussian**: Hiển thị đường năng lượng chuẩn hóa $STE_{\text{norm}} \in [0, 1]$ và đường ngưỡng ngang $T$.
      * Gióng thẳng các vạch biên đỏ (GT) và xanh (thuật toán) từ tầng trên xuống để đối chiếu trực quan.
  - **`visualize_test_dataset`**: Duyệt qua toàn bộ danh sách 4 file kiểm thử cho từng thuật toán, tự động xuất và lưu 12 biểu đồ độc lập vào thư mục `reports/figures/figure_{i}_{name}_{algo}.png`.
  - **`plot_comparison_all_algorithms`**: Vẽ đồ thị so sánh xếp chồng trực tiếp cả 3 thuật toán (**Histogram**, **Binary**, **Gaussian**) trên cùng một file âm thanh và lưu tại `reports/figures/comparison_{name}.png` (4 biểu đồ tổng hợp).

---

## 2. Quy trình luồng làm việc (Pipeline)

```
Danh sách test_signals + Kết quả results + Chỉ số metrics_list
         │
         ├──► [visualize_test_dataset()]
         │       └──► Lưu 12 biểu đồ chi tiết (4 file × 3 thuật toán)
         │            tại: reports/figures/figure_{i}_{name}_{algo}.png
         │
         └──► [plot_comparison_all_algorithms()]
                 └──► Lưu 4 biểu đồ so sánh xếp chồng cả 3 thuật toán
                      tại: reports/figures/comparison_{name}.png
```
