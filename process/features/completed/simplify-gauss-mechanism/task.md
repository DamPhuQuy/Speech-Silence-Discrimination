# Task: FEAT-GAUSS-01 Tối Giản và Chuẩn Hóa Cơ Chế Gaussian VAD trong gauss.ipynb

<task_spec version="3.0" framework="RIPER-5">

<!-- ════════════════════════════════════════════
     SECTION 0 — TASK CONTROL (master state record)
     ════════════════════════════════════════════ -->
<task_control>
  <status>COMPLETED</status>
  <spec_level>S1</spec_level>
  <priority>P1</priority>
  <risk>MEDIUM</risk>
  <estimated_story_points>2</estimated_story_points>
  <working_mode>PAIR</working_mode>
  <observability_mode>OFF</observability_mode>
  <current_phase>REVIEW</current_phase>
  <owner>@antigravity</owner>
  <decision_owner>@engineer</decision_owner>
  <created>2026-10-06</created>
  <last_updated>2026-10-06</last_updated>
</task_control>

---

## 1. Specification (Pillar 1: Task / Spec)

<specification>
  <goal>
    Tái cấu trúc và thay đổi cơ chế triển khai trong [gauss.ipynb](file:///home/phuqy/Documents/main_gk/gauss.ipynb) nhằm đạt mức độ rút gọn tối đa, trực quan, dễ hiểu nhất cho sinh viên thuyết trình trong 3 phút, đồng thời đảm bảo 100% các yêu cầu kỹ thuật và quy chuẩn chấm thi của môn học.
  </goal>

  <current_behavior>
    - [gauss.ipynb](file:///home/phuqy/Documents/main_gk/gauss.ipynb) hiện có 15 cells cồng kềnh (dung lượng > 1.3 MB).
    - Xuất hiện đoạn code uncommitted tại Cell 8 & 9 (Mục 3.1) dài hơn 112 dòng, sử dụng thư viện ngoài `scipy.stats` (vi phạm quy định chỉ dùng built-in NumPy của giảng viên) để vẽ đồ thị zoom phức tạp nhằm giải thích tại sao ngưỡng rơi sát 0.
    - Mã nguồn chứa nhiều khối code phòng thủ rườm rà (quét thư mục 4 lần, xử lý uint8, parse thông số thừa từ lab, thuật toán bipartite matching 40 dòng,...).
    - Cấu trúc các bước chưa đạt độ tinh gọn và liền mạch cao nhất để sinh viên dễ đọc, hiểu và bảo vệ bài.
  </current_behavior>

  <expected_behavior>
    - Notebook [gauss.ipynb](file:///home/phuqy/Documents/main_gk/gauss.ipynb) được tinh gọn thành các khối logic mạch lạc, súc tích, loại bỏ hoàn toàn code thừa và thư viện ngoài (`scipy.stats`).
    - Cơ chế thống kê Gauss được trình bày trong sáng:
      + Ước lượng $(\mu_{\text{sil}}, \sigma_{\text{sil}})$ và $(\mu_{\text{sp}}, \sigma_{\text{sp}})$ trực tiếp từ nhãn chuẩn của 4 file huấn luyện bằng hàm NumPy cơ bản (`np.mean`, `np.std`).
      + Áp dụng công thức ngưỡng giao điểm chuẩn hóa cân bằng độ lệch $z$-score:
        $$T = \frac{\mu_{\text{sil}} \cdot \sigma_{\text{sp}} + \mu_{\text{sp}} \cdot \sigma_{\text{sil}}}{\sigma_{\text{sp}} + \sigma_{\text{sil}}}$$
      + Trực quan hóa phân bố Gauss và histogram trung gian bằng đồ thị NumPy + Matplotlib tinh gọn, thanh thoát, dễ giải thích trong 30 giây.
    - Giữ trọn vẹn độ chính xác phân đoạn, kiểm thử tự động trên cả 4 file test, in bảng MAE/RMSE và hiển thị 4 đồ thị chuẩn gồm Waveform, STE, Ngưỡng $T$, Biên chuẩn, Biên dự đoán và đường F0 (theo hướng dẫn làm slide).
  </expected_behavior>

  <actor_authorization>
    Sinh viên / Kỹ sư thực hiện đồ án môn học Xử lý tín hiệu âm thanh và tiếng nói.
  </actor_authorization>

  <invariants>
    - Tham số cố định: `frame_size = 25 ms`, `frame_shift = 10 ms`, cửa sổ phân tích và tâm khung thời gian.
    - Hậu xử lý: Gộp khoảng lặng ngắn $< 200\text{ ms}$ theo đúng quy định tuyệt đối của đề bài.
    - Dữ liệu: Huấn luyện trên 4 file `data/TinHieuHuanLuyen`, kiểm thử trên 4 file `data/TinHieuKiemThu`.
    - Thư viện: Tuân thủ quy định thi — không dùng toolbox ngoài, chỉ dùng hàm built-in của Python, NumPy, Matplotlib và `scipy.io.wavfile` để đọc audio.
    - Đơn vị đo: Sai số MAE và RMSE tính theo mili-giây (ms).
  </invariants>

  <out_of_scope>
    - Không can thiệp sửa đổi các notebook khác: [binary.ipynb](file:///home/phuqy/Documents/main_gk/binary.ipynb), [histogram.ipynb](file:///home/phuqy/Documents/main_gk/histogram.ipynb).
    - Không sửa đổi cấu trúc dữ liệu âm thanh trong `data/`.
    - Không thêm các bộ lọc tiếng nói ngắn không có trong yêu cầu đề bài.
  </out_of_scope>

  <acceptance_criteria>
    - [ ] AC-1: [gauss.ipynb](file:///home/phuqy/Documents/main_gk/gauss.ipynb) chạy hoàn tất toàn bộ từ đầu đến cuối không có bất kỳ lỗi (clean execution).
    - [ ] AC-2: Loại bỏ hoàn toàn `scipy.stats` và code rườm rà; số cell và số dòng code giảm tối thiểu 30-40%, cấu trúc rõ ràng theo 4 bước bài tập.
    - [ ] AC-3: Thuật toán ước lượng Gauss xác định chính xác bộ tham số $(\mu_{\text{sil}}, \sigma_{\text{sil}}, \mu_{\text{sp}}, \sigma_{\text{sp}})$ và ngưỡng $T^*$.
    - [ ] AC-4: Bảng định lượng in đầy đủ MAE, RMSE trên 4 file kiểm thử (`phone_F2`, `phone_M2`, `studio_F2`, `studio_M2`) kèm trung bình Phone, Studio, Overall.
    - [ ] AC-5: Xuất đủ 4 đồ thị kết quả trực quan gồm 2 tầng (Dạng sóng + Vùng chuẩn + Biên GT/Pred và STE + Ngưỡng + Biên + Đường F0).
  </acceptance_criteria>

  <definition_of_ready>
    - [x] Mục tiêu và tiêu chí nghiệm thu rõ ràng, đo lường được.
    - [x] Ranh giới bất biến (Invariants) và Out-of-scope được xác lập chặt chẽ.
    - [x] Đã hoàn thành phân tích nghiên cứu chi tiết trong research.md.
  </definition_of_ready>
</specification>

---

## 2. Context Boundaries (Pillar 2: Context)

<context_boundaries>
  <target_files>
    - [gauss.ipynb](file:///home/phuqy/Documents/main_gk/gauss.ipynb) — Tái cấu trúc, tinh giản cơ chế và hiển thị.
  </target_files>

  <context_groups>
    - `docs/assignments/` — Đề bài phân đoạn Speech/Silence và Hướng dẫn trình bày slide.
    - `README.md` — Tài liệu tổng quan của đồ án và chuẩn mực kỹ thuật.
    - `docs/notes/note_gauss_threshold.md` — Ghi chú nghiên cứu ngưỡng Gauss.
  </context_groups>

  <source_of_truth>
    <requirement>[Hướng dẫn BT thi GK nhóm 3-4 SV](file:///home/phuqy/Documents/main_gk/docs/assignments/Hướng%20dẫn%20BT%20thi%20GK%20nhóm%203-4%20SV_Phân%20đoạn%20tín%20hiệu%20thành%20tiếng%20nói%20và%20khoảng%20lặng_XLTHS_GK%202026.docx)</requirement>
    <presentation>[Hướng dẫn trình bày slide và nộp bài thi](file:///home/phuqy/Documents/main_gk/docs/assignments/Hướng%20dẫn%20trình%20bày%20slide%20và%20nộp%20bài%20thi.pdf)</presentation>
    <existing_behavior>[gauss.ipynb](file:///home/phuqy/Documents/main_gk/gauss.ipynb)</existing_behavior>
  </source_of_truth>
</context_boundaries>

---

## 3. Verification Strategy

<verification_strategy>
| AC / Risk | Evidence required | Verifier |
|---|---|---|
| AC-1: Clean Run | Toàn bộ cells thực thi thành công không lỗi | `jupyter nbconvert --to notebook --execute gauss.ipynb` |
| AC-2: Code Lean & No scipy.stats | Không chứa `scipy.stats`, giảm dòng code dư thừa | `grep -n "scipy.stats" gauss.ipynb` -> empty |
| AC-3: Ngưỡng Gauss chuẩn | In rõ các tham số $(\mu, \sigma)$ và $T^*$ | Kiểm tra output của Cell huấn luyện |
| AC-4: Bảng MAE/RMSE | Bảng số liệu hoàn chỉnh, MAE khớp với barem | Kiểm tra output Cell đánh giá kiểm thử |
| AC-5: 4 Đồ thị trực quan | 4 figures 2 tầng hiển thị đúng yêu cầu giảng viên | Kiểm tra output hiển thị hình ảnh |
</verification_strategy>

</task_spec>
