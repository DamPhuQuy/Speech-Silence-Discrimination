# Plan: PLAN-001 Speech/Silence Discrimination Presentation Deck

<execution_plan task_id="FEAT-SLIDE-001" plan_id="PLAN-001" version="2.0" framework="RIPER-5">

<!-- PLAN PHASE. Plan artifacts only. No source-code changes. -->
<plan_status>
  <phase>PLAN</phase>
  <last_updated>2026-10-07</last_updated>
</plan_status>

---

## 1. Input Artifacts

<input_artifacts>
  <task_spec>process/features/active/speech-silence-presentation/task.md</task_spec>
  <research>process/features/active/speech-silence-presentation/research.md</research>
  <decision>process/features/active/speech-silence-presentation/decision.md (DEC-001, Option B: pptxgenjs + Matplotlib Asset Pipeline)</decision>
</input_artifacts>

---

## 2. Execution Constraints

<execution_constraints>
  <allowed_files>
    - `scripts/export_presentation_assets.py` — Script trích xuất và sinh đồ thị chất lượng cao
    - `scripts/generate_deck.js` — Script Node.js sinh slide thuyết trình PowerPoint
    - `assets/presentation/*` — Thư mục chứa các tài nguyên ảnh đồ thị phục vụ slide
    - `presentation_speech_silence.pptx` — File PowerPoint kết quả
    - `presentation_speech_silence.pdf` — File PDF của slide
    - `slide_qa/*` — Thư mục chứa ảnh phục vụ Visual QA
    - `process/features/active/speech-silence-presentation/state.md` — Trạng thái thực thi
  </allowed_files>
  <forbidden_files>
    - `binary.ipynb`, `histogram.ipynb`, `simple_statistics.ipynb` (Tuyệt đối không can thiệp sửa đổi các notebook gốc)
    - `data/*` (Không sửa đổi các file âm thanh và file nhãn ground truth)
    - `docs/assignments/*` (Không sửa đổi tài liệu đề bài)
  </forbidden_files>
  <allowed_commands>
    - `python3 scripts/export_presentation_assets.py`
    - `node scripts/generate_deck.js`
    - `soffice --headless --convert-to pdf presentation_speech_silence.pptx`
    - `pdftoppm -png -r 150 presentation_speech_silence.pdf slide_qa/slide`
  </allowed_commands>
  <restricted_operations>
    - Không cài đặt thêm các thư viện bên ngoài không cần thiết.
    - Không làm tràn viền chữ hoặc dùng phông chữ không an toàn.
  </restricted_operations>
</execution_constraints>

---

## 3. Slice Summary

<slice_summary>

| ID | Behavior | Boundary | Files | AC | Verifier | Risk | Mode | Rollback |
|---|---|---|---|---|---|---|---|---|
| **S1** | Sinh và chuẩn hóa toàn bộ hình ảnh đồ thị, sơ đồ khối và biểu đồ so sánh SNR | Assets & Plotting | `scripts/export_presentation_assets.py`, `assets/presentation/` | AC-1, AC-4 | `python3 scripts/export_presentation_assets.py` | Thấp | WRITE | Xóa `assets/presentation/` |
| **S2** | Xây dựng 10 slide PowerPoint hoàn chỉnh theo chuẩn Tech-HUD của template và quy tắc GV | PPTX Deck Generation | `scripts/generate_deck.js`, `presentation_speech_silence.pptx` | AC-2, AC-3, AC-5 | `node scripts/generate_deck.js` | Trung bình | WRITE | Xóa script và file pptx |
| **S3** | Biên dịch sang PDF và thực hiện Visual QA toàn diện từng slide | PDF & Visual QA | `presentation_speech_silence.pdf`, `slide_qa/` | AC-6 | `soffice --headless` & `pdftoppm` | Thấp | EXEC | Chạy lại S2 để chỉnh sửa vị trí |

</slice_summary>

---

## 4. Slice Details

<slices>

  <slice id="S1">
    <objective>Tạo bộ hình ảnh trực quan chất lượng cao (300 DPI) cho 10 slide</objective>
    <change>
      Viết script `scripts/export_presentation_assets.py` để trích xuất và tạo 8 file ảnh đồ họa:
      1. `fig_pipeline.png`: Sơ đồ khối pipeline 5 bước.
      2. `fig_tt1_binary_flow.png`: Sơ đồ khối thuật toán tìm kiếm nhị phân.
      3. `fig_tt2_histogram_flow.png`: Sơ đồ khối và phân tích 2 đỉnh Histogram log(STE).
      4. `fig_tt3_gaussian_flow.png`: Sơ đồ khối và phân phối xác suất Gaussian Bayes.
      5. `fig_test_binary_4files.png`: Đồ thị 4 file test (phone_F2, phone_M2, studio_F2, studio_M2) của TT1.
      6. `fig_test_histogram_4files.png`: Đồ thị 4 file test của TT2.
      7. `fig_test_gaussian_4files.png`: Đồ thị 4 file test của TT3.
      8. `fig_snr_comparison.png`: Biểu đồ cột so sánh MAE giữa 3 thuật toán theo môi trường Phone vs Studio.
    </change>
    <allowed_files>
      - `scripts/export_presentation_assets.py`
      - `assets/presentation/`
    </allowed_files>
    <acceptance_criteria>
      - [ ] Toàn bộ 8 file ảnh được tạo ra với kích thước đầy đủ, chữ trên đồ thị to rõ ràng, không bị méo mó.
    </acceptance_criteria>
    <verifier>
      ```bash
      python3 scripts/export_presentation_assets.py && ls -lh assets/presentation/*.png
      ```
    </verifier>
    <expected_evidence>8 file PNG tồn tại với dung lượng > 50KB mỗi file.</expected_evidence>
    <rollback_point>rm -rf assets/presentation/ scripts/export_presentation_assets.py</rollback_point>
  </slice>

  <slice id="S2">
    <objective>Sinh file PowerPoint 10 slide chuẩn Tech-HUD và quy tắc GV bằng pptxgenjs</objective>
    <change>
      Viết script `scripts/generate_deck.js` sử dụng `pptxgenjs` để dựng 10 slide:
      - Thiết lập layout 16:9 (`13.333" x 7.5"`).
      - Palette: Cyan `#00A8FF`, Orange `#F58220`, Slate `#0F172A`, White `#FFFFFF`.
      - Khung HUD bao quanh slide và các thẻ so sánh (Comparison cards).
      - Font chữ: Tiêu đề 32-36pt bold, nội dung >= 18pt bold/regular.
      - Mật độ: <= 7 dòng/slide, <= 10 từ/dòng.
      - Nội dung slide:
        * Slide 1: Cover Title
        * Slide 2: Pipeline 5 bước
        * Slide 3: TT1 Binary Search
        * Slide 4: TT2 Histogram log(STE)
        * Slide 5: TT3 Gaussian Bayes
        * Slide 6: Kết quả TT1 trên 4 file test
        * Slide 7: Kết quả TT2 trên 4 file test
        * Slide 8: Kết quả TT3 trên 4 file test
        * Slide 9: So sánh 3 thuật toán & Đánh giá SNR
        * Slide 10: Kết luận & Hướng mở rộng ZCR
      - Thêm Speaker Notes vào từng slide hỗ trợ trình bày trong 3 phút.
    </change>
    <allowed_files>
      - `scripts/generate_deck.js`
      - `presentation_speech_silence.pptx`
    </allowed_files>
    <acceptance_criteria>
      - [ ] File `presentation_speech_silence.pptx` được tạo thành công, dung lượng hợp lý.
    </acceptance_criteria>
    <verifier>
      ```bash
      node scripts/generate_deck.js && ls -lh presentation_speech_silence.pptx
      ```
    </verifier>
    <expected_evidence>File `presentation_speech_silence.pptx` được ghi thành công.</expected_evidence>
    <rollback_point>rm -f presentation_speech_silence.pptx scripts/generate_deck.js</rollback_point>
  </slice>

  <slice id="S3">
    <objective>Chuyển đổi sang PDF và thực hiện Visual QA toàn diện</objective>
    <change>
      Chuyển đổi file `.pptx` sang `.pdf` bằng LibreOffice, xuất từng trang thành ảnh PNG và kiểm tra trực quan từng slide.
    </change>
    <allowed_files>
      - `presentation_speech_silence.pdf`
      - `slide_qa/`
    </allowed_files>
    <acceptance_criteria>
      - [ ] File `presentation_speech_silence.pdf` được tạo ra không lỗi.
      - [ ] Đủ 10 trang slide sắc nét, không bị tràn dòng, không đè chữ, chữ to rõ ràng >= 18pt.
    </acceptance_criteria>
    <verifier>
      ```bash
      soffice --headless --convert-to pdf presentation_speech_silence.pptx
      mkdir -p slide_qa && pdftoppm -png -r 150 presentation_speech_silence.pdf slide_qa/slide
      ls -lh slide_qa/slide-*.png
      ```
    </verifier>
    <expected_evidence>Xuất đủ 10 file ảnh slide và xác nhận hiển thị hoàn hảo.</expected_evidence>
    <rollback_point>rm -rf slide_qa presentation_speech_silence.pdf</rollback_point>
  </slice>

</slices>

---

## 5. Scope Contract

<scope_contract>
  <allowed>
    - Tạo `scripts/export_presentation_assets.py` và thư mục `assets/presentation/`.
    - Tạo `scripts/generate_deck.js` và file `presentation_speech_silence.pptx`.
    - Tạo file `presentation_speech_silence.pdf` và thư mục kiểm thử `slide_qa/`.
    - Cập nhật các file quy trình trong `process/features/active/speech-silence-presentation/`.
  </allowed>
  <forbidden>
    - Không sửa đổi mã nguồn và kết quả của 3 file notebook (`binary.ipynb`, `histogram.ipynb`, `simple_statistics.ipynb`).
    - Không thay đổi dữ liệu kiểm thử trong `data/`.
  </forbidden>
</scope_contract>

---

## 6. Verification Matrix

<verification_matrix>

| AC / Risk | Test / Command | Expected Evidence | Strictness | Actual Result |
|---|---|---|---|---|
| AC-1: Asset generation | `python3 scripts/export_presentation_assets.py` | 8 file PNG hợp lệ trong `assets/presentation/` | hard-mandatory | Chờ thực thi |
| AC-2: Deck generation | `node scripts/generate_deck.js` | File `.pptx` được tạo | hard-mandatory | Chờ thực thi |
| AC-3: PDF conversion | `soffice --headless --convert-to pdf presentation_speech_silence.pptx` | File `.pdf` được tạo | hard-mandatory | Chờ thực thi |
| AC-4: Slide Rules QA | Kiểm tra trực quan qua ảnh slide (`pdftoppm`) | $\le 7$ dòng, font $\ge 18$pt, không đè chữ | hard-mandatory | Chờ thực thi |

</verification_matrix>

---

## Gate 2 — Plan Approved

<gate id="G2">
  - [x] Every slice has a defined verifier.
  - [x] Scope contract (allowed / forbidden) approved.
  - [x] Enforcement strictness assigned per AC/verification item.
  - [x] Stop conditions defined per slice.
  - [x] Rollback point defined per slice.
  - [x] Allowed commands listed.
  - [x] Plan approved.
  <approved_by>@engineer</approved_by>
  <approved_date>2026-10-07</approved_date>
</gate>

</execution_plan>
