# Task Lite: TASK-EXPAND-15SLIDES Mở Rộng Bộ Slide Thuyết Trình Lên 15 Slide

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
  <owner>@antigravity</owner>
</task_control>

---

## 1. Intent & Specification

<specification>
  <goal>
    Mở rộng bộ slide thuyết trình từ 10 slide lên 15 slide hoàn chỉnh, kế thừa toàn diện phong cách nhận diện Tech-HUD (Cyan/Orange/Slate/White) từ template `Digital vs. Analog Reliable Signal Science Presentation.pdf`, tuân thủ 100% quy tắc của giảng viên (<= 7 dòng/slide, <= 10 từ/dòng, font >= 18pt), bao phủ chi tiết cả 3 thuật toán (Binary Search, Histogram log(STE), Gaussian Bayes), phân tích chuyên sâu dữ liệu kiểm thử theo từng môi trường Studio và Phone, biểu đồ định lượng và hướng mở rộng ZCR.
  </goal>

  <invariants>
    - Tuân thủ quy định giảng viên: font >= 18pt, <= 7 dòng/slide, <= 10 từ/dòng, màu chữ tương phản cao trên nền sáng.
    - Giữ nguyên cấu trúc dữ liệu và kết quả trong 3 notebook gốc (`binary.ipynb`, `histogram.ipynb`, `simple_statistics.ipynb`).
    - Dữ liệu kiểm thử bao phủ toàn bộ 4 file: `phone_F2`, `phone_M2`, `studio_F2`, `studio_M2`.
    - Sinh đầy đủ cả 2 định dạng: `presentation_speech_silence.pptx` và `presentation_speech_silence.pdf`.
    - Đi kèm Speaker Notes chi tiết cho từng slide.
  </invariants>

  <acceptance_criteria>
    - [x] AC-1: Xác định cấu trúc 15 slide logic, khoa học, phân bố đều thông tin kỹ thuật và thực nghiệm.
    - [x] AC-2: Bổ sung các đồ thị chuyên biệt chất lượng cao 300 DPI phục vụ các slide mới (đặc trưng STE vs log(STE), phân tích riêng môi trường Studio vs Phone, minh họa cơ chế ngưỡng kép ZCR).
    - [x] AC-3: Cập nhật script `scripts/generate_deck.js` để sinh 15 slide PowerPoint chuẩn Tech-HUD và kèm Speaker Notes.
    - [x] AC-4: Cập nhật script `scripts/export_presentation_pdf.py` để xuất file PDF 15 trang chuẩn vector 16:9.
    - [x] AC-5: Thực hiện Visual QA trên toàn bộ 15 slide qua `pdftoppm` đảm bảo 100% không tràn viền, font >= 18pt, số dòng <= 7.
  </acceptance_criteria>

  <!-- Definition-of-Ready (DoR): Do not begin coding if problem or allowed files are vague -->
  <definition_of_ready>
    - [x] Mục tiêu mở rộng 15 slide được làm rõ.
    - [x] Cấu trúc 15 slide và các file can thiệp được định vị chính xác.
  </definition_of_ready>
</specification>

---

## 2. Scope Contract & File Whitelist

<scope_contract>
  <allowed_files>
    <file>scripts/export_presentation_assets.py</file>
    <file>scripts/generate_deck.js</file>
    <file>scripts/export_presentation_pdf.py</file>
    <file>assets/presentation/*</file>
    <file>presentation_speech_silence.pptx</file>
    <file>presentation_speech_silence.pdf</file>
    <file>slide_qa/*</file>
    <file>process/general-plans/active/expand-to-15-slides/task-lite.md</file>
  </allowed_files>

  <forbidden_files>
    <file>binary.ipynb</file>
    <file>histogram.ipynb</file>
    <file>simple_statistics.ipynb</file>
    <file>data/*</file>
    <file>docs/assignments/*</file>
  </forbidden_files>

  <negative_constraints>
    - KHÔNG sửa đổi các notebook gốc hoặc dữ liệu nhãn ground truth.
    - KHÔNG dùng phông chữ lạ gây lỗi tiếng Việt hoặc kích thước chữ dưới 18pt.
    - KHÔNG vượt quá 7 dòng hoặc 10 từ/dòng trên bất kỳ slide nào.
  </negative_constraints>
</scope_contract>

---

## 3. Detailed 15-Slide Architecture

<architecture_15_slides>
  1. **Slide 1: Trang tiêu đề (Cover Title)** — Tên đề tài, GVHD, Thành viên nhóm, Ngày báo cáo.
  2. **Slide 2: Tổng quan bài toán & Thách thức (Problem Statement & Challenges)** — Định nghĩa VAD, môi trường Studio vs Phone, âm vô thanh.
  3. **Slide 3: Sơ đồ khối Pipeline 5 bước (Overall Pipeline Flowchart)** — Chuẩn hóa -> Hamming Framing -> Feature Extraction -> Thresholding -> Post-processing.
  4. **Slide 4: Đặc trưng STE tuyến tính vs Phi tuyến log(STE) (Feature Extraction Analysis)** — So sánh không gian năng lượng, ưu thế tách biệt của log(STE).
  5. **Slide 5: Thuật toán 1: Tìm kiếm nhị phân (TT1 Binary Search)** — Ý tưởng tìm kiếm, hàm tối ưu sai số, 12 vòng lặp, ngưỡng T = 0.000798.
  6. **Slide 6: Thuật toán 2: Phân tích Histogram log(STE) (TT2 Histogram Analysis)** — Phát hiện 2 đỉnh cực đại, cực tiểu giữa 2 đỉnh, trọng số W = 2.0, ngưỡng T = -2.4375.
  7. **Slide 7: Thuật toán 3: Phân phối chuẩn Gaussian Bayes (TT3 Gaussian Classifier)** — Mô hình hóa xác suất 2 lớp, chuẩn tối ưu Bayes, ngưỡng T = 0.000792.
  8. **Slide 8: Tổng hợp ngưỡng toàn cục trên tập Huấn luyện (Training Summary & Optimal Thresholds)** — Bảng so sánh 3 ngưỡng T, độ hội tụ trên 4 file huấn luyện.
  9. **Slide 9: Kết quả thực nghiệm TT1 (Binary Search) trên 4 file kiểm thử** — Waveform, STE, F0, biên chuẩn đỏ vs biên thuật toán xanh, MAE/RMSE.
  10. **Slide 10: Kết quả thực nghiệm TT2 (Histogram log(STE)) trên 4 file kiểm thử** — Waveform, log(STE), F0, biên chuẩn đỏ vs biên thuật toán xanh, MAE/RMSE.
  11. **Slide 11: Kết quả thực nghiệm TT3 (Gaussian Bayes) trên 4 file kiểm thử** — Waveform, STE, F0, biên chuẩn đỏ vs biên thuật toán xanh, MAE/RMSE.
  12. **Slide 12: Đánh giá môi trường Studio (Studio Environment: High SNR)** — Phân tích chi tiết 2 file studio_F2 (49.3 dB) và studio_M2 (37.7 dB), sai số cực thấp 2.49 - 12.49 ms.
  13. **Slide 13: Đánh giá môi trường Phone (Phone Environment: Noise Robustness)** — Phân tích chi tiết 2 file phone_F2 (24.8 dB) và phone_M2 (27.0 dB), chứng minh TT2 kháng nhiễu vượt trội.
  14. **Slide 14: Bảng so sánh định lượng toàn diện & Biểu đồ SNR (Quantitative Benchmarks)** — Bảng so sánh đầy đủ MAE, RMSE theo Studio, Phone, Toàn bộ và biểu đồ cột.
  15. **Slide 15: Kết luận & Hướng mở rộng ngưỡng kép ZCR (Conclusion & Dual-Threshold Outlook)** — Đánh giá giải pháp tối ưu, giải thích sai số âm vô thanh và cơ chế kết hợp Zero Crossing Rate (ZCR).
</architecture_15_slides>

---

## 4. Execution Plan (Compact Slices)

<execution_plan>
  <living_scratchpad>
    - **Completed:** Slice 1 (13 hình ảnh đồ thị 300 DPI), Slice 2 (15 slide PPTX 3.5MB), Slice 3 (15 trang PDF 3.4MB & Visual QA)
    - **Current:** Hoàn thành toàn bộ
    - **Blockers:** Không có
    - **Next Steps:** Bàn giao bộ slide cho người dùng
  </living_scratchpad>

  ### Slice 1: Mở rộng bộ hình ảnh đồ thị chuyên biệt trong `scripts/export_presentation_assets.py`
  - **Action:** Thêm các đồ thị mới:
    * `fig_ste_vs_logste.png` (So sánh STE vs log(STE))
    * `fig_training_summary.png` (Tổng hợp ngưỡng và phân bố trên tập huấn luyện)
    * `fig_studio_deepdive.png` (Phân tích phóng to môi trường Studio F2 & M2)
    * `fig_phone_deepdive.png` (Phân tích phóng to môi trường Phone F2 & M2)
    * `fig_zcr_concept.png` (Minh họa cơ chế ngưỡng kép STE + ZCR)
  - **Verifier:** `.venv/bin/python scripts/export_presentation_assets.py && ls -la assets/presentation/`
  - **Status:** [x] DONE

  ### Slice 2: Cập nhật `scripts/generate_deck.js` để sinh 15 slide chuẩn Tech-HUD
  - **Action:** Lập trình cấu trúc 15 slide hoàn chỉnh, gắn layout và hình vẽ tương ứng, soạn Speaker Notes cho 15 slide.
  - **Verifier:** `node scripts/generate_deck.js && ls -lh presentation_speech_silence.pptx`
  - **Status:** [x] DONE

  ### Slice 3: Cập nhật `scripts/export_presentation_pdf.py` và Visual QA 15 slide
  - **Action:** Xuất file PDF 15 slide và render ảnh PNG kiểm tra chất lượng hiển thị qua `pdftoppm`.
  - **Verifier:** `.venv/bin/python scripts/export_presentation_pdf.py && pdftoppm -png -r 150 presentation_speech_silence.pdf slide_qa/slide_15 && ls slide_qa/slide_15-*.png | wc -l`
  - **Status:** [x] DONE
</execution_plan>

---

## 5. Consolidated Verification & Gates

<verification_gates>
  - [x] **Gate G1/G2 (Plan Approved):** Allowed files confirmed, test verifiers defined, 15-slide architecture established.
  - [x] **Gate G3 (Ready for Handoff):**
    - [x] 15 slides generated in both .pptx (3.5MB) and .pdf (3.4MB).
    - [x] 100% Visual QA passed (no overflow, font >= 18pt, <= 7 lines).
    - [x] All 4 test files and 3 algorithms covered rigorously.
</verification_gates>

</task_lite>
