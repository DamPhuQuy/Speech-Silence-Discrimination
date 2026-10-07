# Research: FEAT-GAUSS-01 Khảo Sát Tái Cấu Trúc và Tối Giản Cơ Chế gauss.ipynb

<research_context task_id="FEAT-GAUSS-01" version="2.1" framework="RIPER-5">

<!-- READ-ONLY PHASE. No source modifications. No implementation decisions. -->
<research_status>
  <phase>RESEARCH</phase>
  <mode>READ-ONLY</mode>
  <research_owner>@antigravity</research_owner>
  <last_updated>2026-10-06</last_updated>
  <halting_status>HALTED_COMPLETE</halting_status>
</research_status>

---

## 1. Current Behavior & Task Grounding

<current_behavior>
  Hiện tại, [gauss.ipynb](file:///home/phuqy/Documents/main_gk/gauss.ipynb) thực hiện phân đoạn tiếng nói / khoảng lặng theo mô hình phân phối chuẩn Gauss qua 15 cells:
  1. Nạp và tiền xử lý tín hiệu: Sử dụng dataclass `AudioSignal` với nhiều trường dữ liệu và bộ parser `.lab` phòng thủ (đọc cả f0mean/f0std).
  2. Trích xuất đặc trưng: Tính năng lượng ngắn hạn `STE`, chuẩn hóa `normalize_minmax` và hàm ước lượng `estimate_f0_track` bằng tự tương quan (autocorrelation).
  3. Huấn luyện tìm ngưỡng:
     - Tập hợp `all_ste` và `all_labels` từ 4 file `TinHieuHuanLuyen`.
     - Tính trung bình và độ lệch chuẩn của Speech ($\mu_{\text{sp}}, \sigma_{\text{sp}}$) và Silence ($\mu_{\text{sil}}, \sigma_{\text{sil}}$).
     - Áp dụng công thức ngưỡng:
       $$T = \frac{\mu_{\text{sil}} \cdot \sigma_{\text{sp}} + \mu_{\text{sp}} \cdot \sigma_{\text{sil}}}{\sigma_{\text{sp}} + \sigma_{\text{sil}}}$$
       kết quả tìm được $T^* \approx 0.000792$.
  4. Cell 8 & 9 (Mục 3.1): Một khối mã dài 112 dòng (đang uncommitted) sử dụng `import scipy.stats as stats` để vẽ biểu đồ 2 panel (toàn cảnh + zoom sát ngưỡng $0.0035$), cố gắng giải thích hình dạng chuông Gauss do phân bố năng lượng STE bị lệch quá mạnh về 0.
  5. Hậu xử lý & Đánh giá: Bộ lọc khoảng lặng ngắn $< 200\text{ ms}$, thuật toán ghép cặp biên 1-1 (greedy bipartite matching), tính MAE/RMSE trên 4 file `TinHieuKiemThu`.
  6. Trực quan hóa: Vòng lặp vẽ 4 biểu đồ 2 tầng cho từng file kiểm thử (Dạng sóng + Ground Truth + Biên GT/Pred và STE + Ngưỡng + Biên + Đường F0).
</current_behavior>

<task_grounding>
  <actual_intent>
    Tối giản hóa toàn diện notebook [gauss.ipynb](file:///home/phuqy/Documents/main_gk/gauss.ipynb) sao cho:
    - Rút gọn tối đa (loại bỏ code dư thừa, code phòng thủ không cần thiết, bỏ thư viện ngoài `scipy.stats`).
    - Dễ hiểu nhất: Luồng thực thi thẳng tắp, cấu trúc rõ ràng, sinh viên có thể trình bày lưu loát trong 3 phút mà giảng viên nhìn vào hiểu ngay ý tưởng và công thức.
    - Đảm bảo đầy đủ 100% yêu cầu đề bài: Đúng quy chuẩn khung (25ms/10ms), lọc khoảng lặng $< 200\text{ ms}$, đủ bảng đánh giá định lượng (MAE/RMSE theo ms) và xuất đủ 4 figure kiểm thử kèm đường F0 theo hướng dẫn slide.
  </actual_intent>
  <architectural_invariants>
    - Kích thước khung 25 ms, bước nhảy 10 ms, lấy mốc thời gian tại tâm khung.
    - Bộ lọc khoảng lặng ảo $< 200\text{ ms}$ là bắt buộc tuyệt đối.
    - Không can thiệp các file khác ([binary.ipynb](file:///home/phuqy/Documents/main_gk/binary.ipynb), [histogram.ipynb](file:///home/phuqy/Documents/main_gk/histogram.ipynb)).
    - Chỉ sử dụng Python chuẩn và NumPy built-ins (không dùng toolbox chuyên dụng / scipy.stats).
  </architectural_invariants>
  <negative_scope>
    - Không tự ý thêm bộ lọc tiếng nói ngắn (`filter_short_speech`).
    - Không thay đổi dữ liệu WAV và LAB trong `data/`.
  </negative_scope>
</task_grounding>

---

## 2. "Trace before Design" Protocol & Execution Flows

<trace_before_design>

### 2.1 Happy Path Flow
```text
TinHieuHuanLuyen (4 file WAV + LAB)
  → Đọc tín hiệu + nhãn Speech/Silence
  → Phân khung 25ms/10ms + Tính STE + Chuẩn hóa Min-Max [0, 1]
  → Tách tập frame Speech (nhãn 1) và Silence (nhãn 0)
  → Ước lượng (mean_sil, std_sil, mean_sp, std_sp) bằng np.mean & np.std
  → Tính ngưỡng T* = (mean_sil * std_sp + mean_sp * std_sil) / (std_sp + std_sil)
  → Vẽ 01 biểu đồ phân phối Gauss + Histogram rút gọn minh họa ngưỡng
TinHieuKiemThu (4 file WAV + LAB)
  → Tính STE_norm + Ước lượng F0
  → Quyết định frame >= T* → Lọc silence < 200ms → Trích xuất mốc biên
  → Đánh giá MAE & RMSE trên các biên khớp 1-1
  → In bảng tổng hợp số liệu
  → Xuất 4 figure 2 tầng (Dạng sóng + Biên; STE + Ngưỡng + F0)
```

### 2.2 Error & Rollback Path Flow
```text
Lỗi đọc file hoặc không tìm thấy nhãn .lab
  → Fallback đường dẫn tìm kiếm trực tiếp trong 'data/'
Khung tín hiệu không có tiếng nói / không có khoảng lặng
  → Tránh chia cho 0: denominator = (std_sp + std_sil); nếu denom == 0 fallback (mean_sil + mean_sp)/2
Lỗi sai số đánh giá (không có biên dự đoán hoặc không khớp biên nào)
  → Trả về MAE = 0.0 ms hoặc báo Miss 100% an toàn không gây crash
```

### 2.3 Data-Flow Slices (Def-Use Chains)
- **Chuỗi tính ngưỡng Gauss:**
  `train_signals` $\rightarrow$ `frames` (line 173) $\rightarrow$ `compute_ste` (line 197) $\rightarrow$ `normalize_minmax` (line 204) $\rightarrow$ `silence_values, speech_values` $\rightarrow$ `np.mean(), np.std()` $\rightarrow$ `T_gaussian` (line 294).
- **Chuỗi phân đoạn & lọc:**
  `test_signals` $\rightarrow$ `ste_norm` $\rightarrow$ `raw_decisions = (ste_norm >= T_gaussian)` $\rightarrow$ `filter_short_silence(raw_decisions)` (line 497) $\rightarrow$ `extract_boundaries` (line 527) $\rightarrow$ `match_boundaries` (line 553) $\rightarrow$ `compute_mae, compute_rmse`.
</trace_before_design>

---

## 3. Constraint & Invariant Discovery

- **Quy chuẩn mã nguồn theo đề bài:**
  1. Không sử dụng thư viện xử lý tín hiệu ngoại trừ các hàm built-in của Numpy (`np.max`, `np.min`, `np.sum`, `np.mean`, `np.std`).
  2. Việc sử dụng `scipy.stats.norm.pdf` ở Cell 9 hiện tại vi phạm tinh thần này; có thể thay thế bằng công thức giải tích chuẩn Gauss bằng NumPy nếu muốn vẽ đường cong mật độ xác suất:
     $$f(x; \mu, \sigma) = \frac{1}{\sigma \sqrt{2\pi}} \exp\left(-\frac{(x - \mu)^2}{2\sigma^2}\right)$$
  3. Cần có comment mô tả ngắn gọn cho từng khối code (5-10 dòng) để sinh viên dễ trình bày.
  4. Trình tự chạy notebook: Run All một lần từ đầu đến cuối là hoàn tất mọi bảng số liệu và hình vẽ.

---

## 4. Component Inventory & Key Anchor Code Snippets

| Thành phần | Vị trí hiện tại | Hiện trạng & Đánh giá | Đề xuất tối giản |
|---|---|---|---|
| `AudioSignal` & Loaders | Lines 61–168 | Rườm rà (quét 4 cấp thư mục, kiểm tra uint8, dataclass 8 trường) | Rút gọn thành dataclass đơn giản 5 trường, đọc file trực tiếp từ `data/` |
| `estimate_f0_track` | Lines 218–255 | 37 dòng autocorrelation | Giữ nguyên thuật toán tự tương quan nhưng viết gọn, loại bỏ các biến trung gian thừa |
| `find_threshold_gaussian` | Lines 286–330 | Tính $\mu, \sigma$ và $T$ | Rất tốt, giữ nguyên công thức $T = \frac{\mu_{sil}\sigma_{sp} + \mu_{sp}\sigma_{sil}}{\sigma_{sp} + \sigma_{sil}}$, làm sạch code |
| Mục 3.1 (Cell 8 & 9) | Lines 335–490 | 155 dòng! Dùng `scipy.stats`, đồ thị 2 panel với zoom cực phức tạp | **Thay đổi cơ chế hiển thị**: Thay bằng 1 figure trực quan duy nhất (Histogram + Đồ thị Gauss thuần NumPy), loại bỏ hoàn toàn `scipy.stats` |
| Hậu xử lý & Ghép biên | Lines 497–620 | 123 dòng, thuật toán ghép biên dài | Tinh giản logic, gom gọn các hàm tính toán sai số |
| Đánh giá & Vẽ đồ thị Test | Lines 625–840 | 215 dòng, bảng in đẹp, vẽ 4 figure | Chuẩn hóa, làm sạch các đoạn cấu hình matplotlib dài dòng |

---

## 5. Side-Effects & Breaking Changes Risk Matrix

| Thay đổi | Rủi ro | Mức độ | Biện pháp kiểm soát |
|---|---|---|---|
| Bỏ `scipy.stats` | Lỗi cú pháp khi vẽ phân phối | Thấp | Tự cài hàm Gauss mật độ xác suất bằng NumPy (`1/(s*sqrt(2pi)) * exp(...)`) |
| Tinh giản Cell 9 | Mất hình minh họa phân phối Gauss | Thấp | Tạo đồ thị phân phối kết hợp histogram súc tích, hiển thị trực tiếp trong notebook thay vì vẽ 2 panel phức tạp |
| Rút gọn cấu trúc nạp dữ liệu | Không tìm thấy file | Rất thấp | Giữ đường dẫn `Path("data") / folder_name` mặc định chuẩn |

---

## 6. Source-of-Truth Analysis & Epistemic Ledger

<epistemic_ledger>
- **Confirmed (Đã xác minh chắc chắn):**
  - Công thức ngưỡng Gauss $T = \frac{\mu_{\text{sil}}\sigma_{\text{sp}} + \mu_{\text{sp}}\sigma_{\text{sil}}}{\sigma_{\text{sp}} + \sigma_{\text{sil}}}$ là chuẩn mực, cho ra $T^* \approx 0.000792$, phân đoạn tốt với MAE $\approx 21.25\text{ ms}$.
  - Giảng viên yêu cầu tự code, không dùng toolbox ngoài, ưu tiên NumPy.
  - Hướng dẫn slide yêu cầu 4 figure trên 4 file kiểm thử có đường F0.
- **Observed (Quan sát thấy):**
  - Notebook hiện tại phình to do Cell 9 uncommitted cố giải thích hình dạng phân phối bằng 112 dòng code phức tạp.
- **Hypothesized (Giả thuyết giải pháp):**
  - Tinh giản toàn bộ notebook về khoảng 8-10 cells trong sáng, loại bỏ hoàn toàn `scipy.stats`, giữ nguyên vẹn logic toán học cốt lõi sẽ giúp bài làm ngắn gọn nhất, dễ hiểu nhất và đạt điểm tối đa.
</epistemic_ledger>

---

## 7. Assumptions & Uncertainties Catalog

- **Giả định 1:** Sinh viên muốn giữ công thức ngưỡng giao điểm chuẩn hóa $T = \frac{\mu_{\text{sil}}\sigma_{\text{sp}} + \mu_{\text{sp}}\sigma_{\text{sil}}}{\sigma_{\text{sp}} + \sigma_{\text{sil}}}$ vì công thức này đã được công nhận trong đề bài và báo cáo nhóm.
- **Giả định 2:** Đồ thị minh họa cơ chế Gauss ở phần huấn luyện chỉ cần 01 đồ thị trực quan duy nhất (phân phối xác suất + histogram thực nghiệm + vạch ngưỡng $T^*$) thay vì 2 panel zoom phức tạp.

---

## 8. Deterministic Research Halting Predicate (Gate G0)

- [x] **$L_{\text{known}}$:** Vị trí các tệp liên quan đã được định vị chính xác ([gauss.ipynb](file:///home/phuqy/Documents/main_gk/gauss.ipynb), [task.md](file:///home/phuqy/Documents/main_gk/process/features/active/simplify-gauss-mechanism/task.md)).
- [x] **$B_{\text{understood}}$:** Hành vi hiện tại và sự cồng kềnh của notebook đã được mổ xẻ chi tiết từng dòng.
- [x] **$C_{\text{known}}$:** Các ràng buộc bất biến (quy chuẩn 25ms/10ms, lọc silence < 200ms, không dùng toolbox ngoài) đã được xác nhận.
- [x] **$P_{\text{checked}}$:** Quy trình huấn luyện và kiểm thử đã được vạch rõ.
- [x] **$V_{\text{known}}$:** Tiêu chí nghiệm thu và công cụ kiểm thử tự động đã sẵn sàng.

**Kết luận Gate G0: ĐẠT (HALTED_COMPLETE).**

</research_context>
