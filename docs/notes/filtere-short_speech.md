# Phân Tích Hiện Tượng Xung Nhiễu Ngắn (Impulse Noise) & Cơ Chế Kháng Nhiễu Giữa Các Thuật Toán

Tài liệu này ghi lại chi tiết thực nghiệm, bằng chứng số liệu và phân tích âm học về hiện tượng **các mốc biên ảo (vạch xanh) xuất hiện trong khoảng lặng** sau khi loại bỏ quy chuẩn lọc tiếng nói ngắn (`filter_short_speech`), nhằm phục vụ cho phần phân tích chuyên sâu trong báo cáo và buổi bảo vệ giữa kỳ.

---

## 1. Hiện Tượng Thực Nghiệm (Observation)

Sau khi chuẩn hóa pipeline (chỉ áp dụng duy nhất điều kiện gộp khoảng lặng $< 200\text{ ms}$ thông qua `filter_short_silence`) trên các biểu đồ phân đoạn trong thư mục `reports/figures/` xuất hiện hiện tượng:

* **Trên thuật toán Binary và Gaussian (ở môi trường điện thoại `phone`):**
  * File `phone_M2`: Xuất hiện một cặp vạch xanh dương (Predicted Boundaries) cách nhau đúng $10\text{ ms}$ (1 khung) tại thời điểm $t = 0.1025\text{ s} - 0.1125\text{ s}$, nằm lọt thỏm trong khoảng lặng ban đầu (vùng trước $0.53\text{ s}$).
  * File `phone_F2`: Xuất hiện một cặp vạch xanh dương cách nhau $20\text{ ms}$ (2 khung) tại thời điểm $t = 0.6225\text{ s} - 0.6425\text{ s}$, nằm trong khoảng lặng trước câu nói (vùng trước $1.02\text{ s}$).
* **Trên thuật toán Histogram:**
  * **Hoàn toàn sạch sẽ, không có bất kỳ vạch xanh ảo nào** trong toàn bộ các khoảng lặng của `phone_M2` và các file studio.

---

## 2. Truy Vết Dữ Liệu Năng Lượng Thực Tế (Data Telemetry)

Truy vết giá trị năng lượng ngắn hạn tại các mốc thời gian xuất hiện xung nhiễu:

### 2.1. File `phone_M2` (Xung tại $t \approx 0.10\text{ s}$)

* **Ngưỡng toàn cục của Binary:** $T_{\text{bin}} = 0.000798$ (STE chuẩn hóa).
* **Ngưỡng toàn cục của Gaussian:** $T_{\text{gauss}} = 0.000792$ (STE chuẩn hóa).
* **Ngưỡng toàn cục của Histogram:** $T_{\text{hist}} = -2.4375$ ($\log(\text{STE})$).

|                                                                                              Thời gian$t$ (giây)                                                                                              | Năng lượng$\text{STE}_{\text{norm}}$ | So với$T_{\text{bin}}$ | Log-Energy$\log(\text{STE})$ |          So với$T_{\text{hist}}$          | Nhãn Binary/Gauss | Nhãn Histogram |
| :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: | :---------------------------------------: | :-----------------------: | :----------------------------: | :-------------------------------------------: | :----------------: | :-------------: |
|                                                                                                $0.0925\text{ s}$                                                                                                |               $0.000666$               |          $< T$          |          $-5.7162$          | $\ll T$ | Silence ($0$) | Silence ($0$) |                    |                |
| **$0.1025\text{ s}$** | **$0.000894$** | **$> T$ (Vượt ngưỡng!)** | **$-5.4227$** | **$\ll T$ (Cách rất xa)** | **Speech ($1$)** | **Silence ($0$)** |                                          |                          |                                |                                              |                    |                |
|                                                                                                $0.1125\text{ s}$                                                                                                |               $0.000734$               |          $< T$          |          $-5.6190$          | $\ll T$ | Silence ($0$) | Silence ($0$) |                    |                |

👉 **Hệ quả trên Binary/Gaussian:** Trạng thái chuyển đổi từ $0 \to 1$ tại $0.1025\text{ s}$ rồi lập tức rơi từ $1 \to 0$ tại $0.1125\text{ s}$. Hệ thống trích xuất hai mốc biên liên tiếp:

$$
\text{Predicted Boundaries} = [\mathbf{0.1025},\, \mathbf{0.1125},\, 0.5325,\, 2.5325]
$$

Hai đường thẳng đứng màu xanh dương cách nhau đúng $10\text{ ms}$ được vẽ lên đồ thị.

### 2.2. File `phone_F2` (Xung tại $t \approx 0.62\text{ s}$)

* Tại $t = 0.6225\text{ s}$: $\text{STE}_{\text{norm}} = 0.001524 > T_{\text{bin}}$ (Speech: $1$).
* Tại $t = 0.6325\text{ s}$: $\text{STE}_{\text{norm}} = 0.001471 > T_{\text{bin}}$ (Speech: $1$).
* Tại $t = 0.6425\text{ s}$: $\text{STE}_{\text{norm}} = 0.000584 < T_{\text{bin}}$ (Silence: $0$).
* Trong khi đó, $\log(\text{STE})$ ở các khung này chỉ đạt $-5.14$ đến $-5.18$, thấp hơn rất nhiều so với $T_{\text{hist}} = -2.4375$.

---

## 3. Tại Sao Quy Tắc Của Đề Bài Không Triệt Tiêu Được Hiện Tượng Này?

Trong tài liệu hướng dẫn bài tập lớn của Giảng viên:

> *"Độ dài tối thiểu của 1 khoảng lặng là 200 ms (dùng điều kiện này để loại bỏ các khoảng lặng 'ảo' có chiều dài quá ngắn)"*

* **Bản chất thuật toán:** Hàm `filter_short_silence(min_silence_ms=200.0)` là một phép toán đóng (*morphological closing*) trên nhãn phân loại:
  $$
  \text{Nếu } (\text{Duration}(\text{Silence}) < 200\text{ ms}) \land (\text{kẹp giữa 2 vùng Speech}) \implies \text{Silence} \to \text{Speech}
  $$
* **Hạn chế đối với xung nhiễu:**
  * Xung nhiễu tại $0.10\text{ s}$ là một mẩu **tiếng nói ngắn ($10\text{ ms}$)** nằm giữa hai khoảng lặng dài ($> 500\text{ ms}$).
  * Điều kiện của đề bài chỉ tác động lên **khoảng lặng ngắn**, hoàn toàn không tác động lên **tiếng nói ngắn**.
  * Vì vậy, nếu không có quy tắc lọc tiếng nói ngắn, xung $10\text{ ms}$ này sẽ tồn tại nguyên vẹn trong chuỗi nhãn và sinh ra mốc biên trên biểu đồ.

---

## 4. Cơ Sở Lý Thuyết Âm Học & Tiêu Chuẩn Quốc Tế

Tại sao trong các hệ thống Voice Activity Detection (VAD) thực tế, người ta luôn đặt thêm điều kiện thời lượng tối thiểu cho tiếng nói ($30\text{ ms} - 50\text{ ms}$)?

1. **Công trình kinh điển của Rabiner & Sambur (1975):**

   * *Nguồn trích dẫn:* **L. R. Rabiner and M. R. Sambur**, *"An Algorithm for Determining the Endpoints of Isolated Utterances"*, **The Bell System Technical Journal (BSTJ)**, Vol. 54, No. 2, pp. 297–315, 1975.
   * *Khẳng định:* Sau khi phân đoạn bằng STE/ZCR, các tác giả định nghĩa: Bất kỳ đoạn tín hiệu nào vượt ngưỡng nhưng kéo dài dưới $50\text{ ms}$ đều bị loại bỏ vì đây là các xung nhiễu không mong muốn (tiếng thở, tiếng tặc lưỡi, clicks cơ học của micro).
2. **Cơ sở sinh lý học cấu âm (Acoustic Phonetics):**

   * *Nguồn trích dẫn:* **Kenneth N. Stevens (1998)**, *"Acoustic Phonetics"*, MIT Press.
   * *Sinh lý phát âm:* Thời lượng của một nguyên âm bình thường ở người là $60\text{ ms} - 300\text{ ms}$. Phụ âm ngắn nhất (tiếng bật của âm tắc - stop release burst) kéo dài $15\text{ ms} - 35\text{ ms}$. Một âm tiết hoàn chỉnh có nghĩa không thể phát âm và kết thúc trong khoảng thời gian $< 30\text{ ms} - 50\text{ ms}$. Do đó, một xung $10\text{ ms}$ về mặt âm học không thể là tiếng người có nghĩa.
3. **Tiêu chuẩn công nghiệp ITU-T G.729 Annex B (1996):**

   * Chuẩn VAD quốc tế quy định kiểm tra chuỗi tối thiểu 3 khung ($30\text{ ms}$) trước khi quyết định kích hoạt trạng thái Voice Activity để triệt tiêu false alarm từ môi trường nhiễu.

---

## 5. Luận Điểm Học Thuật Đắt Giá Cho Báo Cáo & Bảo Vệ

Việc giữ nguyên hiện trạng (Phương án 1) và phân tích sâu hiện tượng này mang lại giá trị học thuật rất cao:

1. **Chứng minh sự ưu việt của phân tích miền Logarit (`log_ste`):**

   * Trên miền $STE$ tuyến tính chuẩn hóa (dùng cho Binary và Gaussian), biên độ năng lượng phân bố không đều; khoảng cách giữa sàn nhiễu (noise floor) và ngưỡng quyết định $T$ rất mỏng manh ($\Delta \approx 0.0001$). Do đó, các xung nhiễu nhẹ dễ dàng làm sai lệch kết quả.
   * Trên miền $\log(STE)$ (dùng cho Histogram), hàm logarit nén dải động cực lớn của tiếng nói và mở rộng khoảng cách giữa tín hiệu và sàn nhiễu. Ngưỡng $T_{\text{hist}} = -2.4375$ cách mức nhiễu $-5.42$ hơn $3$ đơn vị log, giúp **Histogram có khả năng kháng nhiễu xung tự nhiên (inherent noise robustness)** mà không cần dựa dẫm vào bất kỳ bộ lọc nhân tạo nào.
2. **Thể hiện tính trung thực khoa học và bám sát đề tài:**

   * Việc không "vá" code bằng các heuristic ngoài đề bài thể hiện sự tôn trọng tuyệt đối với yêu cầu kỹ thuật của Giảng viên.
   * Thay vì che giấu các vạch xanh giả, việc giải thích cặn kẽ nguồn gốc vật lý, truy vết số liệu từng mili-giây và đối chiếu với nghiên cứu kinh điển của Rabiner & Sambur (1975) chứng minh sinh viên hiểu bản chất sâu sắc từ toán học, tín hiệu đến sinh lý âm học.
