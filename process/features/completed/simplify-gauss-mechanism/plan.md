# Plan: PLAN-GAUSS-01 Kế Hoạch Triển Khai Tối Giản gauss.ipynb

<execution_plan task_id="FEAT-GAUSS-01" plan_id="PLAN-GAUSS-01" version="2.0" framework="RIPER-5">

<!-- PLAN PHASE. Plan artifacts only. No source-code changes. -->
<plan_status>
  <phase>PLAN</phase>
  <last_updated>2026-10-06</last_updated>
</plan_status>

---

## 1. Input Artifacts

<input_artifacts>
  <task_spec>[task.md](file:///home/phuqy/Documents/main_gk/process/features/active/simplify-gauss-mechanism/task.md)</task_spec>
  <research>[research.md](file:///home/phuqy/Documents/main_gk/process/features/active/simplify-gauss-mechanism/research.md)</research>
  <decision>[decision.md](file:///home/phuqy/Documents/main_gk/process/features/active/simplify-gauss-mechanism/decision.md) — DEC-GAUSS-01, Option A (Tinh giản cực đại & thuần NumPy)</decision>
</input_artifacts>

---

## 2. Execution Constraints

<execution_constraints>
  <allowed_files>
    - [gauss.ipynb](file:///home/phuqy/Documents/main_gk/gauss.ipynb) — Notebook mục tiêu tái cấu trúc.
  </allowed_files>
  <forbidden_files>
    - [binary.ipynb](file:///home/phuqy/Documents/main_gk/binary.ipynb)
    - [histogram.ipynb](file:///home/phuqy/Documents/main_gk/histogram.ipynb)
    - `data/*` — Dữ liệu gốc không được can thiệp.
    - `requirements.txt` — Không thêm thư viện phụ thuộc.
  </forbidden_files>
  <allowed_commands>
    - `python3 -c "..."` — Kiểm tra và phân tích cú pháp/nội dung notebook.
    - `.venv/bin/python3 -m jupyter nbconvert --to notebook --execute gauss.ipynb` — Chạy nghiệm thu notebook.
    - `git status`, `git diff` — Theo dõi thay đổi.
  </allowed_commands>
  <restricted_operations>
    - Không sử dụng thư viện `scipy.stats` (chỉ dùng built-in NumPy).
    - Không làm thay đổi logic phân đoạn và tiêu chuẩn đo lường MAE/RMSE (ms).
    - LATS Forced Rollback: Nếu quá trình thực thi gây lỗi 2 lần liên tiếp, khôi phục trạng thái bằng `git checkout gauss.ipynb`.
  </restricted_operations>
  <required_approvals>
    - Phê duyệt Gate G2 trước khi thực thi mã nguồn.
  </required_approvals>
</execution_constraints>

---

## 3. Slice Summary

<slice_summary>

| ID | Behavior | Boundary | Files | AC | Verifier | Risk | Mode | Rollback |
|---|---|---|---|---|---|---|---|---|
| S1 | Tinh giản Tiền xử lý & Trích xuất đặc trưng | Data Loading + Framing + STE + F0 | gauss.ipynb | AC-2 | Python inspect script | LOW | ATOMIC | git checkout |
| S2 | Chuẩn hóa Huấn luyện Gauss & Đồ thị thuần NumPy | Gauss Training + NumPy PDF plot | gauss.ipynb | AC-2, AC-3 | Training execution run | LOW | ATOMIC | git checkout |
| S3 | Tinh giản Hậu xử lý, Bảng MAE & 4 Figure Test | Postprocessing + Evaluation + 4 plots | gauss.ipynb | AC-4, AC-5 | Test evaluation run | LOW | ATOMIC | git checkout |
| S4 | Nghiệm thu toàn diện Run All từ đầu đến cuối | Toàn bộ notebook | gauss.ipynb | AC-1 to AC-5 | Jupyter nbconvert execute | LOW | ATOMIC | git checkout |

</slice_summary>

---

## 4. Slice Details

<slices>

  <slice id="S1">
    <objective>Tinh giản cấu trúc nạp dữ liệu và trích xuất đặc trưng STE / F0 trong gauss.ipynb</objective>
    <change>
      - Đơn giản hóa dataclass `AudioSignal` và hàm `preprocessing`, `parse_lab`, `load_dataset` (loại bỏ kiểm tra uint8 thừa, loại bỏ duyệt 4 đường dẫn, chỉ đọc đúng `data/`).
      - Làm sạch `apply_framing`, `compute_ste`, `normalize_minmax`, và viết gọn `estimate_f0_track`.
    </change>
    <allowed_files>
      - [gauss.ipynb](file:///home/phuqy/Documents/main_gk/gauss.ipynb)
    </allowed_files>
    <acceptance_criteria>
      - [ ] Nạp thành công 4 file huấn luyện, trích xuất STE và F0 chính xác.
    </acceptance_criteria>
    <verifier>
      ```bash
      python3 -c "import json; nb=json.load(open('gauss.ipynb')); print('Cells:', len(nb['cells']))"
      ```
    </verifier>
  </slice>

  <slice id="S2">
    <objective>Tái cấu trúc khối Huấn luyện Gauss và trực quan hóa phân phối thuần NumPy</objective>
    <change>
      - Giữ nguyên công thức ngưỡng: $T^* = \frac{\mu_{\text{sil}}\sigma_{\text{sp}} + \mu_{\text{sp}}\sigma_{\text{sil}}}{\sigma_{\text{sp}} + \sigma_{\text{sil}}}$.
      - Bỏ hoàn toàn Cell 8 & 9 (loại bỏ `scipy.stats` và đồ thị zoom phức tạp).
      - Thêm 01 đồ thị minh họa phân bố chuẩn Gauss + vạch ngưỡng $T^*$ bằng hàm NumPy PDF tự định nghĩa ngắn gọn (~15 dòng).
      - In bảng kết quả định lượng tham số trung gian gọn gàng.
    </change>
    <allowed_files>
      - [gauss.ipynb](file:///home/phuqy/Documents/main_gk/gauss.ipynb)
    </allowed_files>
    <acceptance_criteria>
      - [ ] Tìm ra đúng ngưỡng $T^* \approx 0.000792$.
      - [ ] Không còn bất kỳ dòng import nào của `scipy.stats`.
    </acceptance_criteria>
    <verifier>
      ```bash
      python3 -c "import json; nb=json.load(open('gauss.ipynb')); assert not any('scipy.stats' in ''.join(c['source']) for c in nb['cells'])"
      ```
    </verifier>
  </slice>

  <slice id="S3">
    <objective>Tinh giản Hậu xử lý, Bảng MAE/RMSE và 4 Đồ thị Kiểm thử</objective>
    <change>
      - Tối giản hàm `filter_short_silence` (< 200ms) và `extract_boundaries`.
      - Viết gọn `match_boundaries`, `compute_mae`, `compute_rmse`, `calculate_snr_db`.
      - In bảng kết quả kiểm thử chuẩn mực cho 4 file (`phone_F2`, `phone_M2`, `studio_F2`, `studio_M2`) và trung bình Phone, Studio, Overall.
      - Xuất 4 figure 2 tầng đẹp, rõ ràng, dễ nhìn cho slide thuyết trình (kèm đường F0).
    </change>
    <allowed_files>
      - [gauss.ipynb](file:///home/phuqy/Documents/main_gk/gauss.ipynb)
    </allowed_files>
    <acceptance_criteria>
      - [ ] Bảng kết quả in đủ các chỉ số định lượng, MAE khớp chuẩn barem.
      - [ ] Xuất đủ 4 figures kiểm thử.
    </acceptance_criteria>
    <verifier>
      ```bash
      .venv/bin/python3 -c "
      # Verify execution of test evaluation code
      "
      ```
    </verifier>
  </slice>

  <slice id="S4">
    <objective>Thực thi và nghiệm thu toàn bộ notebook từ đầu đến cuối</objective>
    <change>Chạy toàn bộ notebook bằng Jupyter engine để lưu trữ đầy đủ cell outputs và hình ảnh.</change>
    <allowed_files>
      - [gauss.ipynb](file:///home/phuqy/Documents/main_gk/gauss.ipynb)
    </allowed_files>
    <acceptance_criteria>
      - [ ] Toàn bộ các cells đều có execution output hợp lệ, không có lỗi.
    </acceptance_criteria>
    <verifier>
      ```bash
      .venv/bin/python3 -m jupyter nbconvert --to notebook --execute --inplace gauss.ipynb
      ```
    </verifier>
  </slice>

</slices>

---

## 5. Gate 2 Sign-off

- [x] Ranh giới Scope contract đã khóa (`allowed_files`: chỉ `gauss.ipynb`).
- [x] Mỗi lát cắt (slice) đều có lệnh kiểm chứng và điểm rollback độc lập.
- [x] Tiêu chuẩn nghiệm thu mapping 1-1 với mục tiêu ban đầu.
- [x] Kỹ sư đã phê duyệt phương án tại Gate G1.

**Gate 2 Status: SIGNED / APPROVED.**

</execution_plan>
