# Task: FEAT-GAUSS-SLIDE-01 Thiết Kế Slide Thuyết Trình Thuật Toán Gauss Theo Chuẩn Template

<task_spec version="3.0" framework="RIPER-5">

<!-- ════════════════════════════════════════════
     SECTION 0 — TASK CONTROL (master state record)
     ════════════════════════════════════════════ -->
<task_control>
  <status>ACTIVE</status>
  <spec_level>S1</spec_level>
  <priority>P1</priority>
  <risk>MEDIUM</risk>
  <estimated_story_points>3</estimated_story_points>
  <working_mode>PAIR</working_mode>
  <observability_mode>OFF</observability_mode>
  <current_phase>RESEARCH</current_phase>
  <owner>@antigravity</owner>
  <decision_owner>@engineer</decision_owner>
  <created>2026-10-07</created>
  <last_updated>2026-10-07</last_updated>
</task_control>

---

## 1. Specification (Pillar 1: Task / Spec)

<specification>
  <goal>
    Thiết kế và hoàn thiện bộ slide thuyết trình chuyên nghiệp (4-5 slide) chuyên sâu cho Thuật toán 3: Thống kê Phân phối chuẩn Gauss (Simple Statistics Gaussian / Bayes Quadratic), sử dụng chuẩn template nhận diện từ [Digital vs. Analog Reliable Signal Science Presentation.pptx](file:///home/phuqy/Documents/main_gk/Digital%20vs.%20Analog%20Reliable%20Signal%20Science%20Presentation.pptx). Bộ slide tích hợp đầy đủ số liệu thực nghiệm định lượng, đồ thị minh họa phân phối huấn luyện, đồ thị phân đoạn kiểm thử và các phân tích âm học chuyên sâu từ [simple_statistics.ipynb](file:///home/phuqy/Documents/main_gk/simple_statistics.ipynb), đồng thời tuân thủ 100% quy định chấm thi của giảng viên.
  </goal>

  <current_behavior>
    Trong file `Digital vs. Analog Reliable Signal Science Presentation.pptx`:
    - Slide 1: Đã có tiêu đề sơ khai ("PHÂN ĐOẠN TIẾNG NÓI VÀ KHOẢNG LẶNG", "NHÓM 14").
    - Slide 2: Vẫn chứa nội dung mẫu tiếng Indo/Malay ("PROJECT LIFECYCLE STAGES" - Initiation, Planning, Execution, Closure).
    - Slide 3: Đã chèn hình phân tích phân phối Gauss nhưng tiêu đề và mô tả chưa được tinh chỉnh hoàn thiện.
    - Slide 4: Hoàn toàn trống (Blank slide).
    - Slide 5: Chứa 4 đồ thị kiểm thử nhưng chưa có bảng số liệu tổng hợp định lượng MAE/RMSE chuẩn.
    - Các slide 6-16: Thuộc bài thuyết trình cũ về Tín hiệu Tương tự vs Tín hiệu Số.
  </current_behavior>

  <expected_behavior>
    Tạo ra phiên bản slide hoàn chỉnh, chuẩn chỉnh theo nhận diện thương hiệu của template `Digital vs. Analog Reliable Signal Science Presentation.pptx`:
    1. Slide 1 (Cover): Tiêu đề đề tài "PHÂN ĐOẠN TIẾNG NÓI & KHOẢNG LẶNG - THUẬT TOÁN GAUSSIAN BAYES", định danh nhóm/sinh viên thực hiện.
    2. Slide 2 (Quy trình thuật toán): Chuyển đổi khung 4 STAGE của template sang quy trình 4 bước phân đoạn VAD (Framing/STE -> Mô hình hóa Gauss -> Ngưỡng tối ưu Bayes Quadratic -> Hậu xử lý khoảng lặng ảo).
    3. Slide 3 (Giải pháp lõi trên tập Huấn luyện): Đồ thị phân phối chuẩn Gauss toàn cục + bảng tham số Silence/Speech + điểm giao nhau Bayes Quadratic $T^* = 0.002495$.
    4. Slide 4 (Kết quả thực nghiệm trên tập Kiểm thử): Bảng đánh giá định lượng 4 file test (SNR, MAE, RMSE) + trung bình Phone, Studio và Toàn bộ.
    5. Slide 5 (Trực quan hóa & Phân tích âm học): 4 figure kiểm thử + phân tích sai số chi tiết (Err Start vs Err End) giải thích hiện tượng âm học ở môi trường nhiễu Phone vs phòng thu sạch Studio.
  </expected_behavior>

  <actor_authorization>
    Sinh viên thực hiện báo cáo thi giữa kỳ môn Xử lý tín hiệu số (XLTHS 2026).
  </actor_authorization>

  <invariants>
    - Tuân thủ quy định làm slide của GV: font $\ge 18\text{pt}$, $\le 7$ dòng/slide, $\le 10$ từ/dòng, màu text tương phản cao.
    - Kế thừa 100% visual motif của template mẫu: tỷ lệ 16:9, bảng màu chính Cyan/Electric Blue (#00A8FF) + Vibrant Orange (#F58220) + Dark Slate (#0F172A) + Nền sáng Canvas (#FFFFFF).
    - Dữ liệu thực nghiệm khớp tuyệt đối với notebook [simple_statistics.ipynb](file:///home/phuqy/Documents/main_gk/simple_statistics.ipynb): $T^* = 0.002495$, TB Phone MAE $15.0\text{ ms}$, TB Studio MAE $8.7\text{ ms}$, Toàn bộ $11.9\text{ ms}$.
    - Thời lượng diễn thuyết thiết kế vừa vặn cho 3 phút trình bày slide (trước 1 phút demo chạy code).
  </invariants>

  <out_of_scope>
    - Không sửa đổi mã nguồn thuật toán trong `binary.ipynb` hoặc `histogram.ipynb`.
    - Không thay đổi dữ liệu gốc trong `data/TinHieuHuanLuyen` hay `data/TinHieuKiemThu`.
  </out_of_scope>

  <acceptance_criteria>
    - [ ] AC-1: Khảo sát và trích xuất cấu trúc bố cục, kích thước canvas, mã màu, font chữ của `Digital vs. Analog Reliable Signal Science Presentation.pptx`.
    - [ ] AC-2: Thiết kế kịch bản chi tiết cho 4-5 slide chuẩn (Cover, Core Pipeline, Training & Threshold, Quantitative Results, Critical Phonetic Analysis) đáp ứng quy tắc $\le 7$ dòng, $\le 10$ từ/dòng.
    - [ ] AC-3: Chuẩn bị đầy đủ các asset hình ảnh độ phân giải cao và số liệu bảng từ `simple_statistics.ipynb`.
    - [ ] AC-4: Cập nhật hoặc sinh file PPTX và PDF tương ứng hiển thị hoàn hảo, không lỗi layout, không tràn viền.
  </acceptance_criteria>

  <definition_of_ready>
    - [x] Mục tiêu, tiêu chuẩn template và tài liệu tham khảo được định vị rõ ràng.
    - [x] Các tệp can thiệp được xác định đầy đủ trong whitelist.
  </definition_of_ready>
</specification>

---

## 2. Scope Contract & File Whitelist

<scope_contract>
  <allowed_files>
    <file>process/features/active/gaussian-presentation-deck/*</file>
    <file>Digital vs. Analog Reliable Signal Science Presentation.pptx</file>
    <file>Digital vs. Analog Reliable Signal Science Presentation.pdf</file>
    <file>scripts/export_presentation_assets.py</file>
    <file>scripts/generate_deck.js</file>
    <file>scripts/export_presentation_pdf.py</file>
    <file>assets/presentation/*</file>
  </allowed_files>

  <forbidden_files>
    <file>binary.ipynb</file>
    <file>histogram.ipynb</file>
    <file>data/*</file>
    <file>docs/assignments/*</file>
  </forbidden_files>

  <negative_constraints>
    - KHÔNG can thiệp vào các file dữ liệu âm thanh gốc.
    - KHÔNG dùng font chữ nhỏ hơn 18pt trên slide nội dung.
    - KHÔNG vượt quá 7 dòng chữ trên mỗi slide.
  </negative_constraints>
</scope_contract>

</task_spec>
