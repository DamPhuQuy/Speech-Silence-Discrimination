import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.audio.dataset import load_dataset
from src.evaluate.metrics import evaluate_signal, summarize_metrics
from src.pipeline import run_pipeline
from src.segmentation.segment import segment_signal
import json


def main() -> None:
    output_dir = ROOT_DIR / "reports" / "figures"
    output_dir.mkdir(parents=True, exist_ok=True)

    algo_name = "binary"
    if len(sys.argv) > 1:
        arg_algo = sys.argv[1].lower()
        if arg_algo in ["binary", "histogram", "gaussian"]:
            algo_name = arg_algo

    thresholds, results, metrics_list = run_pipeline(
        train_dir=ROOT_DIR / "TinHieuHuanLuyen",
        test_dir=ROOT_DIR / "TinHieuKiemThu",
        algorithm=algo_name,
        output_dir=output_dir,
        generate_plots=True,
    )

    test_signals = load_dataset(ROOT_DIR / "TinHieuKiemThu")
    algorithms = ["binary", "histogram", "gaussian"]
    summary_by_algo = {}

    for algo in algorithms:
        m_list = []
        for sig in test_signals:
            th_val = thresholds.get_threshold(algo, sig.is_phone)
            res = segment_signal(sig, th_val, algorithm=algo, min_silence_ms=200.0)
            met = evaluate_signal(
                sig, res.predicted_boundaries, algorithm=algo, threshold=th_val
            )
            m_list.append(met)
        summary_by_algo[algo] = summarize_metrics(m_list)

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

if __name__ == "__main__":
    main()
