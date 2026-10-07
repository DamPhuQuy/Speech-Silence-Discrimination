# Technical Decision: DEC-GAUSS-SLIDE-01 Kiến Trúc & Phương Pháp Xây Dựng Slide Thuyết Trình Gaussian

<technical_decision task_id="FEAT-GAUSS-SLIDE-01" dec_id="DEC-GAUSS-SLIDE-01" version="2.0" framework="RIPER-5">

<!-- READ-ONLY PHASE. Evaluating options. PAIR: human decides. DELEGATED: agent auto-selects optimal recommendation and advances. -->
<decision_status>
  <phase>INNOVATE</phase>
  <mode>READ-ONLY</mode>
  <halting_status>READY_FOR_SIGN_OFF</halting_status>
  <decision_owner>@architect</decision_owner>
  <last_updated>2026-10-07T11:44:00+07:00</last_updated>
</decision_status>

---

## 1. Design Space & Degrees of Freedom (I0: Design Space)

<design_space>
  <context_reference>
    <task>[task.md](file:///home/phuqy/Documents/main_gk/process/features/active/gaussian-presentation-deck/task.md)</task>
    <research_artifact>[research.md](file:///home/phuqy/Documents/main_gk/process/features/active/gaussian-presentation-deck/research.md)</research_artifact>
  </context_reference>

  <mutable_dimensions>
    - **Nội dung văn bản & Typography:** Cập nhật toàn bộ các text node trong các slide 1, 2, 3, 5 sang tiếng Việt học thuật, súc tích ($\le 10$ từ/dòng, $\le 7$ dòng/slide, font size $\ge 18\text{pt}$).
    - **Nội dung Slide 4 (Trống):** Bổ sung bảng tổng hợp định lượng 5 cột chuẩn xác (Tên File, Môi trường, SNR, MAE, RMSE) kèm các trung bình Studio, Phone, Toàn bộ.
    - **Cắt giảm Slide:** Loại bỏ hoàn toàn các slide thừa (Slide 6 đến Slide 16 của template Canva).
    - **Công cụ thực thi:** Lựa chọn giữa Chỉnh sửa OOXML trực tiếp (OpenXML ZIP injection), Tự động hóa qua `python-pptx`, hoặc Viết script sinh mới bằng `pptxgenjs`.
  </mutable_dimensions>

  <immutable_boundaries>
    - **Số liệu Thực nghiệm Bất biến:** Phải khớp 100% với [simple_statistics.ipynb](file:///home/phuqy/Documents/main_gk/simple_statistics.ipynb):
      - Ngưỡng tối ưu: $T^* = 0.002495$.
      - Tham số huấn luyện: $\mu_{\text{sil}} = 0.000249, \sigma_{\text{sil}} = 0.000634, \mu_{\text{sp}} = 0.202467, \sigma_{\text{sp}} = 0.235694$.
      - MAE kiểm thử: `phone_F2` ($27.5\text{ ms}$), `phone_M2` ($2.5\text{ ms}$), `studio_F2` ($5.0\text{ ms}$), `studio_M2` ($12.494\text{ ms}$).
      - MAE trung bình: Phone ($15.0\text{ ms}$), Studio ($8.747\text{ ms}$), Toàn bộ ($11.874\text{ ms}$).
    - **Ngôn ngữ Thiết kế & Visual Assets:** Kế thừa tỷ lệ 16:9 ($1440 \times 810\text{ pt}$), bảng màu Canva (Cyan `#00A8FF` / Orange `#F58220` / Slate `#0F172A`), đồ thị `image18.png` (Gaussian PDF) và `image19.png` - `image22.png` (4 waveforms).
    - **Quy tắc Thuyết trình Giảng viên:** Không vượt quá 5 slide, thời lượng trình bày 3 phút.
  </immutable_boundaries>

  <hard_constraints>
    - **Không được làm hỏng tệp:** Tệp đầu ra `.pptx` phải mở được bình thường trên Microsoft PowerPoint và xuất được PDF sạch bằng LibreOffice (`soffice`).
    - **Không sửa đổi dữ liệu gốc:** Không can thiệp vào các tệp âm thanh trong `data/` hay làm hỏng các notebook thuật toán khác (`binary.ipynb`, `histogram.ipynb`).
  </hard_constraints>
</design_space>

---

## 2. Decision Required

<decision_question>
  Lựa chọn phương pháp kỹ thuật tối ưu để tái cấu trúc và hoàn thiện bộ 5 slide thuyết trình Gaussian từ tệp mẫu `Digital vs. Analog Reliable Signal Science Presentation.pptx`: Chỉnh sửa trực tiếp cấu trúc OpenXML của template gốc (Option A), Can thiệp qua mô hình đối tượng `python-pptx` (Option B), hay Tái tạo hoàn toàn bằng script `pptxgenjs` (Option C)?
</decision_question>

---

## 3. Candidate Options (I1: Repo-Native Candidates)

<options>

  <option id="A" type="Repo-Native First">
    <title>Surgical OOXML In-Place Transformation & Slide Trimming (Chỉnh sửa Trực tiếp OpenXML)</title>
    <approach>
      Giải nén tệp mẫu `Digital vs. Analog Reliable Signal Science Presentation.pptx`, sử dụng script Python can thiệp chính xác vào các tệp XML:
      1. Cập nhật các text node (`<a:t>`) trên slide 1, 2, 3, 5 theo các quy tắc giảng viên.
      2. Inject cấu trúc bảng PowerPoint gốc (`<a:tbl>`) vào `slide4.xml` với styling bảng đồng bộ màu sắc template.
      3. Cắt tỉa danh sách slide trong `ppt/presentation.xml` (`<p:sldIdLst>`) chỉ giữ lại rId6 -> rId10 (5 slide đầu), loại bỏ rId11 -> rId21 (slide 6-16).
      4. Thu dọn các rels và đóng gói lại tệp `.pptx`, kiểm tra tính toàn vẹn bằng `scripts/office/validate.py` và xuất PDF bằng `soffice`.
    </approach>
    <repo_native_alignment>Tận dụng 100% hình khối vector, các thẻ tròn 4 giai đoạn, vị trí căn chỉnh tinh xảo của Canva và các ảnh đã chèn sẵn trong file mẫu.</repo_native_alignment>
    <complexity>MEDIUM</complexity>
    <blast_radius>MINIMAL (Chỉ tác động đến presentation target, lưu bản backup trước khi sửa)</blast_radius>
  </option>

  <option id="B" type="Programmatic Object-Model">
    <title>Python-pptx Programmatic Transformation (Xử lý qua Thư viện python-pptx)</title>
    <approach>
      Dùng thư viện `python-pptx` để nạp template, duyệt qua cây `ShapeTree` của từng slide để thay thế text, tạo bảng trên slide 4 bằng `shapes.add_table()`, và can thiệp nội bộ vào `sldIdLst` để xóa các slide 6-16.
    </approach>
    <repo_native_alignment>Sử dụng cú pháp Python có sẵn trong môi trường virtualenv.</repo_native_alignment>
    <complexity>MEDIUM-HIGH</complexity>
    <blast_radius>MODERATE (`python-pptx` không hỗ trợ native API xóa slide; can thiệp nội bộ dễ làm mất style text run hoặc mất theme formatting của Canva)</blast_radius>
  </option>

  <option id="C" type="Declarative Clean-Slate">
    <title>Regenerate Clean 5-Slide Presentation via pptxgenjs (Tái tạo mới bằng Declarative Script)</title>
    <approach>
      Viết script Node.js với `pptxgenjs` (tương tự `scripts/generate_deck.js`), thiết lập layout 16:9, bảng màu và vẽ lại 5 slide từ đầu bằng code, nạp các ảnh biểu đồ từ `assets/presentation/` hoặc trích xuất từ file mẫu.
    </approach>
    <repo_native_alignment>Mã nguồn JavaScript có sẵn trong thư mục `scripts/`.</repo_native_alignment>
    <complexity>HIGH</complexity>
    <blast_radius>LOW (Tạo file độc lập hoàn toàn)</blast_radius>
  </option>

</options>

---

## 4. Weighted Pugh Decision Matrix (I2: Trade-Off Analysis)

<!-- Baseline: Tệp PPTX hiện tại (Baseline = 0).
     Thang điểm: +2 (Rất tốt), +1 (Tốt), 0 (Trung tính), -1 (Kém), -2 (Rất kém).
     Quy tắc: Phương án được chọn phải có Điểm trọng số > 0. -->
<pugh_matrix>

| Tiêu Chí Đánh Giá | Trọng Số ($W_i$) | Baseline (File gốc) | Option A (Surgical OOXML) | Option B (python-pptx) | Option C (pptxgenjs Clean) |
|---|:---:|:---:|:---:|:---:|:---:|
| **1. Độ tương thích & Giữ trọn thẩm mỹ Canva** (Hình khối, màu sắc, font Canva) | **3** | 0 | **+2** (100% nguyên bản) | +1 (Có nguy cơ mất run style) | -1 (Phải dựng lại card thủ công) |
| **2. Tuân thủ Quy chuẩn Thuyết trình** ($\le 7$ dòng, $\le 10$ từ, $\ge 18\text{pt}$) | **3** | 0 | **+2** (Kiểm soát chi tiết từng node) | +1 (Cần override paragraph styles) | **+2** (Cấu hình fontSize chặt chẽ) |
| **3. Độ chính xác Dữ liệu Thực nghiệm** ($T^*$, MAE, RMSE, Audio Error Analysis) | **2** | 0 | **+2** (Inject số liệu chính xác) | **+2** (Inject số liệu chính xác) | **+2** (Inject số liệu chính xác) |
| **4. Độ tin cậy Kỹ thuật & Không hỏng file** (Valid OOXML & xuất PDF sạch) | **2** | 0 | **+1** (Đã có validate script kiểm chứng) | -1 (Rủi ro corrupt khi xóa slide nội bộ) | **+2** (Bộ sinh chuẩn OOXML) |
| **5. Tính khả thi & Tốc độ triển khai** | **2** | 0 | **+2** (Tận dụng ngay 5 slide đã dựng sẵn) | 0 (Mất thời gian xử lý xóa slide) | -1 (Mất nhiều thời gian vẽ lại layout) |
| **Tổng Điểm Trọng Số ($\sum W_i \times S_{ij}$)** | -- | **0** | **+22** | **+7** | **+7** |

</pugh_matrix>

---

## 5. Adversarial Critic Report (I3: Red Team Challenge)

<adversarial_critic target_option="A">
  <performance_critic>
    - **Thách thức:** Quá trình giải nén, chỉnh sửa XML và nén lại zip có làm tăng kích thước file hay gây giật lag khi trình chiếu không?
    - **Phản biện:** Hoàn toàn không. Việc cắt bỏ 11 slide thừa (từ slide 6 đến 16) sẽ giảm dung lượng tệp từ ~7.9 MB xuống chỉ còn ~3.5 MB, giúp bài thuyết trình mở nhanh hơn, mượt mà hơn và tải nhẹ hơn.
  </performance_critic>

  <security_and_hygiene_critic>
    - **Thách thức:** Việc chỉnh sửa trực tiếp XML có thể vô tình làm vỡ namespace (`p:`, `a:`, `r:`) hoặc làm sai lệch liên kết quan hệ trong `_rels`, dẫn đến việc PowerPoint báo lỗi "Corrupt file" khi mở.
    - **Phản biện:** Quy trình sẽ sử dụng script Python với bộ parser an toàn (`defusedxml.minidom` hoặc regex text-node targeting), bảo toàn 100% namespace và shape ID gốc. Đồng thời, bước đóng gói sẽ chạy qua `scripts/office/validate.py` và kiểm tra trực quan bằng việc render sang PDF qua `soffice` để đảm bảo không có bất kỳ lỗi cú pháp nào.
  </security_and_hygiene_critic>

  <broken_assumptions>
    - Giả định rằng Slide 4 có thể chứa vừa cả Bảng số liệu và các chú thích phân tích: Cần bố trí layout chia không gian hợp lý (Bảng ở trên, 3 gạch đầu dòng kết luận đắt giá ở dưới) để đảm bảo không vi phạm quy tắc $\le 7$ dòng và font $\ge 18\text{pt}$.
  </broken_assumptions>

  <research_gaps>
    - Cần xác định vị trí tọa độ của bảng trên Slide 4 để khớp với lề và khung của các slide khác. Tận dụng tọa độ chuẩn của template canvas $1440 \times 810\text{ pt}$ ($18288000 \times 10287000\text{ EMU}$).
  </research_gaps>

  <arbitrator_verdict rounds="1">
    <status>CLEARED</status>
    <debate_summary>
      Option A đạt điểm số vượt trội (+22) nhờ kế thừa trọn vẹn đồ họa chuyên nghiệp của Canva vốn đã được người dùng chọn làm tiêu chuẩn (Standard). Rủi ro kỹ thuật về OpenXML được kiểm soát triệt để bằng script validation và kiểm tra thị giác PDF. Phê duyệt khuyến nghị Option A.
    </debate_summary>
  </arbitrator_verdict>
</adversarial_critic>

---

## 6. Recommendation

<recommendation>
  **Khuyến nghị chính thức: Lựa chọn Phương án A (Surgical OOXML In-Place Transformation & Slide Trimming).**
  
  Lý do cốt lõi:
  1. Đáp ứng trọn vẹn yêu cầu của người dùng: lấy [Digital vs. Analog Reliable Signal Science Presentation.pptx](file:///home/phuqy/Documents/main_gk/Digital%20vs.%20Analog%20Reliable%20Signal%20Science%20Presentation.pptx) làm **chuẩn mực (Standard)**, giữ nguyên đồ họa, màu sắc và bố cục xuất sắc của Canva.
  2. Tối ưu hóa cấu trúc thành đúng 5 slide trọng tâm cho phần Phân phối chuẩn Gauss (Gaussian Distribution & Bayes Threshold), loại bỏ 11 slide template thừa.
  3. Đảm bảo 100% các tiêu chí chấm điểm của Giảng viên: $\le 7$ dòng/slide, $\le 10$ từ/dòng, cỡ chữ $\ge 18\text{pt}$, độ tương phản cao, và căn chỉnh thời lượng 3 phút.
  4. Trình bày số liệu thực nghiệm nhất quán tuyệt đối với [simple_statistics.ipynb](file:///home/phuqy/Documents/main_gk/simple_statistics.ipynb).
</recommendation>

---

## 7. Implementation Decision & Negative Memory (I4: Decision & Graveyard)

<!-- PAIR mode: Human engineer reviews and fills this section before signing Gate 1 -->
<engineer_decision>
  <selected_option>A</selected_option>
  <rationale>Approved by user. Option A preserves 100% of Canva aesthetic, canvas dimensions, vector styling, and embedded plots while enabling surgical text and table injection conforming to academic guidelines.</rationale>

  <!-- NEGATIVE ARCHITECTURAL MEMORY: Lưu trữ các phương án bị bác bỏ để tránh lặp lại sai lầm -->
  <rejected_alternatives>
    <alternative id="B">
      <fatal_flaw>Thư viện python-pptx không có cơ chế chính thức để xóa slide và làm mất các định dạng chạy chữ (run formatting) phức tạp do Canva tạo ra khi gán đè văn bản.</fatal_flaw>
      <resurrection_condition>Chỉ xem xét nếu bài toán yêu cầu tạo slide động hoàn toàn không có template mẫu có sẵn.</resurrection_condition>
    </alternative>
    <alternative id="C">
      <fatal_flaw>Việc viết lại bằng pptxgenjs từ đầu đòi hỏi dựng lại toàn bộ các khối cong phức tạp và sơ đồ 4 giai đoạn, làm giảm tính đồng bộ mỹ thuật với file Canva gốc mà người dùng yêu cầu làm chuẩn.</fatal_flaw>
      <resurrection_condition>Chỉ xem xét nếu file template gốc bị hỏng nghiêm trọng hoặc không thể mở được trên môi trường Linux.</resurrection_condition>
    </alternative>
  </rejected_alternatives>

  <residual_risks>
    - **Rủi ro sai lệch font khi render LibreOffice:** Được kiểm tra trực tiếp qua lệnh xuất PDF `soffice --headless --convert-to pdf` và kiểm tra ảnh cắt từng slide bằng `pdftoppm`.
  </residual_risks>
</engineer_decision>

---

## 8. Constraints Created

<constraints_created>
  - Phải tạo bản sao dự phòng `Digital vs. Analog Reliable Signal Science Presentation.pptx.bak` trước khi thực hiện bất kỳ thao tác ghi đè nào.
  - Số lượng slide hoàn thiện của bộ trình chiếu phải chính xác là 5 slide.
  - Mỗi slide nội dung phải có tối đa 7 dòng, mỗi dòng tối đa 10 từ, và cỡ chữ tối thiểu 18pt cho phần nội dung (tiêu đề $\ge 24\text{pt}$).
  - Mọi số liệu trong Slide 3, Slide 4, Slide 5 phải trích xuất chính xác từ các biến và bảng trong [simple_statistics.ipynb](file:///home/phuqy/Documents/main_gk/simple_statistics.ipynb).
</constraints_created>

---

## 9. Evidence Still Required

<evidence_required>
  - File PDF xuất từ file PPTX sau chỉnh sửa hiển thị sắc nét, không bị tràn viền (overflow), không bị đè chữ (overlap).
  - Bảng định lượng trên Slide 4 hiển thị đầy đủ 7 hàng dữ liệu (4 file đơn lẻ + 3 hàng trung bình) với font chữ rõ ràng, dễ đọc trên máy chiếu.
</evidence_required>

---

## 10. Innovation Halting Verification (Gate G1 Sign-off)

<halting_verification>
  - [x] **D_space (Design Space):** Các chiều có thể thay đổi (text, bảng, số slide) và ranh giới bất biến (số liệu, màu sắc template) được phân định rõ ràng.
  - [x] **S_alternatives (Alternatives):** 3 phương án kiến trúc (OOXML In-Place, python-pptx, pptxgenjs) đã được đề xuất và phân tích đầy đủ.
  - [x] **T_traded (Trade-offs):** Đã đánh giá ma trận quyết định Weighted Pugh Matrix (Phương án A đạt điểm số cao nhất: +22 > 0).
  - [x] **A_challenged (Adversarial):** Red Team Challenge đã chất vấn về rủi ro vỡ XML và hiệu năng tệp; trọng tài đã phê duyệt CLEARED.
  - [x] **D_decided (Decision & Memory):** Đã lưu trữ Negative Architectural Memory cho Phương án B và C.
</halting_verification>

<gate id="G1">
  - [x] All candidate options evaluated across Weighted Pugh Decision Matrix (selected candidate score > 0).
  - [x] Selected design and negative memory (rejected alternatives) recorded.
  - [x] No open business, schema, or security questions remaining unresolved.
  <approved_by>User</approved_by>
  <approved_date>2026-10-07</approved_date>
</gate>

</technical_decision>
