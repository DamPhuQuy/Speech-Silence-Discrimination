# Module: `src/evaluate`
Đo lường định lượng độ chính xác của thuật toán phân đoạn và đánh giá mức nhiễu nền môi trường thu âm.

---

## 1. Các tệp thành phần

* **`metrics.py`**:
  - **`estimate_snr_db`**: Ước lượng tỷ số tín hiệu trên nhiễu SNR (dB) của file âm thanh bằng cách đo lường công suất trung bình giữa vùng tiếng nói và khoảng lặng theo Ground Truth:
    $$SNR\text{ (dB)} = 10 \log_{10}\left(\frac{P_{\text{speech}}}{P_{\text{silence}}}\right)$$
  - **`match_boundaries`**: Ghép cặp mốc biên dự đoán với mốc biên chuẩn Ground Truth:
    - Nếu số lượng biên bằng nhau: ghép 1-1 tuần tự theo thứ tự thời gian.
    - Nếu số lượng biên lệch nhau: với mỗi biên chuẩn, tìm biên dự đoán có khoảng cách thời gian ngắn nhất.
  - **`compute_mae`**: Tính sai số tuyệt đối trung bình (Mean Absolute Error - MAE) tính theo mili-giây (ms):
    $$MAE\text{ (ms)} = \frac{1000}{K} \sum_{k=1}^K |t_{\text{pred}, k} - t_{\text{gt}, k}|$$
  - **`compute_rmse`**: Tính sai số căn bậc hai trung bình (Root Mean Squared Error - RMSE) tính theo mili-giây (ms):
    $$RMSE\text{ (ms)} = 1000 \times \sqrt{\frac{1}{K} \sum_{k=1}^K (t_{\text{pred}, k} - t_{\text{gt}, k})^2}$$
  - **`evaluate_signal`**: Tổng hợp MAE, RMSE, SNR cho một file tín hiệu kiểm thử và đóng gói vào `EvaluationMetrics`.
  - **`summarize_metrics`**: Tổng hợp thống kê trung bình MAE, RMSE phân nhóm theo `Phone` (môi trường điện thoại), `Studio` (phòng thu) và `Overall` (toàn bộ).

---

## 2. Quy trình luồng làm việc (Pipeline)

```
AudioSignal (Chứa mốc chuẩn GT) + Biên dự đoán (predicted_boundaries)
         │
         ▼
[metrics.py: evaluate_signal()]
         │
         ├──> [estimate_snr_db()]     --> Đo SNR (dB) của file âm thanh
         ├──> [match_boundaries()]    --> Ghép cặp các mốc biên tương ứng
         ├──> [compute_mae()]         --> Tính MAE (ms) độ chính xác cao
         └──> [compute_rmse()]        --> Tính RMSE (ms)
         │
         ▼
Đối tượng EvaluationMetrics
         │
         ▼
[metrics.py: summarize_metrics()]
         │
         ▼
Thống kê trung bình theo nhóm môi trường: Phone, Studio, Overall
```
