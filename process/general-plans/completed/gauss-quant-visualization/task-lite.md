# Task Lite: GAUSS-QUANT-01 Trực quan hóa và Xuất Bảng/Hình Định Lượng Cho Thuật Toán Gauss

<task_lite version="3.0" framework="RIPER-5-Lite">

<!-- ════════════════════════════════════════════
     SECTION 0 — TASK CONTROL
     ════════════════════════════════════════════ -->
<task_control>
  <track>LITE</track>
  <status>REVIEW</status>
  <priority>P1</priority>
  <working_mode>PAIR</working_mode>
  <observability_mode>OFF</observability_mode>
  <current_phase>REVIEW</current_phase>
  <owner>@DamPhuQuy</owner>
</task_control>

---

## 1. Intent & Specification

<specification>
  <goal>
    Bổ sung biểu đồ phân bố Gauss (Gaussian PDF Curves) tìm ngưỡng tối ưu T* và bảng số liệu định lượng trung gian (mean, std, số khung theo từng file huấn luyện và pooled all) trong notebook gauss.ipynb, tự động xuất hình ảnh độ phân giải cao vào reports/figures/ để phục vụ trình bày slide và báo cáo giữa kỳ.
  </goal>

  <invariants>
    - Giữ nguyên các hàm cốt lõi, tham số framing (25ms/10ms), ngưỡng tối ưu T_gaussian = 0.000792 và kết quả phân đoạn 4 file kiểm thử.
    - Không sửa đổi kết quả định lượng MAE/RMSE đã được công bố trên tập kiểm thử.
    - Đảm bảo mã nguồn notebook thực thi hoàn toàn bằng NumPy/SciPy/Matplotlib thuần, không phát sinh lỗi khi chạy toàn bộ notebook.
  </invariants>

  <acceptance_criteria>
    - [x] AC-1: Bổ sung code hiển thị bảng thống kê trung gian chi tiết các thông số (N_sil, N_sp, mean_sil, std_sil, mean_sp, std_sp, T_file) cho từng file và pooled toàn bộ tập huấn luyện.
    - [x] AC-2: Bổ sung biểu đồ kép phân bố Gauss (Linear Zoom và Log-Y Full range) thể hiện rõ ràng các hàm mật độ PDF của Silence & Speech, vị trí ngưỡng T*, và vùng nhầm lẫn (Area of Confusion).
    - [x] AC-3: Xuất file hình ảnh chất lượng cao vào reports/figures/figure_gaussian_threshold_analysis.png.
    - [x] AC-4: Toàn bộ notebook gauss.ipynb thực thi thành công từ đầu đến cuối không lỗi (Zero errors).
  </acceptance_criteria>

  <definition_of_ready>
    - [x] Intent and acceptance criteria are clear without assumptions.
    - [x] Allowed files in Section 2 are identified.
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
    - DO NOT refactor unrelated code in binary.ipynb or histogram.ipynb.
    - DO NOT alter existing test set evaluation results in gauss.ipynb.
    - DO NOT install new external dependencies outside requirements.txt.
  </negative_constraints>
</scope_contract>

---

## 3. Execution Plan (Compact Slices)

<execution_plan>
  <living_scratchpad>
    - **Completed:** Slice 1 (Thống kê trung gian + biểu đồ Gauss tìm ngưỡng), Slice 2 (Thực thi toàn bộ notebook gauss.ipynb), Slice 3 (Vá lỗi logic hậu xử lý: trailing silence trong filter_short_silence, tính chẵn lẻ phân đoạn trong extract_boundaries, và thuật toán ghép cặp Bipartite 1-to-1 matching trong match_boundaries).
    - **Current:** Hoàn thành, sẵn sàng báo cáo cho người dùng.
    - **Blockers:** Không có.
    - **Next Steps:** Báo cáo chi tiết nguyên nhân, giải pháp và kết quả định lượng cho người dùng.
  </living_scratchpad>

  ### Slice 1: Thêm Cell Thống kê & Vẽ Biểu đồ Gauss Tìm Ngưỡng trong gauss.ipynb
  - **Action:** Cập nhật gauss.ipynb bổ sung Cell trực quan hóa và bảng số liệu trung gian ngay sau Cell 7, lưu file ảnh `figure_gaussian_threshold_analysis.png`.
  - **Verifier:** Chạy kiểm thử notebook bằng Python kernel để xác nhận tạo ra hình ảnh và bảng in chính xác.
  - **Status:** [x] DONE

  ### Slice 2: Chạy toàn bộ Notebook gauss.ipynb và Kiểm tra Kết quả
  - **Action:** Thực thi toàn bộ notebook `gauss.ipynb`, lưu lại outputs đầy đủ vào file .ipynb.
  - **Verifier:** Kiểm tra file ảnh đã xuất hiện trong reports/figures/ và các cell outputs hiển thị trọn vẹn.
  - **Status:** [x] DONE

  ### Slice 3: Vá Lỗi Logic Hậu Xử Lý (filter_short_silence, extract_boundaries, match_boundaries)
  - **Action:** Sửa lỗi gộp trailing silence ở cuối file, chuẩn hóa quy tắc đóng/mở biên chẵn cặp, nâng cấp giải thuật ghép cặp 1-1 Bipartite Matching kèm báo cáo False Alarms / Missed.
  - **Verifier:** Chạy lại toàn bộ `gauss.ipynb`, xác nhận MAE bảo toàn 21.2470 ms, số biên luôn chẵn và hiển thị minh bạch các xung nhiễu giả.
  - **Status:** [x] DONE
</execution_plan>

---

## 4. Consolidated Verification & Gates

<verification_gates>
  <!-- Gate G1/G2: Scope & Architecture check (pre-execution) -->
  - [x] **Gate G1/G2 (Plan Approved):** Allowed files confirmed, test verifiers defined.

  <!-- Gate G3: Verification evidence (post-execution) -->
  - [x] **Gate G3 (Ready for Handoff):**
    - [x] Verifier commands executed cleanly (Zero errors).
    - [x] Git diff inspected — NO files touched outside `<allowed_files>`.
    - [x] Edge-case self-check verified.
    - [x] No temporary debug logs or unintended changes.
</verification_gates>

</task_lite>
