# Task Lite: GAUSS-SUBPLOT-01 Bổ Sung Subplot Điểm Giao Nhau Phân Phối Gauss

<task_lite version="3.0" framework="RIPER-5-Lite">

<!-- ════════════════════════════════════════════
     SECTION 0 — TASK CONTROL
     ════════════════════════════════════════════ -->
<task_control>
  <track>LITE</track>
  <status>COMPLETED</status>
  <priority>P2</priority>
  <working_mode>PAIR</working_mode>
  <observability_mode>OFF</observability_mode>
  <current_phase>REVIEW</current_phase>
  <owner>@antigravity</owner>
</task_control>

---

## 1. Intent & Specification

<specification>
  <goal>
    Cập nhật Code Cell 5 (Mục 3.1) trong [gauss.ipynb](file:///home/phuqy/Documents/main_gk/gauss.ipynb) để bổ sung thêm subplot thứ 2 trực quan hóa cận cảnh điểm giao nhau giữa 2 phân phối chuẩn Gauss (Silence và Speech) tại ngưỡng tối ưu $T^* \approx 0.000791$, đồng thời cập nhật file ảnh xuất ra tại [figure_gaussian_threshold_analysis.png](file:///home/phuqy/Documents/main_gk/reports/figures/figure_gaussian_threshold_analysis.png).
  </goal>

  <invariants>
    - Duy trì mã nguồn thuần NumPy và Matplotlib (không dùng scipy.stats).
    - Giữ nguyên các tham số thống kê ($\mu, \sigma$) và giá trị ngưỡng $T^*$.
    - Không làm thay đổi kết quả phân đoạn hoặc sai số MAE/RMSE trên tập kiểm thử.
  </invariants>

  <acceptance_criteria>
    - [x] AC-1: Cell 5 (Mục 3.1) hiển thị 2 subplots: (a) Toàn cảnh phân phối Gauss [0, 0.6] và (b) Cận cảnh điểm giao nhau quanh ngưỡng $T^*$ [0, 0.0035] có đánh dấu điểm giao nhau $(T^*, y_{\text{intersect}})$.
    - [x] AC-2: Cập nhật file ảnh [figure_gaussian_threshold_analysis.png](file:///home/phuqy/Documents/main_gk/reports/figures/figure_gaussian_threshold_analysis.png).
    - [x] AC-3: Notebook [gauss.ipynb](file:///home/phuqy/Documents/main_gk/gauss.ipynb) thực thi hoàn tất không lỗi, hiển thị đồ thị 2 panel trong outputs.
  </acceptance_criteria>

  <definition_of_ready>
    - [x] Mục tiêu và tiêu chuẩn nghiệm thu rõ ràng.
    - [x] File cho phép trong Section 2 đã xác định.
  </definition_of_ready>
</specification>

---

## 2. Scope Contract & File Whitelist

<scope_contract>
  <allowed_files>
    <file>/home/phuqy/Documents/main_gk/gauss.ipynb</file>
    <file>/home/phuqy/Documents/main_gk/reports/figures/figure_gaussian_threshold_analysis.png</file>
  </allowed_files>

  <forbidden_files>
    <file>/home/phuqy/Documents/main_gk/binary.ipynb</file>
    <file>/home/phuqy/Documents/main_gk/histogram.ipynb</file>
    <file>/home/phuqy/Documents/main_gk/data/**</file>
  </forbidden_files>

  <negative_constraints>
    - Không sửa đổi logic các cell khác trong gauss.ipynb.
    - Không sử dụng thư viện ngoài `scipy.stats`.
  </negative_constraints>
</scope_contract>

---

## 3. Implementation Plan

<plan>
  - Bước 1: Cập nhật mã nguồn Cell index 9 trong `gauss.ipynb` để vẽ `fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 4.8), dpi=120)`.
    + Panel (a): Toàn cảnh 2 hình chuông phân phối Gauss $[0.0, 0.6]$.
    + Panel (b): Phóng to cận cảnh điểm giao nhau quanh ngưỡng $T^*$ $[0.0, 0.0035]$ kèm điểm giao nhau $(T^*, y_{\text{intersect}})$ và mũi tên chú thích.
  - Bước 2: Chạy kernel thực thi để lưu outputs mới và cập nhật file ảnh.
  - Bước 3: Kiểm chứng kết quả hiển thị.
</plan>

---

## 4. Verification

<verification>
  - Kiểm tra số lượng axes trong output của Cell 9: Đủ 2 axes (2 subplots).
  - Kiểm tra file ảnh `figure_gaussian_threshold_analysis.png` được cập nhật.
</verification>

</task_lite>
