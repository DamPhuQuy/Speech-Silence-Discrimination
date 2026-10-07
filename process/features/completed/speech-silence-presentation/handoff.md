# Handoff: FEAT-SLIDE-001 Speech/Silence Discrimination Presentation Deck

<handoff task_id="FEAT-SLIDE-001" version="2.0" framework="RIPER-5">

<!-- Final projection. Short. Do not duplicate research/plan/review artifacts. -->
<!-- Answer: What changed? Why? What proves it? What remains risky? -->

<handoff_status>
  <review_decision>PASS</review_decision>
  <review_artifact>[review.md](file:///home/phuqy/Documents/main_gk/process/features/active/speech-silence-presentation/review.md)</review_artifact>
  <completed_date>2026-10-07</completed_date>
</handoff_status>

---

## 1. What Changed

<what_changed>
  Đã hoàn thiện bộ slide thuyết trình báo cáo bài thi giữa kỳ môn Xử lý tín hiệu số (XLTHS 2026) theo đề tài "Phân đoạn tín hiệu tiếng nói và khoảng lặng (Speech / Silence Discrimination)":
  - Sinh thành công 2 file sản phẩm hoàn chỉnh: `presentation_speech_silence.pptx` (2.6 MB) và `presentation_speech_silence.pdf` (2.1 MB).
  - Tích hợp trọn vẹn kết quả thực nghiệm từ 3 notebook thuật toán: TT1 (Binary Search), TT2 (Histogram log(STE)), và TT3 (Gaussian Bayes).
  - Thiết kế đồ họa chuẩn nhận diện Tech-HUD hiện đại (kế thừa từ `Digital vs. Analog Reliable Signal Science Presentation.pdf`) với khung viền công nghệ, màu Cyan `#00A8FF` và Orange `#F58220` trên nền Canvas trắng tương phản cao.
  - Tuân thủ 100% quy định khắt khe của giảng viên: <= 10 từ/dòng, <= 7 dòng/slide, font >= 18pt, thời lượng 3 phút (+1 phút demo), không lý thuyết suông, hình vẽ to rõ kèm biên chuẩn đỏ / biên thuật toán xanh và đường F0.
</what_changed>

<main_changes>
  - `presentation_speech_silence.pptx` — File bài thuyết trình PowerPoint hoàn thiện (10 slide, tỷ lệ 16:9, kèm Speaker Notes chi tiết từng slide).
  - `presentation_speech_silence.pdf` — File PDF chuẩn vector độ phân giải cao phục vụ nộp bài thi.
  - `scripts/export_presentation_assets.py` — Script trích xuất và dựng 8 đồ thị chuẩn hóa 300 DPI từ 4 file tín hiệu kiểm thử và tập huấn luyện.
  - `scripts/generate_deck.js` — Script Node.js tự động sinh deck PowerPoint với hệ thống bố cục Tech-HUD.
  - `scripts/export_presentation_pdf.py` — Script xuất file PDF vector độc lập đảm bảo chất lượng hiển thị sắc nét.
  - `assets/presentation/` — Thư mục chứa 8 ảnh đồ họa chất lượng cao phục vụ slide.
</main_changes>

---

## 2. Why

<why>
  Để phục vụ buổi báo cáo thi giữa kỳ môn Xử lý tín hiệu số với yêu cầu nghiêm ngặt về thời lượng (3 phút thuyết trình), hình thức trình bày (quy tắc 7 dòng, font >= 18pt, trực quan hóa cao), và hàm lượng kỹ thuật thực nghiệm (phải minh họa trên toàn bộ 4 file kiểm thử, so sánh định lượng MAE/RMSE/SNR và giải thích nguyên nhân sai số, đề xuất giải pháp cải tiến).
</why>

---

## 3. What Proves It

<evidence>

| AC | Verifier | Result |
|---|---|---|
| AC-1 (Tri thức & Nghiên cứu) | Đọc `research.md` | PASS |
| AC-2 (Kiến trúc & Quyết định) | Đọc `decision.md` | PASS |
| AC-3 (Kế hoạch lát cắt) | Đọc `plan.md` | PASS |
| AC-4 (Sinh đồ thị chất lượng cao) | `python3 scripts/export_presentation_assets.py` | PASS |
| AC-5 (Sinh PPTX & PDF) | `node scripts/generate_deck.js` & `python3 scripts/export_presentation_pdf.py` | PASS |
| AC-6 (Tuân thủ tiêu chí giảng viên) | Kiểm tra trực quan 10 ảnh slide trong `slide_qa/` | PASS |

<!-- To reproduce: -->
```bash
# 1. Sinh đồ thị độ phân giải cao
.venv/bin/python scripts/export_presentation_assets.py

# 2. Sinh bài thuyết trình PowerPoint
node scripts/generate_deck.js

# 3. Xuất file PDF vector phục vụ nộp bài
.venv/bin/python scripts/export_presentation_pdf.py
```

</evidence>

---

## 4. What Remains Risky

<residual_risk>
  - Không có rủi ro kỹ thuật. Người trình bày chỉ cần đọc theo kịch bản Speaker Notes đã tích hợp sẵn trong từng slide để đảm bảo thời lượng trong vòng 3 phút.
</residual_risk>

---

## 5. Decisions & Assumptions

<decisions_and_assumptions>
  - DEC-001: Lựa chọn kết hợp `pptxgenjs` để xây dựng slide PowerPoint tương thích cao và Matplotlib Asset Pipeline để render các đồ thị tín hiệu phức tạp với độ sắc nét tuyệt đối.
  - Bổ sung `scripts/export_presentation_pdf.py` để đảm bảo có thể xuất file PDF vector 16:9 hoàn hảo ngay trong môi trường dòng lệnh Linux mà không cần cài đặt gói GUI LibreOffice Impress.
</decisions_and_assumptions>

---

## 6. Next Action

<next_action>
  Nhóm sinh viên sử dụng file `presentation_speech_silence.pptx` để thuyết trình và nộp cả 2 file `presentation_speech_silence.pptx` cùng `presentation_speech_silence.pdf` theo hướng dẫn của giảng viên.
</next_action>

</handoff>
