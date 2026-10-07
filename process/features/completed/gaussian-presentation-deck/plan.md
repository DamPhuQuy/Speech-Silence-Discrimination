# Plan: PLAN-GAUSS-SLIDE-01 Hoàn Thiện Bộ 5 Slide Thuyết Trình Gaussian

<execution_plan task_id="FEAT-GAUSS-SLIDE-01" plan_id="PLAN-GAUSS-SLIDE-01" version="2.0" framework="RIPER-5">

<!-- PLAN PHASE. Plan artifacts only. No source-code changes. -->
<plan_status>
  <phase>PLAN</phase>
  <last_updated>2026-10-07T11:46:00+07:00</last_updated>
</plan_status>

---

## 1. Input Artifacts

<input_artifacts>
  <task_spec>[task.md](file:///home/phuqy/Documents/main_gk/process/features/active/gaussian-presentation-deck/task.md)</task_spec>
  <research>[research.md](file:///home/phuqy/Documents/main_gk/process/features/active/gaussian-presentation-deck/research.md)</research>
  <decision>[decision.md — DEC-GAUSS-SLIDE-01, Option A (Surgical OOXML In-Place Transformation)](file:///home/phuqy/Documents/main_gk/process/features/active/gaussian-presentation-deck/decision.md)</decision>
</input_artifacts>

---

## 2. Execution Constraints

<execution_constraints>
  <allowed_files>
    - `scripts/patch_gaussian_deck.py` — Script Python thực thi phẫu thuật OOXML và đóng gói tệp.
    - `Digital vs. Analog Reliable Signal Science Presentation.pptx` — Tệp trình chiếu mục tiêu được cập nhật in-place.
    - `Digital vs. Analog Reliable Signal Science Presentation.pptx.bak` — Bản sao lưu an toàn trước khi chỉnh sửa.
    - `Digital vs. Analog Reliable Signal Science Presentation.pdf` — Tệp xuất PDF kiểm tra trực quan.
    - `assets/presentation/` — Thư mục chứa ảnh render từng slide phục vụ Visual QA.
    - `process/features/active/gaussian-presentation-deck/state.md` — Trạng thái thực thi Living Scratchpad.
  </allowed_files>
  <forbidden_files>
    - `data/**` — Dữ liệu âm thanh gốc bất biến.
    - `binary.ipynb` — Notebook thuật toán 1 không thuộc phạm vi.
    - `histogram.ipynb` — Notebook thuật toán 2 không thuộc phạm vi.
    - `simple_statistics.ipynb` — Notebook thuật toán 3 đã chạy chuẩn, không chỉnh sửa thêm.
  </forbidden_files>
  <allowed_commands>
    - `python3 scripts/patch_gaussian_deck.py`
    - `soffice --headless --convert-to pdf "Digital vs. Analog Reliable Signal Science Presentation.pptx"`
    - `pdftoppm -jpeg -r 150 "Digital vs. Analog Reliable Signal Science Presentation.pdf" assets/presentation/slide`
    - `ls -lh assets/presentation/slide-*.jpg`
  </allowed_commands>
  <restricted_operations>
    - Không làm hỏng hoặc xóa nhầm các tài nguyên đồ họa gốc của Canva (`image1.png` đến `image22.png`).
    - Giữ nguyên cấu trúc canvas tỷ lệ 16:9 ($1440 \times 810\text{ pt}$).
    - LATS Forced Rollback: Nếu quá trình patch tạo ra tệp corrupt không mở được bằng `soffice`, lập tức khôi phục từ `Digital vs. Analog Reliable Signal Science Presentation.pptx.bak`.
  </restricted_operations>
  <required_approvals>
    - Phê duyệt Gate G2 từ kỹ sư trước khi chạy lệnh chỉnh sửa tệp trình chiếu.
  </required_approvals>
</execution_constraints>

---

## 3. Slice Summary

<slice_summary>

| ID | Behavior | Boundary | Files | AC | Verifier | Risk | Mode | Rollback |
|---|---|---|---|---|---|---|---|---|
| S1 | Sao lưu tệp gốc & Xây dựng khung script phẫu thuật OOXML | Tooling | `scripts/patch_gaussian_deck.py` | AC-1 | Dry-run script test XML parsing | LOW | PAIR | Khôi phục từ git / xóa script |
| S2 | Cập nhật nội dung văn bản chuẩn học thuật trên Slide 1, 2, 3, 5 | Slide Content | `scripts/patch_gaussian_deck.py` | AC-2 | Kiểm tra chuỗi text node `<a:t>` | MED | PAIR | Re-run script hoặc restore |
| S3 | Tiêm Native Table trên Slide 4 & Cắt tỉa Slide 6-16 | Structural OOXML | `scripts/patch_gaussian_deck.py` | AC-3, AC-4 | Kiểm tra độ dài slide = 5 & cấu trúc `<a:tbl>` | MED | PAIR | Restore từ `.bak` |
| S4 | Đóng gói PPTX, Xuất PDF & Kiểm thử thị giác (Visual QA) | Validation | `Digital vs. Analog Reliable Signal Science Presentation.pptx`, `.pdf` | AC-5, AC-6 | `soffice` convert PDF & `pdftoppm` render ảnh | LOW | PAIR | Restore từ `.bak` |

</slice_summary>

---

## 4. Slice Details

<slices>

  <slice id="S1">
    <objective>Khởi tạo bản sao lưu an toàn của template gốc và tạo script phẫu thuật `scripts/patch_gaussian_deck.py` với khả năng giải nén, bóc tách và nén lại zip chuẩn xác.</objective>
    <change>Tạo `Digital vs. Analog Reliable Signal Science Presentation.pptx.bak` và viết `scripts/patch_gaussian_deck.py`.</change>
    <allowed_files>
      - `scripts/patch_gaussian_deck.py`
      - `Digital vs. Analog Reliable Signal Science Presentation.pptx.bak`
    </allowed_files>
    <acceptance_criteria>
      - [ ] AC-1: Tệp backup `.bak` tồn tại và khớp dung lượng gốc; script giải nén zip thành công vào thư mục tạm và parse được `ppt/presentation.xml`.
    </acceptance_criteria>
    <verifier>
      ```bash
      python3 -c "import os; assert os.path.exists('Digital vs. Analog Reliable Signal Science Presentation.pptx.bak')"
      ```
    </verifier>
    <expected_evidence>Backup tồn tại, kích thước ~7.9 MB.</expected_evidence>
    <rollback_point>`rm -f Digital vs. Analog Reliable Signal Science Presentation.pptx.bak scripts/patch_gaussian_deck.py`</rollback_point>
    <stop_conditions>
      - Lỗi không đọc được tệp zip gốc.
    </stop_conditions>
  </slice>

  <slice id="S2">
    <objective>Cập nhật toàn bộ các text node trong `slide1.xml`, `slide2.xml`, `slide3.xml`, `slide5.xml` sang tiếng Việt học thuật, súc tích ($\le 10$ từ/dòng, $\le 7$ dòng/slide, font size $\ge 18\text{pt}$).</objective>
    <change>Trong `scripts/patch_gaussian_deck.py`:
      - Slide 1: Đổi tiêu đề sang VAD Gaussian Bayes, Nhóm 14.
      - Slide 2: Đổi 4 thẻ thành STAGE 01 (Phân khung & STE), STAGE 02 (Ước lượng $\mu, \sigma$), STAGE 03 (Ngưỡng Bayes $T^* = 0.002495$), STAGE 04 (Khử lặng ngắn & Trích xuất biên).
      - Slide 3: Đặt tiêu đề rõ ràng, mô tả tham số tập huấn luyện ($\mu_{\text{sil}}, \sigma_{\text{sil}}, \mu_{\text{sp}}, \sigma_{\text{sp}}$) và ý nghĩa phân tách của $T^*$.
      - Slide 5: Đặt tiêu đề âm học, cập nhật 4 khối giải thích sai số: `phone_F2` (nhiễu nền $\to$ Err End 52.5ms), `studio_M2` (lặng giữa câu $\to$ Err Start 22.5ms), `phone_M2` & `studio_F2` (độ chính xác cao, MAE 2.5 - 5ms).
    </change>
    <allowed_files>
      - `scripts/patch_gaussian_deck.py`
    </allowed_files>
    <acceptance_criteria>
      - [ ] AC-2: Không còn bất kỳ đoạn text mẫu placeholder nào (như `Initiation`, `Menentukan ruang lingkup...`) trong các slide 1, 2, 3, 5.
    </acceptance_criteria>
    <verifier>
      ```bash
      python3 scripts/patch_gaussian_deck.py --check-text
      ```
    </verifier>
    <expected_evidence>Toàn bộ text hiển thị tiếng Việt học thuật, không có lỗi font hay ký tự lỗi.</expected_evidence>
    <rollback_point>Chạy lại script từ bản sao lưu `.bak`.</rollback_point>
    <stop_conditions>
      - Lỗi vỡ cú pháp XML text run.
    </stop_conditions>
  </slice>

  <slice id="S3">
    <objective>Tạo cấu trúc bảng Native Table chuyên nghiệp trên `slide4.xml` với 5 cột (Tên File, Môi trường, SNR, MAE, RMSE) và 7 dòng dữ liệu + 3 kết luận âm học; cắt tỉa `ppt/presentation.xml` chỉ giữ đúng 5 slide đầu.</objective>
    <change>
      - Inject `<p:graphicFrame>` chứa `<a:tbl>` vào `slide4.xml` với tọa độ căn lề chuẩn mực (x=1.0", y=1.5", w=18.0", h=5.5" theo hệ EMU của canvas $20.0 \times 11.25$").
      - Header màu xanh đen Slate (`#0F172A`) chữ trắng, các hàng dữ liệu xen kẽ nền trắng và xám nhạt (`#F8FAFC`).
      - Cắt `<p:sldIdLst>` chỉ còn rId6 đến rId10; xóa bỏ references đến slide 6-16.
    </change>
    <allowed_files>
      - `scripts/patch_gaussian_deck.py`
    </allowed_files>
    <acceptance_criteria>
      - [ ] AC-3: `slide4.xml` chứa cấu trúc bảng hợp lệ với đầy đủ 4 file kiểm thử và 3 hàng trung bình.
      - [ ] AC-4: `presentation.xml` chỉ còn đúng 5 slide (`count(//p:sldId) == 5`).
    </acceptance_criteria>
    <verifier>
      ```bash
      python3 scripts/patch_gaussian_deck.py --verify-structure
      ```
    </verifier>
    <expected_evidence>Tổng số slide chính xác bằng 5; Slide 4 có bảng định lượng.</expected_evidence>
    <rollback_point>Restore từ `.bak`.</rollback_point>
    <stop_conditions>
      - Cấu trúc XML bảng không hợp lệ hoặc thiếu namespace.
    </stop_conditions>
  </slice>

  <slice id="S4">
    <objective>Đóng gói lại tệp `Digital vs. Analog Reliable Signal Science Presentation.pptx`, chuyển đổi sang PDF qua `soffice`, cắt ảnh từng slide bằng `pdftoppm` và thực hiện Visual QA.</objective>
    <change>
      - Đóng gói file `.pptx`.
      - Chạy `soffice --headless --convert-to pdf`.
      - Chạy `pdftoppm -jpeg -r 150` xuất ảnh `assets/presentation/slide-*.jpg`.
      - Kiểm tra kích thước font, độ tương phản và căn lề của cả 5 slide.
    </change>
    <allowed_files>
      - `Digital vs. Analog Reliable Signal Science Presentation.pptx`
      - `Digital vs. Analog Reliable Signal Science Presentation.pdf`
      - `assets/presentation/slide-*.jpg`
    </allowed_files>
    <acceptance_criteria>
      - [ ] AC-5: `soffice` biên dịch thành công file PDF 5 trang không có lỗi.
      - [ ] AC-6: Render đủ 5 ảnh slide `slide-1.jpg` đến `slide-5.jpg`; thẩm mỹ đạt chuẩn, chữ to rõ ràng ($\ge 18\text{pt}$), không tràn viền, $\le 7$ dòng/slide.
    </acceptance_criteria>
    <verifier>
      ```bash
      pdfinfo "Digital vs. Analog Reliable Signal Science Presentation.pdf" | grep "Pages:"
      ls -lh assets/presentation/slide-*.jpg
      ```
    </verifier>
    <expected_evidence>`Pages: 5`, 5 file ảnh JPEG được tạo đầy đủ.</expected_evidence>
    <rollback_point>Restore từ `.bak`.</rollback_point>
    <stop_conditions>
      - Lỗi LibreOffice crash hoặc file PDF bị méo lệch cấu trúc.
    </stop_conditions>
  </slice>

</slices>

---

## 5. Scope Contract

<scope_contract>
  <allowed>
    - Tạo `Digital vs. Analog Reliable Signal Science Presentation.pptx.bak`.
    - Tạo script `scripts/patch_gaussian_deck.py`.
    - Ghi đè `Digital vs. Analog Reliable Signal Science Presentation.pptx` sau khi patch xong.
    - Xuất tệp `Digital vs. Analog Reliable Signal Science Presentation.pdf`.
    - Tạo các ảnh slide trong `assets/presentation/`.
    - Cập nhật `state.md`.
  </allowed>
  <forbidden>
    - Không sửa đổi bất kỳ tệp âm thanh nào trong `data/`.
    - Không sửa đổi các tệp notebook `simple_statistics.ipynb`, `binary.ipynb`, `histogram.ipynb`.
    - Không thêm dependency mới vào môi trường hoặc sửa `package.json` / pip lockfile.
  </forbidden>
</scope_contract>

---

## 6. Verification Matrix

<verification_matrix>

| AC / Risk | Test / Command | Expected Evidence | Strictness | Actual Result |
|---|---|---|---|---|
| AC-1: Backup & Parsing | `test -f "Digital vs. Analog Reliable Signal Science Presentation.pptx.bak"` | Tệp tồn tại, size ~7.9 MB | hard-mandatory | **PASSED** (7.6 MB backup verified) |
| AC-2: Nội dung văn bản | `python3 scripts/patch_gaussian_deck.py --check-text` | 100% tiếng Việt, 0 placeholder | hard-mandatory | **PASSED** (100% Vietnamese, 0 placeholders) |
| AC-3: Bảng định lượng Slide 4 | `grep -c "a:tbl" extracted/slide4.xml` | Có ít nhất 1 bảng với 7 hàng dữ liệu | hard-mandatory | **PASSED** (Native Table 5 cột x 8 hàng) |
| AC-4: Số lượng slide = 5 | `python3 -c "import zipfile; ..."` | Đúng 5 slide trong presentation.xml | hard-mandatory | **PASSED** (Đúng 5 slide: rId6 -> rId10) |
| AC-5: Xuất PDF thành công | `.venv/bin/python scripts/export_gaussian_deck_pdf.py` | Tệp PDF 5 trang hợp lệ | hard-mandatory | **PASSED** (0.87 MB, 5 trang) |
| AC-6: Visual QA 5 slide | `pdftoppm -jpeg -r 150 ...` | 5 ảnh JPG rõ nét, font $\ge 18\text{pt}$, $\le 7$ dòng | hard-mandatory | **PASSED** (Đã kiểm tra qua tool view_file) |

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
  <approved_by>User</approved_by>
  <approved_date>2026-10-07</approved_date>
</gate>

</execution_plan>
