# Research: RES-GAUSS-SLIDE-01 Khảo Sát Kiến Trúc Template Slide & Tích Hợp Dữ Liệu Gaussian

<research_artifact task_id="FEAT-GAUSS-SLIDE-01" version="2.0" framework="RIPER-5">

<!-- ════════════════════════════════════════════
     PHASE 1: RESEARCH — INVESTIGATION ONLY
     EXECUTION tool group is hard-locked.
     ════════════════════════════════════════════ -->

## 1. Executive Summary & Problem Understanding

Nhiệm vụ của bài toán là xây dựng bộ slide thuyết trình chuyên sâu, cô đọng (4-5 slide) báo cáo về **Thuật toán 3: Phân phối chuẩn Gauss (Simple Statistics / Bayes Quadratic)** trong đồ án môn học Xử lý tín hiệu số (XLTHS 2026).
Yêu cầu cốt lõi:
1. **Chuẩn hóa Template:** Kế thừa 100% phong cách thiết kế, tỷ lệ màn hình 16:9, hệ màu và typography từ file mẫu [Digital vs. Analog Reliable Signal Science Presentation.pptx](file:///home/phuqy/Documents/main_gk/Digital%20vs.%20Analog%20Reliable%20Signal%20Science%20Presentation.pptx).
2. **Chuẩn hóa Số liệu & Hình ảnh:** Tích hợp dữ liệu thực nghiệm đã kiểm chứng từ [simple_statistics.ipynb](file:///home/phuqy/Documents/main_gk/simple_statistics.ipynb), với ngưỡng Bayes bậc hai $T^* = 0.002495$, các tham số phân phối Gauss $\mu_{\text{sil}}, \sigma_{\text{sil}}, \mu_{\text{sp}}, \sigma_{\text{sp}}$, bảng sai số định lượng MAE/RMSE trên 4 file kiểm thử (`phone_F2`, `phone_M2`, `studio_F2`, `studio_M2`) và phân tích âm học `Err Start`/`Err End`.
3. **Tuân thủ Tiêu chí Chấm thi của Giảng viên:** $\le 7$ dòng chữ/slide, $\le 10$ từ/dòng, font size $\ge 18\text{pt}$, màu chữ tương phản cao trên nền sáng, tập trung vào sơ đồ, đồ thị và giải thích bản chất âm học trong thời lượng 3 phút.

---

## 2. Repo Map & Tri-Search Analysis

### 2.1. Nguồn Dữ Liệu Thực Nghiệm
* [simple_statistics.ipynb](file:///home/phuqy/Documents/main_gk/simple_statistics.ipynb):
  * Cell 6: Huấn luyện toàn cục trên 4 file `TinHieuHuanLuyen`, tìm tham số Gauss và giải nghiệm phương trình Bayes Quadratic:
    * $\mu_{\text{sil}} = 0.000249, \sigma_{\text{sil}} = 0.000634$
    * $\mu_{\text{sp}} = 0.202467, \sigma_{\text{sp}} = 0.235694$
    * Ngưỡng tối ưu $T^* = 0.002495$.
  * Cell 7: Đồ thị mật độ xác suất PDF (2 Subplots) minh họa toàn cảnh hình chuông và cận cảnh điểm giao nhau Bayes $T^*$.
  * Cell 11: Bảng tổng hợp định lượng kết quả kiểm thử trên 4 file:
    * `phone_F2` (Phone): SNR $24.8\text{ dB}$ | MAE $27.5000\text{ ms}$ | RMSE $37.1652\text{ ms}$ | Err Start $2.5\text{ ms}$ | Err End $52.5\text{ ms}$
    * `phone_M2` (Phone): SNR $27.0\text{ dB}$ | MAE $2.5000\text{ ms}$ | RMSE $2.5000\text{ ms}$ | Err Start $2.5\text{ ms}$ | Err End $2.5\text{ ms}$
    * `studio_F2` (Studio): SNR $49.3\text{ dB}$ | MAE $5.0000\text{ ms}$ | RMSE $5.5929\text{ ms}$ | Err Start $2.5\text{ ms}$ | Err End $7.5\text{ ms}$
    * `studio_M2` (Studio): SNR $37.7\text{ dB}$ | MAE $12.4940\text{ ms}$ | RMSE $16.0031\text{ ms}$ | Err Start $22.5\text{ ms}$ | Err End $2.5\text{ ms}$
    * **TB Phone (2 file):** MAE $15.0000\text{ ms}$ | RMSE $19.8326\text{ ms}$
    * **TB Studio (2 file):** MAE $8.7470\text{ ms}$ | RMSE $10.7980\text{ ms}$
    * **Toàn bộ (4 file):** MAE $11.8735\text{ ms}$ | RMSE $15.3153\text{ ms}$
  * Cell 12: 4 đồ thị 2 tầng (Dạng sóng + Biên GT/Thuật toán; STE + Ngưỡng + F0).

### 2.2. Khảo Sát Template Gốc
* [Digital vs. Analog Reliable Signal Science Presentation.pptx](file:///home/phuqy/Documents/main_gk/Digital%20vs.%20Analog%20Reliable%20Signal%20Science%20Presentation.pptx):
  * **Kích thước Canvas:** `cx = 18288000 EMU` ($20.0\text{ inches} = 1440\text{ pt}$), `cy = 10287000 EMU` ($11.25\text{ inches} = 810\text{ pt}$). Tỷ lệ màn chiếu 16:9.
  * **Bảng màu chủ đạo (Color Palette):**
    * Cyan / Electric Blue: `#00BCD4` / `#00A8FF`
    * Vibrant Orange / Amber: `#FF9800` / `#F58220`
    * Deep Slate / Charcoal: `#0F172A` / `#333333`
    * Clean White Canvas: `#FFFFFF`
  * **Font chữ (Typography):** Calibri / Arial sạch sẽ, hiện đại.
  * **Cấu trúc Slide hiện có:**
    * Slide 1: Bìa đề tài ("PHÂN ĐOẠN TIẾNG NÓI VÀ KHOẢNG LẶNG", "NHÓM 14").
    * Slide 2: Sơ đồ 4 STAGE tròn/thanh ngang (hiện là nội dung mẫu tiếng Malay/Indo).
    * Slide 3: Đồ thị phân phối chuẩn Gauss (`image18.png`) kèm 2 dòng chú thích.
    * Slide 4: Slide trống (Blank slide).
    * Slide 5: Ghép 4 đồ thị kiểm thử (`image19.png` -> `image22.png`) kèm 4 ghi chú sai số.
    * Slide 6-16: Các slide lý thuyết cũ về Tín hiệu Analog vs Digital.

---

## 3. Relation Tracing & Data-Flow Slicing

```
[simple_statistics.ipynb]
   │
   ├─► Cell 6: Tham số Gauss (mu, sigma) & T* = 0.002495 ─────► Slide 3 (Huấn luyện & Ngưỡng)
   ├─► Cell 7: Đồ thị PDF 2 chuông Gauss (image18.png) ────────► Slide 3 (Trực quan hóa PDF)
   │
   ├─► Cell 8: Logic 4 bước (Framing, STE, Bayes, Postprocess) ─► Slide 2 (Quy trình 4 STAGE)
   │
   ├─► Cell 11: Bảng số liệu MAE/RMSE/SNR/Bounds ──────────────► Slide 4 (Bảng Định Lượng)
   │
   └─► Cell 12: 4 Figure kiểm thử (image19 - image22) ─────────► Slide 5 (Trực quan hóa & Âm học)
```

---

## 4. Behavioral Evidence & Empirical Findings

### 4.1. Nhược Điểm của File PPTX Hiện Tại
1. Slide 2 chứa văn bản mẫu không liên quan (`Initiation`, `Planning`, `Execution`, `Closure` bằng tiếng Malay/Indo).
2. Slide 3 thiếu tiêu đề rõ ràng, mô tả quá ngắn gọn chưa làm nổi bật cơ sở lý thuyết Bayes Quadratic.
3. Slide 4 hoàn toàn trống, trong khi đây là vị trí bắt buộc phải có **Bảng kết quả định lượng tổng hợp** theo tiêu chuẩn báo cáo khoa học.
4. Slide 5 mới chỉ liệt kê câu chữ tản mạn, chưa có cấu trúc phân tích âm học `Err Start` vs `Err End` để chỉ rõ tại sao `phone_F2` bị sai số ở biên cuối và `studio_M2` bị sai số ở biên đầu.
5. Slides 6 đến 16 là nội dung thừa của template Canva ban đầu, làm loãng bài thuyết trình 3 phút.

### 4.2. Giải Pháp Tinh Chỉnh Bố Cục 5 Slide
* **Slide 1 (Cover):** Tên đề tài, Thuật toán Gaussian Bayes, Sinh viên/Nhóm thực hiện.
* **Slide 2 (Sơ đồ 4 Giai đoạn):** Tận dụng layout 4 STAGE tuyệt đẹp của template để mô tả:
  * STAGE 01: Phân khung & Tính Năng lượng STE chuẩn hóa.
  * STAGE 02: Ước lượng Tham số Phân phối Gauss ($\mu, \sigma$).
  * STAGE 03: Xác định Ngưỡng Bayes Quadratic Tối ưu $T^*$.
  * STAGE 04: Hậu xử lý Khử Khoảng lặng Ảo & Đánh giá.
* **Slide 3 (Huấn luyện & Điểm Giao nhau Gauss):** Giữ hình `image18.png`, bổ sung bảng tham số $\mu, \sigma$ của Silence/Speech và giải thích nghiệm $T^* = 0.002495$.
* **Slide 4 (Bảng Tổng Hợp Kết Quả Định Lượng):** Dựng bảng số liệu 5 cột chuyên nghiệp (Tên File, Môi trường, SNR, MAE, RMSE) kèm các chỉ số trung bình Studio, Phone và Toàn bộ.
* **Slide 5 (Trực Quan Hóa & Phân Tích Âm Học):** Giữ 4 đồ thị kiểm thử, bổ sung bảng phân tích `Err Start` và `Err End` giải thích hiện tượng âm học ở kênh điện thoại vs phòng thu sạch.
* **Loại bỏ Slide 6 - 16** để tinh gọn file thành đúng 5 slide chuẩn.

---

## 5. Constraints, Invariants & Risk Matrix

| Rủi ro / Thách thức | Mức độ | Biện pháp kiểm soát & Hóa giải |
| :--- | :---: | :--- |
| Chữ quá nhỏ (< 18pt) bị trừ điểm | Cao | Thiết lập font size $\ge 18\text{pt}$ cho toàn bộ bullet points và tiêu đề phụ, $\ge 24\text{pt}$ cho tiêu đề chính. |
| Quá nhiều chữ (> 7 dòng/slide) | Cao | Áp dụng cấu trúc 3-5 gạch đầu dòng ngắn gọn, $\le 10$ từ/dòng. |
| Làm hỏng cấu trúc XML của PPTX khi chỉnh sửa | Trung bình | Sử dụng kỹ thuật giải nén XML chuẩn hoặc script `pptxgenjs`/Python OpenXML đã được validate. |
| Số liệu lệch so với notebook [simple_statistics.ipynb](file:///home/phuqy/Documents/main_gk/simple_statistics.ipynb) | Cao | Khóa số liệu chuẩn từ kết quả chạy thực tế: $T^* = 0.002495$, MAE Studio $8.7\text{ ms}$, MAE Phone $15.0\text{ ms}$, Toàn bộ $11.9\text{ ms}$. |

---

## 6. Epistemic Ledger

* **Đã Xác Nhận (Confirmed):**
  * Template PPTX có canvas 16:9 ($1440 \times 810\text{ pt}$).
  * Đồ thị phân phối chuẩn Gauss và 4 đồ thị kiểm thử đã có sẵn trong file dưới dạng `image18.png` đến `image22.png`.
  * Notebook `simple_statistics.ipynb` đã hoàn thiện và chạy sạch Cell 0 -> Cell 12.
* **Đã Quan Sát (Observed):**
  * Slide 4 bị bỏ trống; Slide 2 mang nội dung placeholder; Slide 6-16 là rác template.
* **Giả Thuyết (Hypothesized):**
  * Cập nhật trực tiếp nội dung các slide 1-5 và lược bỏ slide 6-16 sẽ tạo ra tệp trình chiếu hoàn hảo, đồng bộ 100% với file PDF mẫu mà không cần vẽ lại đồ thị từ đầu.

---

## 7. Gate 0 Verification (Deterministic Halting Predicate)

- [x] **$L_{\text{known}}$ (Locations Known):** File PPTX mục tiêu, notebook mã nguồn, các asset hình ảnh và quy định thi đã được định vị chính xác.
- [x] **$B_{\text{understood}}$ (Baseline Understood):** Hiểu rõ hiện trạng 16 slide của template và các phần cần thay thế/loại bỏ.
- [x] **$C_{\text{known}}$ (Constraints Known):** Quy tắc $\le 7$ dòng, $\le 10$ từ/dòng, font $\ge 18\text{pt}$, thời lượng 3 phút.
- [x] **$P_{\text{checked}}$ (Patterns Checked):** Đã kiểm tra cấu trúc OpenXML của PPTX và thư viện slide.
- [x] **$V_{\text{known}}$ (Verification Known):** Quy trình kiểm tra bằng mắt (Visual Inspection) và xuất PDF để đối chiếu layout.

**Kết luận Gate 0:** $R_{\text{complete}} = \text{TRUE}$. Sẵn sàng chuyển tiếp sang pha **INNOVATE**.

</research_artifact>
