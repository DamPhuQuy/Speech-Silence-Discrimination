# Research: FEAT-SLIDE-001 Speech/Silence Discrimination Presentation Deck

<research_context task_id="FEAT-SLIDE-001" version="2.1" framework="RIPER-5">

<!-- READ-ONLY PHASE. No source modifications. No implementation decisions. -->
<research_status>
  <phase>RESEARCH</phase>
  <mode>READ-ONLY</mode>
  <research_owner>@antigravity</research_owner>
  <last_updated>2026-10-07</last_updated>
  <halting_status>HALTED_COMPLETE</halting_status>
</research_status>

---

## 1. Current Behavior & Task Grounding

<current_behavior>
  Codebase đã hoàn tất quá trình cài đặt và thực nghiệm 3 thuật toán phân đoạn tiếng nói và khoảng lặng trong 3 Jupyter Notebooks độc lập:
  1. `binary.ipynb`: Thuật toán tìm kiếm nhị phân (Energy-based Binary Search - Hodgkinson 2012).
  2. `histogram.ipynb`: Thuật toán phân tích Histogram 2 đỉnh (Giannakopoulos 2014) trên log(STE).
  3. `simple_statistics.ipynb`: Thuật toán thống kê phân phối chuẩn Gaussian (Bayes thresholding).

  Cả 3 notebook đều đã chạy ra kết quả hoàn chỉnh:
  - Huấn luyện trên 4 file `TinHieuHuanLuyen` (`phone_F1`, `phone_M1`, `studio_F1`, `studio_M1`).
  - Kiểm thử trên 4 file `TinHieuKiemThu` (`phone_F2`, `phone_M2`, `studio_F2`, `studio_M2`).
  - Đã xuất đầy đủ đồ thị trực quan (waveform, STE/logSTE, ground truth vs predicted boundaries, F0 track) và bảng số liệu định lượng (MAE, RMSE, SNR).
  - Chưa có bộ slide thuyết trình (.pptx / .pdf) theo đúng phong cách thiết kế của template mẫu và quy định của giáo viên.
</current_behavior>

<task_grounding>
  <actual_intent>
    Tạo bộ slide thuyết trình chuẩn chỉnh phục vụ báo cáo thi giữa kỳ môn Xử lý tín hiệu số. Bài thuyết trình có thời lượng 3 phút, đòi hỏi súc tích, trực quan, không lý thuyết suông, kế thừa ngôn ngữ thiết kế của file mẫu `Digital vs. Analog Reliable Signal Science Presentation.pdf` (phong cách công nghệ Tech-HUD, tỷ lệ 16:9, bảng màu Cyan - Cam - Trắng - Xanh than), tuân thủ nghiêm ngặt quy định: <= 10 từ/dòng, <= 7 dòng/slide, font >= 18pt, số liệu và hình vẽ to rõ ràng.
  </actual_intent>
  <architectural_invariants>
    - Slide canvas: 16:9 widescreen (13.333" x 7.5").
    - Quy tắc font: Font chuẩn hỗ trợ tiếng Việt (Arial, Calibri, Segoe UI), tiêu đề >= 32pt, nội dung >= 18pt.
    - Quy tắc mật độ: Tối đa 7 dòng/slide, tối đa 10 từ/dòng.
    - Quy tắc nội dung giáo viên: Tuyệt đối không trình bày định nghĩa giáo trình; tập trung 100% vào sơ đồ khối giải pháp, giá trị ngưỡng tìm được, hình vẽ 4 file kiểm thử và bình luận đúng/sai định lượng.
    - Độ chính xác dữ liệu: Trích xuất chính xác 100% số liệu MAE, RMSE, SNR từ 3 notebook.
  </architectural_invariants>
  <negative_scope>
    - Không sửa đổi logic hoặc code trong các notebook gốc.
    - Không dùng các file âm thanh ngoài 4 file kiểm thử trong thư mục quy định.
  </negative_scope>
</task_grounding>

---

## 2. Source of Truth & Quy chuẩn Giảng viên (Rubric Analysis)

<source_of_truth_analysis>

| Văn bản / Nguồn | Nội dung quy định then chốt | Mức độ ràng buộc |
|---|---|---|
| `Hướng dẫn trình bày slide và nộp bài thi.pdf` | • Thời gian: 3 phút slide + 1 phút demo.<br>• Slide tập trung sơ đồ khối giải pháp, đồ thị, số liệu, bình luận.<br>• **KHÔNG trình bày lý thuyết và công thức**.<br>• Quy tắc chữ: **<= 10 từ/hàng, <= 7 hàng/slide, Font >= 18pt**.<br>• Dùng tất cả 4 file test trong `TinHieuKiemThu`.<br>• Minh họa kết quả trung gian (STE/logSTE), biên chuẩn (đỏ) & biên tìm được (xanh), đường F0.<br>• Có bình luận cho mỗi hình (đúng/sai nhiều/ít, vị trí, nguyên nhân).<br>• Nộp bản PDF của slide kèm source code. | Bắt buộc 100% (Tiêu chí chấm điểm trực tiếp) |
| `Hướng dẫn BT thi GK nhóm 3-4 SV...docx` | • Cố định: frame_len = 25ms, frame_shift = 10ms.<br>• Chiều dài khoảng lặng tối thiểu = 200ms.<br>• So sánh 3 thuật toán: Binary Search, Histogram, Simple Statistics.<br>• Đánh giá định lượng MAE và RMSE (ms), khảo sát ảnh hưởng SNR (dB). | Bắt buộc 100% |
| `Digital vs. Analog Reliable Signal Science Presentation.pdf` | • Phong cách: Sci-Fi / Cyber / Tech HUD.<br>• Màu sắc: Cyan `#00A8FF`, Cam `#F58220`, Nền trắng `#FFFFFF`, Viền xám đen `#0F172A`.<br>• Bố cục: Thẻ so sánh (comparison cards), HUD bracket viền góc, icon công nghệ. | Template chuẩn thẩm mỹ |

</source_of_truth_analysis>

---

## 3. Khảo sát & Tổng hợp Dữ liệu Thực nghiệm từ 3 Notebook

<notebook_evidence>

### 3.1 Tập dữ liệu Huấn luyện & Kiểm thử
- **Tập Huấn luyện (`data/TinHieuHuanLuyen`):** 4 file (`phone_F1`, `phone_M1`, `studio_F1`, `studio_M1`) $\rightarrow$ Dùng chung để tìm 01 ngưỡng tối ưu toàn cục.
- **Tập Kiểm thử (`data/TinHieuKiemThu`):** 4 file (`phone_F2`, `phone_M2`, `studio_F2`, `studio_M2`) $\rightarrow$ Đánh giá độc lập trên cả 4 file.

### 3.2 Thuật toán 1: Energy-based Binary Search (`binary.ipynb`)
- **Tài liệu tham khảo:** CS425 Audio and Speech Processing (Hodgkinson 2012), Mục 2.1.
- **Đặc trưng:** Năng lượng ngắn hạn chuẩn hóa $STE = \sum x^2[n]$.
- **Cơ chế:** Khởi tạo $T_0$ ở trung vị giữa min và max energy; lặp cập nhật $T_{k+1} = \frac{\mu_{sil}(T_k) + \mu_{sp}(T_k)}{2}$ cho đến khi $|T_{k+1} - T_k| < \epsilon$.
- **Kết quả huấn luyện:**
  - Hội tụ sau: **12 vòng lặp**.
  - Ngưỡng tối ưu toàn cục: **$T_{binary} = 0.000798$**.
  - Thống kê tập train: 497 khung Silence, 794 khung Speech.
- **Kết quả kiểm thử:**
  - `phone_F2` (Phone, SNR = 24.8 dB): MAE = **62.50 ms**, RMSE = **86.64 ms**
  - `phone_M2` (Phone, SNR = 27.0 dB): MAE = **7.50 ms**, RMSE = **9.01 ms**
  - `studio_F2` (Studio, SNR = 49.3 dB): MAE = **2.49 ms**, RMSE = **2.49 ms**
  - `studio_M2` (Studio, SNR = 37.7 dB): MAE = **12.49 ms**, RMSE = **12.49 ms**
  - **Trung bình Phone:** MAE = **35.00 ms**
  - **Trung bình Studio:** MAE = **7.49 ms**
  - **Toàn bộ 4 file:** MAE = **21.25 ms**

### 3.3 Thuật toán 2: Histogram Analysis (`histogram.ipynb`)
- **Tài liệu tham khảo:** A method for silence removal and segmentation (Giannakopoulos 2014).
- **Đặc trưng:** Logarit năng lượng ngắn hạn $\log(STE)$ chuẩn hóa (lấy log giúp nén dải động và tách biệt nhiễu nền).
- **Cơ chế:** Xây dựng Histogram với 40 bins, làm mịn; tìm 2 cực đại cục bộ: $M_1$ (đỉnh silence/noise) và $M_2$ (đỉnh speech); tính ngưỡng theo trọng số: $T = \frac{W \cdot M_1 + M_2}{W + 1}$ với $W = 2.0$.
- **Kết quả huấn luyện:**
  - Tổng số khung: 1291 khung.
  - Ngưỡng tối ưu toàn cục: **$T_{histogram} = -2.4375$** (trên thang $\log(STE)$).
- **Kết quả kiểm thử:**
  - `phone_F2` (Phone, SNR = 24.8 dB): MAE = **45.00 ms**, RMSE = **48.28 ms** (Cải thiện vượt trội so với Binary Search!)
  - `phone_M2` (Phone, SNR = 27.0 dB): MAE = **10.00 ms**, RMSE = **10.31 ms**
  - `studio_F2` (Studio, SNR = 49.3 dB): MAE = **2.49 ms**, RMSE = **2.49 ms**
  - `studio_M2` (Studio, SNR = 37.7 dB): MAE = **15.00 ms**, RMSE = **16.77 ms**
  - **Trung bình Phone:** MAE = **27.50 ms** (Thấp nhất trong 3 thuật toán)
  - **Trung bình Studio:** MAE = **8.75 ms**
  - **Toàn bộ 4 file:** MAE = **18.12 ms** (Hiệu suất tổng thể tốt nhất!)

### 3.4 Thuật toán 3: Simple Statistics / Gaussian Distribution (`simple_statistics.ipynb`)
- **Cơ chế:** Khảo sát các khung gán nhãn chuẩn từ file `.lab`; giả định phân phối STE của Sp và Sil tuân theo phân phối chuẩn Gaussian $N(\mu, \sigma^2)$; tìm ngưỡng giao điểm phân loại tối ưu Bayes: $T = \frac{\mu_{sil}\sigma_{sp} + \mu_{sp}\sigma_{sil}}{\sigma_{sil} + \sigma_{sp}}$.
- **Kết quả huấn luyện:**
  - Silence: $\mu_{sil} = 0.000249$, $\sigma_{sil} = 0.000634$
  - Speech: $\mu_{sp} = 0.202467$, $\sigma_{sp} = 0.235694$
  - Ngưỡng tối ưu toàn cục: **$T_{gaussian} = 0.000792$**.
- **Kết quả kiểm thử:**
  - `phone_F2` (Phone, SNR = 24.8 dB): MAE = **62.50 ms**, RMSE = **86.64 ms**
  - `phone_M2` (Phone, SNR = 27.0 dB): MAE = **7.50 ms**, RMSE = **9.01 ms**
  - `studio_F2` (Studio, SNR = 49.3 dB): MAE = **2.49 ms**, RMSE = **2.49 ms**
  - `studio_M2` (Studio, SNR = 37.7 dB): MAE = **12.49 ms**, RMSE = **12.49 ms**
  - **Trung bình Phone:** MAE = **35.00 ms**
  - **Trung bình Studio:** MAE = **7.49 ms**
  - **Toàn bộ 4 file:** MAE = **21.25 ms**

### 3.5 Bảng so sánh tổng hợp 3 Thuật toán trên Tập Kiểm thử

| Thuật toán | Ngưỡng $T$ | TB Phone MAE (ms) | TB Studio MAE (ms) | MAE Toàn bộ (ms) | Ưu thế & Đặc điểm |
|---|---|---|---|---|---|
| **1. Binary Search** | 0.000798 | 35.00 ms | **7.49 ms** | 21.25 ms | Đơn giản, hội tụ nhanh sau 12 bước, rất chính xác ở Studio |
| **2. Histogram log(STE)** | -2.4375 | **27.50 ms** | 8.75 ms | **18.12 ms** | **Kháng nhiễu tốt nhất**, tách biệt dải động, MAE thấp nhất |
| **3. Gaussian Statistics** | 0.000792 | 35.00 ms | **7.49 ms** | 21.25 ms | Cơ sở xác suất vững chắc, tương đồng Binary Search |

### 3.6 Phân tích nguyên nhân sai số & Ảnh hưởng môi trường (Bình luận kết quả)
1. **Ảnh hưởng của môi trường thu âm (SNR):**
   - Môi trường Studio (SNR cao 37.7 - 49.3 dB): Nền tĩnh lặng hoàn hảo, năng lượng silence cực nhỏ $\approx 0$. Cả 3 thuật toán đều đạt độ chính xác gần như tuyệt đối (sai số trên `studio_F2` chỉ **2.49 ms**, tức lệch dưới 1 frame!).
   - Môi trường Phone (SNR thấp 24.8 - 27.0 dB): Nhiễu môi trường và tiếng xì microphone làm năng lượng vùng silence dâng cao. Đặc biệt trên `phone_F2` (giọng nữ nhẹ, âm lượng biến thiên lớn), sai số biên đầu/cuối tăng lên (45 - 62 ms).
2. **Hiện tượng cắt phạm âm vô thanh (Unvoiced Speech):**
   - Các phụ âm vô thanh như /s/, /f/, /t/, /ch/ có năng lượng STE rất bé, dễ bị ngưỡng năng lượng đơn lẻ coi là khoảng lặng.
   - Giải pháp đề xuất mở rộng: Bổ sung đặc trưng Tần số qua điểm không (Zero-Crossing Rate - ZCR) để tạo bộ phát hiện ngưỡng kép Dual-Threshold STE + ZCR.

</notebook_evidence>

---

## 4. Ngôn ngữ Thiết kế Template (Visual Identity Analysis)

<template_design_analysis>
  Dựa trên phân tích 13 trang của `Digital vs. Analog Reliable Signal Science Presentation.pdf`:
  - **Canvas:** Tỷ lệ chuẩn 16:9 widescreen (10" x 5.625" hoặc 13.333" x 7.5").
  - **Bảng màu chủ đạo (Tech Signal Theme):**
    - Cyan Electric: `#00A8FF` (Thanh bar dưới, tiêu đề chính, điểm nhấn công nghệ).
    - Vivid Amber / Orange: `#F58220` (Thanh bar trên, badge highlight, ngưỡng threshold).
    - Dark Border / Slate: `#0F172A` / `#1E293B` (Khung viền, viền thẻ so sánh, HUD frame).
    - Canvas Background: `#FFFFFF` (Nền trắng sạch, tương phản cao, hiện đại).
    - Text Body: `#0F172A` (Độ tương phản WCAG AAA vượt trội trên nền trắng).
  - **Họa tiết trang trí (Motif):**
    - HUD Tech Frame: Khung viền góc vát công nghệ bao quanh slide hoặc thẻ nội dung.
    - Status Badge: Các ô bo tròn/viên thuốc màu Cyan/Cam làm nhãn nổi bật (vd: `[STUDIO: 49.3 dB]`, `[MAE: 2.49 ms]`).
    - Two-column / Multi-column Comparison Cards: So sánh trực quan giữa các đối tượng.
  - **Đảm bảo quy tắc GV:**
    - Font size: Tiêu đề 32-38pt bold, nội dung chính 18-22pt bold/medium.
    - Mật độ: 4 - 6 hàng/slide, mỗi hàng 6 - 9 từ.
</template_design_analysis>

---

## 5. Danh mục Hình vẽ Cần chuẩn hóa cho Slide

<visual_assets>
  Để đảm bảo slide có hình ảnh sắc nét, to rõ ràng theo đúng yêu cầu GV:
  - `fig_pipeline.png`: Sơ đồ khối quy trình phân đoạn 5 bước.
  - `fig_tt1_binary_flow.png`: Sơ đồ khối thuật toán tìm kiếm nhị phân.
  - `fig_tt2_histogram_flow.png`: Sơ đồ khối & đồ thị 2 đỉnh Histogram Giannakopoulos.
  - `fig_tt3_gaussian_flow.png`: Sơ đồ khối & đường cong phân phối xác suất Gauss.
  - `fig_test_binary_4files.png`: Đồ thị 4 file kiểm thử của TT1 (tổng hợp 4 góc).
  - `fig_test_histogram_4files.png`: Đồ thị 4 file kiểm thử của TT2 (tổng hợp 4 góc).
  - `fig_test_gaussian_4files.png`: Đồ thị 4 file kiểm thử của TT3 (tổng hợp 4 góc).
  - `fig_snr_comparison.png`: Biểu đồ so sánh MAE giữa 3 thuật toán theo môi trường Phone vs Studio.
</visual_assets>

---

## 6. Halting Predicate & Exit Criteria (Gate G0)

<halting_verification>
  - [x] **L_known (Localization):** Đã định vị chính xác toàn bộ 3 notebook, dữ liệu âm thanh và nhãn groundtruth trong `data/`, cùng quy định trong `docs/assignments/`.
  - [x] **B_understood (Behavior):** Đã giải mã cơ chế hoạt động, công thức xác định ngưỡng và phân tích sâu sắc kết quả kiểm thử của cả 3 thuật toán.
  - [x] **C_known (Constraints):** Nắm rõ 100% ràng buộc khắt khe của giảng viên: thời lượng 3 phút, font >= 18pt, <= 7 dòng, <= 10 từ/dòng, không lý thuyết suông, hình ảnh to rõ.
  - [x] **P_checked (Patterns):** Đã trích xuất cấu trúc mỹ thuật từ `Digital vs. Analog Reliable Signal Science Presentation.pdf` (HUD frame, Cyan `#00A8FF`, Orange `#F58220`, nền trắng).
  - [x] **V_known (Verification):** Đã xác định cơ chế kiểm thử: render `.pptx` qua `pptxgenjs`, chuyển đổi sang `.pdf` qua LibreOffice và xuất ảnh PNG qua `pdftoppm` để visual QA.
</halting_verification>

Gate G0 Complete: Đã hoàn tất phase RESEARCH. Sẵn sàng báo cáo người dùng trong chế độ PAIR để chuyển sang phase INNOVATE.

</research_context>
