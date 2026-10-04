import os
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent

# Tự động chuyển sang môi trường ảo .venv nếu đang chạy bằng python hệ thống
venv_python = ROOT_DIR / ".venv" / "bin" / "python"
if venv_python.exists() and sys.executable != str(venv_python):
    try:
        import numpy  # noqa: F401
    except ImportError:
        os.execv(str(venv_python), [str(venv_python)] + sys.argv)

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import json
from src.audio.dataset import load_dataset
from src.evaluate.metrics import evaluate_signal, summarize_metrics
from src.models import EvaluationMetrics, SegmentationResult
from src.segmentation.segment import segment_signal
from src.segmentation.threshold import calibrate_thresholds
from src.visualization.plotting import (
    plot_comparison_all_algorithms,
    visualize_test_dataset,
)


def main() -> None:
    output_dir = ROOT_DIR / "reports" / "figures"
    output_dir.mkdir(parents=True, exist_ok=True)

    # 1. Tải tập dữ liệu huấn luyện và kiểm thử
    train_signals = load_dataset("TinHieuHuanLuyen")
    test_signals = load_dataset("TinHieuKiemThu")

    # 2. Hiệu chuẩn bộ ngưỡng cho các thuật toán
    thresholds = calibrate_thresholds(train_signals)

    algorithms = ["histogram", "binary", "gaussian"]
    results_by_algo: dict[str, list[SegmentationResult]] = {}
    metrics_by_algo: dict[str, list[EvaluationMetrics]] = {}
    summary_by_algo: dict[str, dict] = {}

    # 3. Chạy phân đoạn và đánh giá (Quy chuẩn dùng chung ngưỡng toàn cục theo yêu cầu đề bài)
    for algo in algorithms:
        r_list: list[SegmentationResult] = []
        m_list: list[EvaluationMetrics] = []
        for sig in test_signals:
            th_val = thresholds.get_threshold(algo, sig.is_phone, use_common=True)

            res = segment_signal(
                sig,
                th_val,
                algorithm=algo,
                min_silence_ms=200.0,
            )
            met = evaluate_signal(
                sig,
                res.predicted_boundaries,
                algorithm=algo,
                threshold=th_val,
            )
            r_list.append(res)
            m_list.append(met)

        results_by_algo[algo] = r_list
        metrics_by_algo[algo] = m_list
        summary_by_algo[algo] = summarize_metrics(m_list)

        # Lưu đồ thị từng thuật toán
        visualize_test_dataset(test_signals, r_list, m_list, output_dir=output_dir)

    # Lưu đồ thị so sánh xếp chồng cả 3 thuật toán
    for i, sig in enumerate(test_signals):
        res_dict = {algo: results_by_algo[algo][i] for algo in algorithms}
        met_dict = {algo: metrics_by_algo[algo][i] for algo in algorithms}
        comp_path = output_dir / f"comparison_{sig.name}.png"
        plot_comparison_all_algorithms(sig, res_dict, met_dict, save_path=comp_path)

    # Lưu báo cáo tổng hợp JSON
    report_json_path = ROOT_DIR / "reports" / "ket_qua_tong_hop.json"
    report_json_path.parent.mkdir(parents=True, exist_ok=True)
    report_data = {
        "thresholds": {
            "binary": {
                "global": thresholds.binary_threshold,
                "phone": thresholds.binary_threshold_phone,
                "studio": thresholds.binary_threshold_studio,
            },
            "histogram": {
                "global": thresholds.histogram_threshold,
                "phone": thresholds.histogram_threshold_phone,
                "studio": thresholds.histogram_threshold_studio,
            },
            "gaussian": {
                "global": thresholds.gaussian_threshold,
                "phone": thresholds.gaussian_threshold_phone,
                "studio": thresholds.gaussian_threshold_studio,
                "mean_speech": thresholds.mean_speech,
                "std_speech": thresholds.std_speech,
                "mean_silence": thresholds.mean_silence,
                "std_silence": thresholds.std_silence,
            },
        },
        "summary": summary_by_algo,
    }
    with open(report_json_path, "w", encoding="utf-8") as f:
        json.dump(report_data, f, ensure_ascii=False, indent=2)

    # 4. In bảng kết quả trực quan, ngắn gọn, dễ hiểu (độ chính xác 6 chữ số thập phân)
    print("\n" + "=" * 92)
    print(
        "        KẾT QUẢ PHÂN ĐOẠN TIẾNG NÓI & KHOẢNG LẶNG (QUY CHUẨN NGƯỠNG TOÀN CỤC)        "
    )
    print("=" * 92)
    header = (
        f"{'Tên File':<12} {'Môi trường':<11} {'SNR (dB)':<10} "
        f"{'Histogram (MAE)':<18} {'Binary (MAE)':<18} {'Gaussian (MAE)'}"
    )
    print(header)
    print("-" * 92)

    for i, sig in enumerate(test_signals):
        h_met = metrics_by_algo["histogram"][i]
        b_met = metrics_by_algo["binary"][i]
        g_met = metrics_by_algo["gaussian"][i]

        print(
            f"{sig.name:<12} {h_met.environment:<11} {h_met.snr_db:4.1f} dB   "
            f"{h_met.mae_ms:9.6f} ms     "
            f"{b_met.mae_ms:9.6f} ms     "
            f"{g_met.mae_ms:9.6f} ms"
        )

    print("-" * 92)
    # Tổng kết theo nhóm môi trường
    hp_mae = summary_by_algo["histogram"]["Phone"]["mean_mae_ms"]
    bp_mae = summary_by_algo["binary"]["Phone"]["mean_mae_ms"]
    gp_mae = summary_by_algo["gaussian"]["Phone"]["mean_mae_ms"]
    print(f"{'TB Phone':<12} {'Phone (2 file)':<21} {hp_mae:9.6f} ms     {bp_mae:9.6f} ms     {gp_mae:9.6f} ms")

    hs_mae = summary_by_algo["histogram"]["Studio"]["mean_mae_ms"]
    bs_mae = summary_by_algo["binary"]["Studio"]["mean_mae_ms"]
    gs_mae = summary_by_algo["gaussian"]["Studio"]["mean_mae_ms"]
    print(f"{'TB Studio':<12} {'Studio (2 file)':<21} {hs_mae:9.6f} ms     {bs_mae:9.6f} ms     {gs_mae:9.6f} ms")

    ha_mae = summary_by_algo["histogram"]["Overall"]["mean_mae_ms"]
    ba_mae = summary_by_algo["binary"]["Overall"]["mean_mae_ms"]
    ga_mae = summary_by_algo["gaussian"]["Overall"]["mean_mae_ms"]
    print(f"{'Toàn bộ':<12} {'Overall (4 file)':<21} {ha_mae:9.6f} ms     {ba_mae:9.6f} ms     {ga_mae:9.6f} ms")
    print("=" * 92)
    print(f"  • Histogram : T = {thresholds.histogram_threshold:7.4f} (log-STE)")
    print(f"  • Binary    : T = {thresholds.binary_threshold:7.6f} (norm-STE)")
    print(f"  • Gaussian  : T = {thresholds.gaussian_threshold:7.6f} (norm-STE)")
    total_figs = len(test_signals) * (len(algorithms) + 1)
    print(
        f"\n[Hoàn tất]: Đã lưu {total_figs} biểu đồ vào {output_dir.relative_to(ROOT_DIR)}/ và số liệu JSON vào {report_json_path.relative_to(ROOT_DIR)}\n"
    )


if __name__ == "__main__":
    main()
