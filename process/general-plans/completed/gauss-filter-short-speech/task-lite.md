# Task Lite: GAUSS-SHORT-SPEECH-01 Mở Rộng Trực Quan Hóa Xung Nhiễu & Bổ Sung Lọc Tiếng Nói Ngắn (filter_short_speech)

<task_lite version="3.0" framework="RIPER-5-Lite">

<!-- ════════════════════════════════════════════
     SECTION 0 — TASK CONTROL
     ════════════════════════════════════════════ -->
<task_control>
  <track>LITE</track>
  <status>COMPLETED</status>
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
    Mở rộng Cell 14 (exec 45/46) trong notebook gauss.ipynb để trực quan hóa phóng to cận cảnh (zoom-in) các đoạn xung nhiễu ngắn (10ms tại t ≈ 0.10s ở phone_M2 và 20ms tại t ≈ 0.62s ở phone_F2) làm nổi bật cặp vạch biên giả khi chưa lọc tiếng nói ngắn. Đồng thời thêm Markdown và Code Cell mới cài đặt cơ chế `filter_short_speech(min_speech_ms=30.0)` theo cơ sở lý thuyết Rabiner & Sambur (1975), in bảng đối chiếu MAE/RMSE trước vs sau khi lọc và trực quan hóa 4 đồ thị sạch nhiễu.
  </goal>

  <invariants>
    - Giữ nguyên các hàm cốt lõi, tham số framing (25ms/10ms), ngưỡng tối ưu T_gaussian = 0.000791.
    - Không sửa đổi mã nguồn các notebook khác (binary.ipynb, histogram.ipynb).
    - Giữ code thuần khiết NumPy / Matplotlib, không phụ thuộc thư viện ngoài scipy.stats.
    - Đảm bảo notebook gauss.ipynb thực thi thành công từ đầu đến cuối không lỗi (Zero errors).
  </invariants>

  <acceptance_criteria>
    - [x] AC-1: Mở rộng Cell 14 (exec 45/46) bổ sung góc nhìn phóng to cận cảnh (Zoom-in Inset / Subplot) cho các tín hiệu có xung nhiễu ngắn (phone_F2 và phone_M2), hiển thị rõ cặp biên giả chỉ cách nhau 10-20ms.
    - [x] AC-2: Thêm Markdown giới thiệu cơ sở âm học Rabiner & Sambur (1975) / ITU-T G.729 và Code Cell mới định nghĩa `filter_short_speech(min_speech_ms=30.0)`.
    - [x] AC-3: Trong Cell mới, in bảng đối chiếu định lượng (Số biên khớp, MAE, RMSE) Trước vs Sau khi lọc short speech cho cả 4 file test.
    - [x] AC-4: Trong Cell mới, trực quan hóa 4 đồ thị phân đoạn sau khi đã lọc sạch short speech, xác nhận triệt tiêu hoàn toàn các vạch biên ảo.
    - [x] AC-5: Toàn bộ notebook gauss.ipynb thực thi thành công và lưu đầy đủ outputs/figures.
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
  </allowed_files>

  <forbidden_files>
    <file>/home/phuqy/Documents/main_gk/binary.ipynb</file>
    <file>/home/phuqy/Documents/main_gk/histogram.ipynb</file>
    <file>/home/phuqy/Documents/main_gk/data/**</file>
  </forbidden_files>

  <negative_constraints>
    - DO NOT edit binary.ipynb or histogram.ipynb.
    - DO NOT alter data files in data/.
    - DO NOT use replace_file_content on .ipynb files (use python script via run_command).
  </negative_constraints>
</scope_contract>

---

## 3. Execution Plan (Compact Slices)

<execution_plan>
  <living_scratchpad>
    - **Completed:** Slice 1 (Mở rộng Cell 14 với subplot cận cảnh xung nhiễu 3 tầng), Slice 2 (Thêm Markdown 5 & Code Cell filter_short_speech kèm bảng đối chiếu và 4 đồ thị sạch nhiễu), Slice 3 (Thực thi thành công toàn bộ 17 cells của notebook gauss.ipynb).
    - **Current:** Hoàn tất, sẵn sàng báo cáo cho người dùng.
    - **Blockers:** Không có.
    - **Next Steps:** Báo cáo chi tiết cho người dùng và lưu trữ hồ sơ hoàn thành.
  </living_scratchpad>

  ### Slice 1: Mở rộng Cell 14 (exec 45/46) với Subplot Phóng To Cận Cảnh Xung Nhiễu
  - **Action:** Cập nhật Cell 14 để với các file có xung nhiễu (phone_M2 tại t ≈ 0.10s và phone_F2 tại t ≈ 0.62s), vẽ thêm subplot zoom cận cảnh (3 panels: Toàn cảnh waveform, Toàn cảnh STE + F0, và Cận cảnh xung nhiễu phóng to biên độ + STE).
  - **Verifier:** Kiểm tra code chạy không lỗi và sinh đồ thị đẹp mắt.
  - **Status:** [x] DONE

  ### Slice 2: Thêm Cell Mới với Cơ Chế `filter_short_speech` & Đánh Giá Đối Chiếu
  - **Action:** Thêm Markdown Mục 5 (Cơ sở lý thuyết loại bỏ tiếng nói ngắn) và Code Cell mới định nghĩa `filter_short_speech(min_speech_ms=30.0)`, chạy đánh giá, in bảng đối chiếu Trước vs Sau khi lọc, và vẽ 4 đồ thị sạch nhiễu.
  - **Verifier:** Chạy thực thi notebook, kiểm tra kết quả bảng số liệu và 4 đồ thị mới.
  - **Status:** [x] DONE

  ### Slice 3: Thực Thi Toàn Bộ Notebook gauss.ipynb & Kiểm Tra Đầy Đủ Outputs
  - **Action:** Chạy toàn bộ notebook gauss.ipynb bằng python kernel, lưu lại outputs vào file .ipynb.
  - **Verifier:** Toàn bộ cells có outputs hợp lệ, zero errors.
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
