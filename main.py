"""One-command demonstration of frozen Histogram Speech/Silence segmentation."""
import argparse
from pathlib import Path

from src.config import load_frozen_histogram
from src.pipeline import evaluate_frozen_histogram
from src.evaluate.plot import plot_test_report
from src.evaluate.reporting import format_training_information, format_final_table, save_test_report


def main(*, show: bool = True, project_root: Path | None = None) -> list[Path]:
    """Load/print the training lock, evaluate every test WAV, plot and report.

    Use the existing training model rather than refitting during a demonstration.
    A missing lock/data or invalid model fails; there is no test-derived fallback.
    Display the final Figures by default; show=False saves them without windows.
    project_root supports another checkout and synthetic integration tests.
    """
    root = Path(project_root).resolve() if project_root is not None else Path(__file__).resolve().parent
    config, model, information = load_frozen_histogram(root / "output" / "training" / "final_histogram_configuration.json")
    print(format_training_information(information), end="\n\n")
    report = evaluate_frozen_histogram(root / "data" / "tinhieukiemthu", config, model, information)
    report_path = save_test_report(
        report, root / "output" / "test" / "histogram_test_evaluation.json",
        root / "docs" / "notes" / "histogram_test_evaluation.md",
    )
    print(format_final_table(report))
    # Print/save evaluation before the display call waits for windows to close.
    paths = plot_test_report(report, root / "output" / "test" / "figures", show=show)
    print(f"Created {len(paths)} main Figures for {report['number_of_wavs']} test WAVs.")
    for path in paths:
        print(path)
    print(f"Detailed evaluation: {report_path}")
    print(f"Noise/error summary: {report_path.with_name('noise_vs_error.json')}")
    return paths

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--show", action=argparse.BooleanOptionalAction, default=True,
                        help="Display the final Figures (default); --no-show saves them without windows.")
    args = parser.parse_args()
    try:
        main(show=args.show)
    except (OSError, ValueError, RuntimeError) as exc:
        parser.exit(status=1, message=f"Histogram demonstration failed: {exc}\n")
