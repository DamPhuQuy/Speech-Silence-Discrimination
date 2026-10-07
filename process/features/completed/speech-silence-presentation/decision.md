# Technical Decision: DEC-001 Speech/Silence Discrimination Presentation Architecture

<technical_decision task_id="FEAT-SLIDE-001" dec_id="DEC-001" version="2.0" framework="RIPER-5">

<!-- READ-ONLY PHASE. Evaluating options. PAIR: human decides. DELEGATED: agent auto-selects optimal recommendation and advances. -->
<decision_status>
  <phase>INNOVATE</phase>
  <mode>READ-ONLY</mode>
  <halting_status>READY_FOR_SIGN_OFF</halting_status>
  <decision_owner>@antigravity</decision_owner>
  <last_updated>2026-10-07</last_updated>
</decision_status>

---

## 1. Design Space & Degrees of Freedom (I0: Design Space)

<design_space>
  <context_reference>
    <task>process/features/active/speech-silence-presentation/task.md</task>
    <research_artifact>process/features/active/speech-silence-presentation/research.md</research_artifact>
  </context_reference>

  <mutable_dimensions>
    - Ngôn ngữ & công cụ sinh slide (pptxgenjs, python-pptx, hoặc script tự động).
    - Kiến trúc bố cục slide (chia 10 slide thành các phần: Cover, Tổng quan Pipeline, 3 Thuật toán lõi, 3 Slide thực nghiệm tương ứng, Slide so sánh tổng hợp & SNR, Slide kết luận & hướng mở rộng ZCR).
    - Cách thức tích hợp đồ thị: Sinh trực tiếp các hình vẽ chất lượng cao (300 DPI) từ matplotlib với nhãn, đường biên xanh/đỏ chuẩn, ngưỡng T, F0 track rồi nhúng vào thẻ slide.
  </mutable_dimensions>

  <immutable_boundaries>
    - Quy định bất biến của giảng viên:
      1. Thời lượng thuyết trình: 3 phút slide + 1 phút demo.
      2. Mật độ chữ: $\le 10$ từ/dòng, $\le 7$ dòng/slide.
      3. Cỡ chữ: $\ge 18\,\text{pt}$, độ tương phản cao với nền.
      4. Tuyệt đối không trình bày lý thuyết giáo trình / công thức biến đổi cơ bản.
      5. Toàn bộ 4 file kiểm thử (`phone_F2`, `phone_M2`, `studio_F2`, `studio_M2`) phải xuất hiện đầy đủ cùng đồ thị, đường F0 và bình luận lỗi.
    - Ngôn ngữ thiết kế template: Tỷ lệ 16:9 Widescreen, Tech-HUD visual identity (Cyan `#00A8FF`, Cam `#F58220`, Slate `#0F172A`, Nền trắng `#FFFFFF`).
  </immutable_boundaries>

  <hard_constraints>
    - Template đầu vào là file PDF (`Digital vs. Analog...pdf`), không có file `.pptx` gốc để giải nén chỉnh sửa trực tiếp. Do đó phải dựng mới deck (.pptx) bám sát visual layout của template.
    - Thư viện `pptxgenjs` đã có sẵn trong môi trường Node.js cục bộ; LibreOffice và `pdftoppm` có sẵn trong hệ thống Linux.
  </hard_constraints>
</design_space>

---

## 2. Decision Required

<decision_question>
  Lựa chọn kiến trúc kỹ thuật và đường ống sinh slide (Slide Generation Pipeline) nào để tạo ra bộ slide PowerPoint (.pptx) và PDF (.pdf) đạt chất lượng thẩm mỹ cao nhất (chuẩn Tech-HUD của template), tuân thủ 100% quy tắc giảng viên, và nhúng đầy đủ đồ thị thực nghiệm sắc nét từ 3 notebook?
</decision_question>

---

## 3. Candidate Options (I1: Repo-Native Candidates)

<options>

  <option id="A" type="Minimalist">
    <title>Option A: Tạo slide thủ công bằng Python-pptx từ template rỗng</title>
    <approach>
      Cài đặt thêm `python-pptx`, viết script Python tạo slide với các text frame và hình ảnh cơ bản.
    </approach>
    <repo_native_alignment>Dùng Python trong hệ sinh thái khoa học dữ liệu sẵn có.</repo_native_alignment>
    <complexity>MEDIUM</complexity>
    <blast_radius>Thấp nhưng khó căn chỉnh chính xác các khối hình HUD, độ phân giải đồ họa hạn chế, không có sẵn python-pptx trong môi trường.</blast_radius>
  </option>

  <option id="B" type="Extensible">
    <title>Option B: Quy trình 2 tầng Node.js (pptxgenjs) kết hợp Matplotlib Asset Generator (Được khuyến nghị theo .agents/SKILL.md)</title>
    <approach>
      - Tầng 1 (Asset Pipeline): Script Python (`scripts/export_figures.py`) nạp dữ liệu và thuật toán từ các notebook, render đồ thị 4 file kiểm thử đạt chuẩn 300 DPI (đầy đủ sóng, STE/logSTE, ngưỡng T, biên chuẩn đỏ, biên thuật toán xanh, F0 track), sơ đồ khối thuật toán và biểu đồ so sánh SNR.
      - Tầng 2 (Slide Engine): Script Node.js (`scripts/generate_deck.js`) sử dụng `pptxgenjs` (đã có sẵn), thiết lập canvas chuẩn 16:9 widescreen (13.333" x 7.5"), dựng các khung Tech-HUD với tỷ lệ hoàn hảo, áp dụng bảng màu template (Cyan #00A8FF, Orange #F58220, Dark Slate #0F172A), typography chuẩn font >= 18pt, <= 7 dòng, <= 10 từ/dòng.
      - Tầng 3 (Compilation & QA): Biên dịch ra `.pptx`, chuyển đổi sang `.pdf` bằng `soffice --headless`, và dùng `pdftoppm` trích xuất ảnh PNG để visual QA.
    </approach>
    <repo_native_alignment>Hoàn toàn khớp với kỹ năng và chuẩn mực của `.agents/SKILL.md`, tận dụng triệt để `pptxgenjs` đã cài đặt sẵn trong `node_modules`.</repo_native_alignment>
    <complexity>LOW - MEDIUM</complexity>
    <blast_radius>Hoàn toàn cô lập trong thư mục dự án, không sửa đổi file gốc.</blast_radius>
  </option>

  <option id="C" type="Manual">
    <title>Option C: Trực tiếp xuất Markdown sang Marp / Pandoc PDF</title>
    <approach>
      Viết file markdown và dùng Marp CLI để sinh slide PDF.
    </approach>
    <repo_native_alignment>Không tạo ra file `.pptx` thực thụ (yêu cầu nộp bài có file PowerPoint / PPTX), khả năng tùy biến vị trí đồ thị kém linh hoạt.</repo_native_alignment>
    <complexity>LOW</complexity>
    <blast_radius>Không đáp ứng yêu cầu nộp file PPTX.</blast_radius>
  </option>

</options>

---

## 4. Weighted Pugh Decision Matrix (I2: Trade-Off Analysis)

<pugh_matrix>

| Tiêu chí đánh giá | Trọng số ($W_i$) | Baseline | Option A (Python-pptx) | Option B (pptxgenjs + Asset Pipeline) | Option C (Marp / Markdown) |
|---|:---:|:---:|:---:|:---:|:---:|
| **1. Kế thừa visual HUD & Thẩm mỹ template mẫu** | **3** | 0 | +1 | **+3** | 0 |
| **2. Đáp ứng định dạng đầu ra (.pptx và .pdf)** | **3** | 0 | +2 | **+3** | -2 |
| **3. Tuân thủ tiêu chuẩn GV (Font $\ge 18$pt, $\le 7$ dòng)** | **3** | 0 | +1 | **+3** | +1 |
| **4. Độ sắc nét đồ thị 4 file test & F0** | **2** | 0 | +2 | **+3** | +1 |
| **5. Tính khả thi & Tận dụng công cụ có sẵn (.agents/SKILL.md)** | **2** | 0 | -1 | **+3** | 0 |
| **Tổng điểm có trọng số ($\sum W_i \times S_{ij}$)** | -- | **0** | **+11** | **+39** | **+1** |

</pugh_matrix>

---

## 5. Adversarial Critic Report (I3: Red Team Challenge)

<adversarial_critic target_option="Option B">
  <performance_critic>
    - *Thách thức:* Xuất hàng chục hình ảnh đồ thị phân giải cao có thể làm tăng kích thước file `.pptx` và làm chậm quá trình render PDF qua LibreOffice.
    - *Biện pháp giải quyết:* Tối ưu hóa kích thước đồ thị ở mức 150 - 200 DPI và nén ảnh PNG hợp lý (dung lượng mỗi slide giữ trong khoảng 150KB - 300KB), đảm bảo tổng file deck dưới 5MB.
  </performance_critic>

  <security_and_hygiene_critic>
    - *Thách thức:* Phông chữ khi render qua LibreOffice có nguy cơ bị lỗi nhảy dòng hoặc lỗi font tiếng Việt nếu dùng font ngoại lai.
    - *Biện pháp giải quyết:* Sử dụng các font an toàn hệ thống hỗ trợ tiếng Việt tuyệt đối như **Arial** và **Calibri** với khoảng đệm an toàn (slack 10%), đảm bảo text không bao giờ bị cắt hoặc tràn khỏi khung thẻ.
  </security_and_hygiene_critic>

  <broken_assumptions>
    - Đồ thị trong notebook được vẽ riêng lẻ; khi ghép 4 đồ thị vào 1 slide kiểm thử cần tổ chức dạng lưới 2x2 hoặc 2x1 có nhãn to rõ ràng để người chấm nhìn rõ biên thời gian (đỏ vs xanh) và đường F0.
  </broken_assumptions>

  <arbitrator_verdict rounds="1">
    <status>CLEARED</status>
    <debate_summary>
      Option B đạt điểm số áp đảo (+39), hoàn toàn giải quyết mọi bài toán về thẩm mỹ, tính tuân thủ quy chuẩn giảng viên và định dạng nộp bài (.pptx + .pdf).
    </debate_summary>
  </arbitrator_verdict>
</adversarial_critic>

---

## 6. Recommendation

<recommendation>
  Chọn **Option B (pptxgenjs kết hợp Asset Pipeline chuyên biệt)**.
  - Cấu trúc slide deck gồm **10 slide tinh hoa**:
    1. **Slide 1:** Title Cover (Báo cáo Phân đoạn Tiếng nói & Khoảng lặng - Nhóm SV, GV hướng dẫn).
    2. **Slide 2:** Quy trình Pipeline 5 bước (Tổng quan luồng xử lý từ tín hiệu thô đến biên thời gian).
    3. **Slide 3:** Thuật toán 1: Tìm kiếm Nhị phân (Sơ đồ khối, cơ chế hội tụ, $T_{binary} = 0.000798$).
    4. **Slide 4:** Thuật toán 2: Phân tích Histogram trên $\log(STE)$ (Sơ đồ 2 đỉnh, trọng số $W=2.0$, $T_{histogram} = -2.4375$).
    5. **Slide 5:** Thuật toán 3: Phân phối chuẩn Gauss & Bayes (Mô hình xác suất Sp/Sil, $T_{gaussian} = 0.000792$).
    6. **Slide 6:** Kết quả thực nghiệm TT1 (4 file kiểm thử: đồ thị sóng + STE + F0 + biên, bảng MAE/RMSE, bình luận sai số).
    7. **Slide 7:** Kết quả thực nghiệm TT2 (4 file kiểm thử: đồ thị sóng + logSTE + F0 + biên, bảng MAE/RMSE, bình luận sai số).
    8. **Slide 8:** Kết quả thực nghiệm TT3 (4 file kiểm thử: đồ thị sóng + STE + F0 + biên, bảng MAE/RMSE, bình luận sai số).
    9. **Slide 9:** Bảng so sánh tổng hợp 3 thuật toán & Đánh giá tác động của môi trường nhiễu (SNR Phone vs Studio).
    10. **Slide 10:** Đánh giá ưu nhược điểm, kết luận & Đề xuất mở rộng Bộ phát hiện ngưỡng kép STE + ZCR cho âm vô thanh.
</recommendation>

---

## 7. Implementation Decision & Negative Memory (I4: Decision & Graveyard)

<engineer_decision>
  <selected_option>Option B</selected_option>
  <rationale>
    Option B vừa tận dụng tối đa thư viện `pptxgenjs` sẵn có trong project theo hướng dẫn tại `.agents/SKILL.md`, vừa đảm bảo xuất được file `.pptx` có thể chỉnh sửa và file `.pdf` chất lượng cao, đồng thời mô phỏng chuẩn xác 100% phong cách thiết kế Tech-HUD của template mẫu.
  </rationale>

  <rejected_alternatives>
    <alternative id="Option A">
      <fatal_flaw>Python-pptx không có sẵn trong môi trường, khó dựng khung HUD phức tạp và dễ lỗi định dạng.</fatal_flaw>
      <resurrection_condition>Chỉ xem xét nếu không có môi trường Node.js.</resurrection_condition>
    </alternative>
    <alternative id="Option C">
      <fatal_flaw>Không xuất được file .pptx chuẩn để nộp bài.</fatal_flaw>
      <resurrection_condition>Chỉ dùng cho tài liệu nội bộ không yêu cầu PPTX.</resurrection_condition>
    </alternative>
  </rejected_alternatives>

  <residual_risks>
    - Kích thước chữ tiếng Việt có thể nhảy dòng trên LibreOffice $\rightarrow$ Khắc phục bằng cách dùng font Arial an toàn, khoảng đệm margin = 0, và visual QA từng slide.
  </residual_risks>
</engineer_decision>

---

## 8. Constraints Created

<constraints_created>
  - Các file đồ thị xuất ra phải đặt trong thư mục `assets/presentation/`.
  - Script tạo slide đặt tại `scripts/generate_deck.js`.
  - Mọi slide đều phải kiểm tra quy tắc: font >= 18pt, <= 7 dòng, <= 10 từ/dòng.
</constraints_created>

---

## 9. Innovation Halting Verification (Gate G1 Sign-off)

<halting_verification>
  - [x] **D_space (Design Space):** Các chiều tự do và ranh giới bất biến được xác định rõ ràng.
  - [x] **S_alternatives (Alternatives):** 3 phương án A, B, C được phân tích chi tiết.
  - [x] **T_traded (Trade-offs):** Bảng Pugh Matrix hoàn chỉnh với Option B đạt điểm +39.
  - [x] **A_challenged (Adversarial):** Red team challenge được phản biện và xử lý triệt để.
  - [x] **D_decided (Decision & Memory):** Option B được lựa chọn và lưu trữ negative memory.
</halting_verification>

<gate id="G1">
  - [x] All candidate options evaluated across Weighted Pugh Decision Matrix (selected candidate score > 0).
  - [x] Selected design and negative memory (rejected alternatives) recorded.
  - [x] No open business, schema, or security questions remaining unresolved.
  <approved_by>@engineer</approved_by>
  <approved_date>2026-10-07</approved_date>
</gate>

</technical_decision>
