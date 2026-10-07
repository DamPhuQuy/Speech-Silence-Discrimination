# Task: FEAT-SLIDE-001 Speech/Silence Discrimination Presentation Deck

<task_spec version="3.0" framework="RIPER-5">

<!-- ════════════════════════════════════════════
     SECTION 0 — TASK CONTROL (master state record)
     ════════════════════════════════════════════ -->
<task_control>
  <status>COMPLETED</status>
  <spec_level>S1</spec_level>
  <priority>P1</priority>
  <risk>MEDIUM</risk>
  <estimated_story_points>5</estimated_story_points>
  <working_mode>PAIR</working_mode>
  <observability_mode>OFF</observability_mode>
  <current_phase>REVIEW</current_phase>
  <owner>@antigravity</owner>
  <decision_owner>@engineer</decision_owner>
  <created>2026-10-07</created>
  <last_updated>2026-10-07</last_updated>
</task_control>

---

## 1. Specification (Pillar 1: Task / Spec)

<specification>
  <goal>
    Thiết kế và tạo bộ slide thuyết trình chuyên nghiệp (file .pptx và file .pdf xuất kèm) báo cáo bài thi giữa kỳ môn Xử lý tín hiệu số: "Phân đoạn tín hiệu tiếng nói và khoảng lặng (Speech / Silence Discrimination)", kế thừa phong cách thiết kế từ file mẫu `Digital vs. Analog Reliable Signal Science Presentation.pdf`, tích hợp toàn bộ dữ liệu thực nghiệm, đồ thị chất lượng cao và số liệu định lượng (MAE, RMSE, SNR) từ 3 notebook thuật toán (`binary.ipynb`, `histogram.ipynb`, `simple_statistics.ipynb`), đồng thời tuân thủ 100% các tiêu chí khắt khe trong `docs/assignments/`.
  </goal>

  <current_behavior>
    Hiện tại nhóm đã có 3 notebook chạy hoàn chỉnh với đầy đủ kết quả thực nghiệm, hình vẽ và bảng số liệu định lượng trên tập Huấn luyện (`TinHieuHuanLuyen`) và tập Kiểm thử (`TinHieuKiemThu`), file PDF hướng dẫn làm slide/nộp bài, và file mẫu slide định dạng PDF (`Digital vs. Analog Reliable Signal Science Presentation.pdf`). Tuy nhiên chưa có file slide thuyết trình (.pptx/.pdf) được dựng theo chuẩn quy định.
  </current_behavior>

  <expected_behavior>
    Xuất ra file slide trình chiếu `presentation_speech_silence.pptx` và bản PDF tương ứng `presentation_speech_silence.pdf` đạt chuẩn:
    1. Kế thừa visual identity của template mẫu: tỷ lệ 16:9, bảng màu Cyan/Electric Blue (#00A8FF) + Vibrant Orange (#F58220) + White Canvas (#FFFFFF) + Dark Slate (#0F172A), khung viền công nghệ Tech-HUD hiện đại.
    2. Quy tắc nội dung theo hướng dẫn GV: <= 10 từ/hàng, <= 7 hàng/slide, cỡ chữ >= 18pt, độ tương phản cao, hình vẽ và số liệu to rõ ràng, tập trung vào sơ đồ thuật toán, giải pháp lõi, kết quả đồ thị và bình luận kết quả, không dài dòng lý thuyết.
    3. Bao phủ đầy đủ 3 thuật toán:
       - TT1: Binary Search Threshold (Hodgkinson 2012)
       - TT2: Histogram Analysis (Giannakopoulos 2014)
       - TT3: Simple Statistics / Gaussian Distribution (Bayes)
    4. Trực quan hóa kết quả thực nghiệm trên toàn bộ 4 file kiểm thử (`phone_F2`, `phone_M2`, `studio_F2`, `studio_M2`): dạng sóng với biên chuẩn vs biên tìm được, hàm đặc trưng STE/log(STE), đường tần số cơ bản F0, bảng so sánh sai số MAE/RMSE theo từng môi trường Phone / Studio và Toàn bộ.
    5. Đánh giá chuyên sâu ảnh hưởng của nhiễu môi trường (SNR) và đề xuất hướng mở rộng ngưỡng kép STE + ZCR cho âm vô thanh.
  </expected_behavior>

  <actor_authorization>
    Sinh viên / Nhóm thực hiện báo cáo thi giữa kỳ môn Xử lý tín hiệu số (XLTHS 2026).
  </actor_authorization>

  <invariants>
    - Quy tắc slide của giảng viên: <= 10 từ/dòng, <= 7 dòng/slide, font >= 18pt.
    - Màu chữ tương phản rõ rệt với nền (nền trắng/sáng, chữ đen/xanh đậm, highlight màu cam/cyan).
    - Trình bày kết quả trên tất cả 4 file trong thư mục TinHieuKiemThu (không dùng file khác).
    - Các hình vẽ minh họa phải có đầy đủ: dạng sóng, hàm đặc trưng, biên chuẩn (đỏ), biên thuật toán (xanh), đường F0.
    - Số liệu định lượng MAE, RMSE tính bằng đơn vị miliseconds (ms), SNR tính bằng dB.
    - Không sửa đổi mã nguồn hoặc phá vỡ cấu trúc của các notebook `.ipynb` hiện có.
  </invariants>

  <out_of_scope>
    - Không viết lại lý thuyết toán học cơ bản / sách giáo khoa quá dài dòng (giảng viên cấm trình bày lý thuyết suông).
    - Không can thiệp sửa đổi các file audio mẫu và file groundtruth `.lab`.
  </out_of_scope>

  <acceptance_criteria>
    - [x] AC-1: Khảo sát và tổng hợp toàn bộ tri thức từ 3 notebook, tài liệu hướng dẫn và template PDF vào `research.md`.
    - [x] AC-2: Hoàn thành phương án thiết kế kiến trúc slide và cấu trúc deck trong `decision.md`.
    - [x] AC-3: Lập kế hoạch phân rã thực thi chi tiết (slices) trong `plan.md`.
    - [x] AC-4: Tạo script sinh slide tự động (pptxgenjs) trích xuất đồ thị độ phân giải cao và dựng layout chuẩn template.
    - [x] AC-5: Xuất thành công file `presentation_speech_silence.pptx` và `presentation_speech_silence.pdf`.
    - [x] AC-6: Đạt 100% tiêu chí QA: Font >= 18pt, <= 7 dòng/slide, <= 10 từ/dòng, không tràn chữ, hình vẽ sắc nét, đầy đủ 4 file kiểm thử.
  </acceptance_criteria>

  <definition_of_ready>
    - [x] Mục tiêu và tiêu chí chấp nhận được định nghĩa cụ thể, có thể kiểm chứng.
    - [x] Ranh giới bất biến và out-of-scope được xác định rõ ràng.
    - [x] Nguồn dữ liệu kiểm thử và kết quả thuật toán đã có sẵn trong notebook.
  </definition_of_ready>
</specification>

---

## 2. Context Boundaries (Pillar 2: Context)

<context_boundaries>
  <target_files>
    - `scripts/generate_deck.js` — Script tạo file PowerPoint sử dụng thư viện `pptxgenjs`
    - `scripts/extract_figures.py` — Script trích xuất và chuẩn hóa hình ảnh đồ thị từ notebook/matplotlib
    - `presentation_speech_silence.pptx` — File bài thuyết trình PowerPoint hoàn thiện
    - `presentation_speech_silence.pdf` — File PDF của bài thuyết trình phục vụ nộp bài thi
  </target_files>

  <context_groups>
    - `docs/assignments/Hướng dẫn trình bày slide và nộp bài thi.pdf`
    - `docs/assignments/Hướng dẫn BT thi GK nhóm 3-4 SV_Phân đoạn tín hiệu thành tiếng nói và khoảng lặng_XLTHS_GK 2026.docx`
    - `docs/assignments/Hướng dẫn BT - Phân đoạn tín hiệu thành tiếng nói và khoảng lặng_XLTHS_GK 2026.docx`
    - `Digital vs. Analog Reliable Signal Science Presentation.pdf`
    - `binary.ipynb`
    - `histogram.ipynb`
    - `simple_statistics.ipynb`
  </context_groups>

  <source_of_truth>
    <requirement>docs/assignments/Hướng dẫn trình bày slide và nộp bài thi.pdf</requirement>
    <architecture>.agents/SKILL.md</architecture>
    <existing_behavior>binary.ipynb, histogram.ipynb, simple_statistics.ipynb</existing_behavior>
    <tests>MAE, RMSE and SNR metrics calculated across 4 test signals</tests>
  </source_of_truth>
</context_boundaries>

---

## 3. Verification Strategy

<verification_strategy>

| AC / Risk | Evidence required | Verifier |
|---|---|---|
| AC-1: Research | `research.md` hoàn thành với bảng thông số đầy đủ | Kiểm tra Gate G0 |
| AC-2: Innovate | `decision.md` chốt layout, palette, và cấu trúc slide | Kiểm tra Gate G1 |
| AC-3: Plan | `plan.md` liệt kê các lát cắt (slices) rõ ràng | Kiểm tra Gate G2 |
| AC-4 & AC-5: File sinh ra | File `.pptx` và `.pdf` được tạo ra không lỗi | `soffice --headless --convert-to pdf` & kiểm tra dung lượng |
| AC-6: Slide QA | Quy tắc <= 7 dòng, font >= 18pt, không tràn chữ | Trích xuất ảnh từng slide bằng `pdftoppm` và visual QA |

</verification_strategy>

---

## 4. Decisions

<decisions>
  <approved_decisions>
    <!-- Ghi nhận sau khi chốt ở phase Innovate -->
  </approved_decisions>

  <open_decisions>
    <!-- Câu hỏi thiết kế mở -->
  </open_decisions>
</decisions>

---

## 5. RIPER-5 Execution Plan (Pillar 4: Loop)

<execution_plan>
  <phase name="Research" order="1">
    - [x] Ingest task spec, domain invariants, and out-of-scope boundaries.
    - [x] Đọc và đối chiếu yêu cầu môn học trong docs/assignments.
    - [x] Phân tích thiết kế của template slide mẫu (màu sắc, tỷ lệ, hình khối, typography).
    - [x] Trích xuất toàn bộ dữ liệu, thông số ngưỡng, MAE/RMSE và đồ thị từ 3 notebook.
    - [x] Tạo file `research.md` đầy đủ bằng chứng thực nghiệm.
    <gate id="G0" label="Research Complete">
      - [x] Dữ liệu 3 thuật toán và 4 file test được trích xuất chính xác.
      - [x] Quy tắc slide (font >= 18pt, <= 7 dòng, <= 10 từ/dòng) được mô hình hóa.
      - [x] Sơ đồ khối pipeline và thuật toán được thiết kế.
    </gate>
  </phase>

  <phase name="Innovate" order="2">
    - [x] Lựa chọn giải pháp kỹ thuật tạo deck (pptxgenjs kết hợp asset pipeline).
    - [x] Xác định cấu trúc slide chi tiết (khoảng 10-12 slide đáp ứng 3 phút trình bày).
    - [x] Lập ma trận đánh giá Pugh Trade-off Matrix.
    - [x] Tạo file `decision.md` (Gate G1).
    <gate id="G1" label="Gate 1 — Decision Approved">
      - [x] Options reviewed and trade-offs analyzed.
      - [x] Selected option recorded in `decision.md`.
      - [x] No blocking business/schema/security decision remains open.
      <approved_by>@engineer</approved_by>
      <approved_date>2026-10-07</approved_date>
    </gate>
  </phase>

  <phase name="Plan" order="3">
    - [x] Phân rã công việc thành các lát cắt nhỏ (Slices).
    - [x] Thiết lập Scope Contract (Allowed Files / Forbidden Files).
    - [x] Tạo file `plan.md` (Gate G2).
    <gate id="G2" label="Gate 2 — Plan Approved">
      - [x] Every slice has a verifier.
      - [x] Allowed/forbidden file scope is defined.
      - [x] Rollback point defined per slice.
      - [x] Stop conditions defined.
      - [x] Plan approved.
      <approved_by>@engineer</approved_by>
      <approved_date>2026-10-07</approved_date>
    </gate>
  </phase>

  <phase name="Execute" order="4">
    - [x] Triển khai script trích xuất hình ảnh đồ thị sắc nét từ notebook.
    - [x] Triển khai script sinh slide pptxgenjs với theme chuẩn template.
    - [x] Render file `.pptx` và chuyển đổi sang `.pdf`.
    - [x] Cập nhật `state.md`.
  </phase>

  <phase name="Review" order="5">
    - [x] Kiểm tra visual QA từng slide qua ảnh PNG (pdftoppm).
    - [x] Kiểm tra nội dung text, quy tắc font chữ, không tràn lề.
    - [x] Tạo file `review.md` và `handoff.md` (Gate G3).
  </phase>
</execution_plan>

---

## 6. Guardrails & Escalation (Pillar 3 & 4: Harness)

<guardrails>
  <stop_conditions>
    - Không tự ý sửa đổi code gốc trong các notebook .ipynb mà làm thay đổi kết quả thuật toán.
    - Không dùng các font chữ không hỗ trợ tiếng Việt gây lỗi hiển thị dấu tiếng Việt.
    - Dừng lại xin ý kiến người dùng khi hoàn thành mỗi Gate trong chế độ PAIR.
  </stop_conditions>

  <retry_budget max_attempts="3">
    Tối đa 3 lần thử nghiệm sinh slide nếu phát hiện lỗi format hoặc lỗi chuyển đổi PDF.
  </retry_budget>
</guardrails>

</task_spec>
