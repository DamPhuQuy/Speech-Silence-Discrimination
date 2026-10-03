# Kiểm tra yêu cầu đường F0 cho phần Histogram

## Kết luận về phạm vi

Hướng dẫn trình bày có nhắc rõ đường F0, nhưng đề bài Speech/Silence đang dùng
không yêu cầu tính F0. Tài liệu giảng dạy phân nhiệm vụ phân đoạn và tính F0
thành các task riêng. Vì hướng dẫn trình bày không ghi điều kiện áp dụng cho
từng task, chưa đủ căn cứ để khẳng định sinh viên làm Histogram phải cài thêm
một thuật toán pitch. Cũng không nên bỏ qua câu nhắc F0 trong hướng dẫn chung.

Project hiện không có contour F0 hay cài đặt trích xuất F0 được cung cấp sẵn.
Đợt kiểm tra này chỉ ghi nhận yêu cầu và dữ liệu; không thêm thuật toán, không
đổi hình demo, cấu hình huấn luyện hoặc ngưỡng khóa.

## Nguồn yêu cầu và cách phân loại

| Nguồn | Vị trí và nội dung | Phân loại |
|---|---|---|
| [Đề bài phân đoạn Speech/Silence](<../assignments/Hướng dẫn BT - Phân đoạn tín hiệu thành tiếng nói và khoảng lặng_XLTHS_GK 2026.docx>) | Mục 4: "Mỗi SV trong nhóm cài đặt và demo 01 thuật toán nêu ở trên"; yêu cầu STE/MA hoặc logSTE/logMA xếp chồng lên tín hiệu, biên dự đoán/GT và MAE/RMSE. Không có F0/pitch. | Yêu cầu cốt lõi của bài phân đoạn |
| [Hướng dẫn trình bày slide và nộp bài thi](<../assignments/Hướng dẫn trình bày slide và nộp bài thi.pdf>) | Trang 1, mục "Cách trình bày kết quả thực nghiệm trên slide": "các đường kẻ dọc thể hiện biên thời gian chuẩn & biên thời gian mà thuật toán tự động xác định được, đường F0 của tín hiệu". | Nội dung trong hướng dẫn trình bày chung; không nêu riêng Histogram hoặc ngoại lệ cho từng task |
| [Chapter6](../references/Chapter6_AUDIO-SPEECH%20SIGNAL%20PROCESSING.pdf) | Trang PDF 48: task 1a "phân đoạn speech vs. silence", task 2a "tính F0 dùng hàm tự tương quan", task 2b "tính F0 dùng hàm AMDF"; sinh viên phân công nhiệm vụ không trùng nhau. | Phạm vi nhiệm vụ khác nhau trong tài liệu giảng dạy |
| [README định dạng LAB](../../data/tinhieuhuanluyen/README.txt) | Dòng 13: F0mean/F0std là trung bình và độ lệch chuẩn của F0 tại các frame hữu thanh, đơn vị Hz. | Metadata thống kê, không phải yêu cầu thuật toán hoặc contour |
| Các ghi chú Histogram và paper Histogram trong project | Không tìm thấy yêu cầu vẽ đường F0. | Không bổ sung yêu cầu F0 cho thuật toán Histogram |

Ở lần kiểm tra trước, `Hướng dẫn triển khai.docx` tại thư mục gốc và
`histogram_presentation_docs.md` cũng đã được đọc. Hai file này không còn trong
project ở lần review cuối, nên không được liệt kê là nguồn hiện có. Ký hiệu
`f = [f0, f1, ..., fN-1]` trong lộ trình cũ chỉ là vector đặc trưng, không phải
contour F0. Kết luận phía trên dựa vào các tài liệu vẫn có trong project.

Việc hướng dẫn trình bày phục vụ nhiều task là suy luận từ cách phân công trong
Chapter6, không phải một ngoại lệ được viết rõ trong hướng dẫn trình bày.
Nếu áp dụng câu trong hướng dẫn trình bày như yêu cầu bắt buộc cho phần này,
tình trạng hiện tại cần được báo cáo đúng:

> F0 curve is required by the presentation instruction but the current project does not contain an F0 contour or an approved F0 extraction implementation.

## Dữ liệu hiện có

Đã kiểm tra toàn bộ 8 LAB: 4 file huấn luyện và 4 file kiểm thử. Mỗi file chỉ có
các interval `start/end/sil/v/uv` cùng hai dòng F0mean/F0std. Các timestamp của
interval là biên phân đoạn, không phải thời điểm của một mẫu F0.

| Tập | File | F0mean (Hz) | F0std (Hz) |
|---|---|---:|---:|
| Huấn luyện | phone_F1.lab | 217 | 23 |
| Huấn luyện | phone_M1.lab | 122 | 18 |
| Huấn luyện | studio_F1.lab | 232 | 40 |
| Huấn luyện | studio_M1.lab | 113 | 26 |
| Kiểm thử | phone_F2.lab | 145 | 33.7 |
| Kiểm thử | phone_M2.lab | 129 | 18.6 |
| Kiểm thử | studio_F2.lab | 200 | 46.1 |
| Kiểm thử | studio_M2.lab | 155 | 30.8 |

Hai thống kê này không xác định một chuỗi F0 theo thời gian. Không thể dùng
chúng để dựng đường F0 thật, kể cả bằng một đường hằng hoặc các điểm ngẫu nhiên.
`parse_labels()` đang bỏ qua các dòng thống kê và giữ nhãn gốc `v`/`uv` phục vụ
phân đoạn; hành vi này được giữ nguyên.

## Cài đặt và tài liệu phương pháp

Không tìm thấy estimator pitch/F0 hoặc contour lưu sẵn trong `src/`, `scripts/`,
`pipeline.ipynb`, cấu hình, models, dependencies hay các JSON kết quả. Những
chỗ nhắc F0 trong notebook/tests hiện chỉ nói về việc bỏ qua dòng thống kê LAB.

Chapter6 giới thiệu ACF/AMDF ở trang PDF 36, lưu đồ ACF ở trang 41 và dải
70-400 Hz ở trang 42. CS425 có chương pitch riêng, với ví dụ và hướng dẫn cửa
sổ khác. Đây là tài liệu phương pháp cho nhiệm vụ F0; chúng không cung cấp
một hàm F0 đã được triển khai trong project hoặc bộ frame/hop F0 bắt buộc cho
bài Histogram. Hướng dẫn trình bày cũng yêu cầu tự cài đặt DSP, chỉ cho phép
các phép built-in Matlab/NumPy; không có phép cho dùng pitch toolbox.

## Quyết định trong task này

Chỉ thêm tài liệu kiểm tra này. Không tạo `src/features/f0.py`, không thêm
dependency, không thêm đường F0 hoặc panel F0. Các hình cuối vẫn giữ dạng sóng
chồng với đặc trưng đã chọn và ngưỡng T*, biên dự đoán xanh dương, biên LAB đỏ,
cùng phần so sánh Speech/Silence và MAE/RMSE. Mô hình hiện tại vẫn dùng logSTE
với T* = -2.4375196566847372.

Không thay đổi code nên không cần kiểm thử một thuật toán F0 mới. Việc thiếu
contour/cài đặt sẵn và điểm chưa rõ về phạm vi áp dụng hướng dẫn trình bày
được ghi nhận, thay vì tạo dữ liệu F0 hoặc tự mở rộng nhiệm vụ Histogram.
