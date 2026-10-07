# Task Lite: TASK-BAYES-QUADRATIC Cập Nhật Ngưỡng Bayes Quadratic trong simple_statistics.ipynb

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
    Cập nhật cell chứa hàm `def find_threshold_gaussian` trong notebook `simple_statistics.ipynb` sang cơ chế giải nghiệm phương trình phân định Bayes bậc hai (Bayes Quadratic / Quadratic Discriminant Analysis) giữa 2 phân phối chuẩn Gauss: $p(x | \text{silence}) = p(x | \text{speech})$, đồng thời bảo đảm tính toán đầy đủ bộ dữ liệu huấn luyện `all_ste` và `all_labels` để toàn bộ các cell sau (Cell 7, 11, 12) thực thi trơn tru không lỗi.
  </goal>

  <invariants>
    - Giữ nguyên các hàm tiền xử lý và trích xuất đặc trưng `preprocessing`, `parse_lab`, `apply_framing`, `compute_ste`.
    - Không làm hỏng cấu trúc định dạng JSON của notebook `simple_statistics.ipynb`.
    - Kiểm tra chạy thông suốt toàn bộ 13 cells từ đầu đến cuối không lỗi (Clean execution).
  </invariants>

  <acceptance_criteria>
    - [x] AC-1: Cập nhật Cell 6 của `simple_statistics.ipynb` định nghĩa `solve_bayes_quadratic_threshold` và `find_threshold_gaussian` theo phương trình đẳng mật độ xác suất Bayes bậc 2: $Ax^2 + Bx + C = 0$.
    - [x] AC-2: Cập nhật Cell 5 (Markdown) tương ứng với công thức toán học Bayes Quadratic.
    - [x] AC-3: Thực thi thành công toàn bộ notebook `simple_statistics.ipynb` từ Cell 0 đến Cell 12, sinh ra bảng thông số huấn luyện ($T = 0.002495$) và bảng kết quả kiểm thử trên 4 file.
  </acceptance_criteria>

  <definition_of_ready>
    - [x] Mục tiêu và phương pháp toán học Bayes Quadratic được xác định chính xác.
    - [x] File can thiệp: `simple_statistics.ipynb`.
  </definition_of_ready>
</specification>

---

## 2. Scope Contract & File Whitelist

<scope_contract>
  <allowed_files>
    <file>simple_statistics.ipynb</file>
    <file>process/general-plans/active/bayes-quadratic-threshold/task-lite.md</file>
  </allowed_files>

  <forbidden_files>
    <file>binary.ipynb</file>
    <file>histogram.ipynb</file>
    <file>data/*</file>
    <file>docs/assignments/*</file>
  </forbidden_files>

  <negative_constraints>
    - KHÔNG dùng `replace_file_content` sửa trực tiếp `.ipynb` (chỉ dùng script Python load/dump JSON).
    - KHÔNG thêm thư viện ngoài (chỉ dùng NumPy, Matplotlib, scipy.io.wavfile).
  </negative_constraints>
</scope_contract>

---

## 3. Execution Plan (Compact Slices)

<execution_plan>
  <living_scratchpad>
    - **Completed:** Slice 1 (Cập nhật Cell 5 & Cell 6 và chạy thông suốt toàn bộ notebook)
    - **Current:** Hoàn thành toàn bộ
    - **Blockers:** Không có
    - **Next Steps:** Bàn giao kết quả cho người dùng
  </living_scratchpad>

  ### Slice 1: Cập nhật Cell 5 và Cell 6 trong `simple_statistics.ipynb`
  - **Action:** Cập nhật công thức Markdown Cell 5 và mã nguồn Cell 6 với hàm giải Bayes Quadratic và huấn luyện toàn bộ tập train.
  - **Verifier:** Kiểm tra chạy qua toàn bộ notebook không lỗi bằng script python `exec`.
  - **Status:** [x] DONE
</execution_plan>

---

## 4. Consolidated Verification & Gates

<verification_gates>
  - [x] **Gate G1/G2 (Plan Approved):** Allowed files confirmed, test verifiers defined.
  - [x] **Gate G3 (Ready for Handoff):**
    - [x] Cell 6 updated with Bayes Quadratic logic.
    - [x] Full notebook run executed cleanly without NameError or exceptions (T_gaussian = 0.002495).
</verification_gates>

</task_lite>
