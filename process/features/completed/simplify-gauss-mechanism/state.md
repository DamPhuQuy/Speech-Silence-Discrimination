# State: FEAT-GAUSS-01 Tối Giản và Chuẩn Hóa Cơ Chế gauss.ipynb

<loop_state task_id="FEAT-GAUSS-01" version="2.0" framework="RIPER-5">

<!-- Living Scratchpad & Persistent Memory of the Execute loop. Update after every slice to prevent goal drift (OWASP ASI10). -->
<state_header>
  <current_phase>EXECUTE</current_phase>
  <current_gate>G2</current_gate>
  <last_updated>2026-10-06</last_updated>
</state_header>

---

## 1. Task

<task_ref>
  <task_spec>[task.md](file:///home/phuqy/Documents/main_gk/process/features/active/simplify-gauss-mechanism/task.md)</task_spec>
  <plan>[plan.md](file:///home/phuqy/Documents/main_gk/process/features/active/simplify-gauss-mechanism/plan.md)</plan>
</task_ref>

---

## 2. Goal & Invariants

<goal_and_invariants>
  <goal>Tái cấu trúc và tối giản hóa gauss.ipynb theo Phương án A (thuần NumPy, loại bỏ Cell 8-9 cồng kềnh, giữ vững tính chính xác và đầy đủ yêu cầu).</goal>
  <invariants>
    - Kích thước khung 25ms, độ dịch khung 10ms, tâm khung.
    - Lọc khoảng lặng < 200ms.
    - Không sử dụng scipy.stats hoặc toolbox ngoài.
    - Đầy đủ 4 figure kiểm thử kèm đường F0.
  </invariants>
</goal_and_invariants>

---

## 3. Approved Decisions

<approved_decisions>
  - DEC-GAUSS-01: Lựa chọn Option A (Tinh giản cực đại & thuần NumPy). Bỏ Cell 8-9 rườm rà, vẽ 1 đồ thị phân phối Gauss tinh gọn.
</approved_decisions>

---

## 4. Completed Slices

<completed_slices>
  | Slice | Status | Atomic Commit | Verifier Result | Evidence |
  |---|---|---|---|---|
  | S1: Data Loading & Features | DONE | local | PASS | Nạp 4 file huấn luyện, trích xuất STE & F0 thành công |
  | S2: Gauss Training & NumPy Plot | DONE | local | PASS | Ngưỡng T = 0.000791, 0 scipy.stats, biểu đồ NumPy sạch |
  | S3: Postprocessing & Metrics Table | DONE | local | PASS | MAE/RMSE khớp 100% chuẩn: Phone 35ms, Studio 7.494ms |
  | S4: Full Notebook Execution | DONE | local | PASS | Toàn bộ 16 cells chạy thành công và lưu đầy đủ figures |
</completed_slices>

---

## 5. Current Slice

<current_slice>
  <id>S4</id>
  <objective>Hoàn tất nghiệm thu và chuyển sang REVIEW</objective>
  <status>DONE</status>
</current_slice>

---

## 6. Next Steps

- Thực hiện tái cấu trúc `gauss.ipynb`:
  1. Header markdown và imports (chỉ import standard: os, sys, warnings, dataclass, Path, plt, np, wav).
  2. Section 1: Tiền xử lý & Nạp dữ liệu (dataclass AudioSignal gọn gàng, preprocessing, parse_lab, load_dataset).
  3. Section 2: Trích xuất đặc trưng STE & F0 (apply_framing, compute_ste, normalize_minmax, estimate_f0_track).
  4. Section 3: Huấn luyện tìm ngưỡng Gauss (find_threshold_gaussian, tính all_ste & all_labels, tính T_gaussian).
  5. Section 3.1: Bảng kết quả định lượng tham số trung gian & Đồ thị phân phối chuẩn Gauss thuần NumPy (tự cài hàm PDF 2 dòng bằng NumPy, vẽ histogram + đường cong phân phối + vạch ngưỡng T*).
  6. Section 4: Hậu xử lý & Đánh giá (filter_short_silence, extract_boundaries, match_boundaries, compute_mae, compute_rmse, calculate_snr_db).
  7. Section 5: Đánh giá trên tập kiểm thử (in bảng MAE/RMSE đầy đủ).
  8. Section 6: Trực quan hóa 4 hình ảnh kiểm thử (Waveform + Vùng chuẩn + Biên GT/Pred; STE + Ngưỡng + Biên + F0).
  9. Section 7: Nhận xét & Bình luận kết quả.
- Chạy nghiệm thu `gauss.ipynb`.

</loop_state>
