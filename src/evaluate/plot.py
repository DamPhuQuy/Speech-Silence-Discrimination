"""One final Figure per WAV; detailed Histogram debugging stays in the notebook."""
from pathlib import Path
from typing import Any

from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure
from matplotlib.lines import Line2D
import numpy as np

from src.audio.loader import load_audio
from src.config import Config
from src.evaluate.metrics import evaluate_result
from src.models import (
    AudioSignal, EvaluationMetrics, GroundTruthSegment, ShortTimeFeatures, SegmentationResult,
)


FEATURE_NAMES = {"ste": "STE", "ma": "MA", "logste": "logSTE", "logma": "logMA"}


def _error_text(value: float) -> str:
    return f"{value:.3f} ms" if np.isfinite(value) else "không có cặp biên khớp"


def _state_intervals(axis, segments, offset: float, color: str) -> None:
    """Draw supplied binary intervals; do not reclassify or fill LAB gaps."""
    for start, end, label in segments:
        axis.hlines(offset + (label == "speech"), start, end, color=color, linewidth=2)
    for previous, current in zip(segments, segments[1:]):
        if abs(previous[1] - current[0]) <= 1e-9 and previous[2] != current[2]:
            axis.vlines(current[0], offset, offset + 1, color=color, linewidth=1.1)


def plot_result(
    signal: AudioSignal, features: ShortTimeFeatures, result: SegmentationResult,
    output_path: Path | None = None, *, metrics: EvaluationMetrics | None = None,
    interactive: bool = False,
) -> Figure:
    """Create one two-panel Figure and optionally save it as a PNG.

    Overlay waveform samples on the left amplitude axis and unchanged feature
    values at their frame centers on the right axis. Frozen T* belongs to the
    feature axis; BLUE/RED lines mark predicted/LAB boundaries in seconds.
    The lower panel compares postprocessed intervals with LAB. Metrics are reused verbatim. If
    omitted, the existing boundary evaluator supplies its documented defaults.
    No feature/threshold estimation or Histogram construction occurs here.

    The default uses an unregistered Agg Figure without opening a window.
    interactive=True registers the same single Figure with pyplot; the caller
    decides when to show/close it. Return the Figure for inspection or display.
    """
    if signal.name != result.signal_name or features.feature_type not in FEATURE_NAMES:
        raise ValueError("Signal/result names and selected feature must be valid.")
    samples = np.asarray(signal.signal)
    values, times = np.asarray(features.values), np.asarray(features.timestamps)
    if (samples.ndim != 1 or not samples.size or not np.isfinite(signal.fs) or signal.fs <= 0
            or not np.all(np.isfinite(samples)) or not np.isfinite(signal.duration_sec) or signal.duration_sec <= 0):
        raise ValueError("Plotting requires finite mono audio, positive Fs and duration.")
    if (values.ndim != 1 or not values.size or times.shape != values.shape
            or not np.array_equal(times, result.timestamps)
            or not np.all(np.isfinite(values)) or not np.all(np.isfinite(times))
            or np.any(np.diff(times) <= 0)
            or np.asarray(result.filtered_decisions).shape != values.shape
            or not np.isfinite(result.threshold_used)):
        raise ValueError("Feature values, frame timestamps and decisions must align with a finite threshold.")
    if metrics is None:
        metrics = evaluate_result(signal, result)
    if (metrics.signal_name != signal.name or metrics.threshold != result.threshold_used
            or list(metrics.predicted_boundaries) != list(result.predicted_boundaries)
            or list(metrics.gt_boundaries) != list(signal.gt_boundaries)):
        raise ValueError("Metrics must describe this recording's frozen prediction and LAB boundaries.")

    if interactive:
        from matplotlib import pyplot as plt
        with plt.ioff():
            figure = plt.figure(figsize=(13, 8), layout="constrained")
    else:
        figure = Figure(figsize=(13, 8), layout="constrained")
        FigureCanvasAgg(figure)
    waveform, states = figure.subplots(2, 1, sharex=True, gridspec_kw={"height_ratios": [2.5, 1.2]})
    feature_axis = waveform.twinx()
    feature_name = FEATURE_NAMES[features.feature_type]
    figure.suptitle(
        f"{signal.wav_path.name} | Histogram | {feature_name} | Ngưỡng khóa T* = {result.threshold_used:.6f}\n"
        f"MAE = {_error_text(metrics.mae_ms)} | RMSE = {_error_text(metrics.rmse_ms)} | "
        f"Khớp {metrics.matched_count}/{len(metrics.gt_boundaries)} | "
        f"Thừa {metrics.unmatched_predictions} | Bỏ sót {metrics.unmatched_ground_truth}",
        fontsize=13, fontweight="bold",
    )

    waveform_line, = waveform.plot(np.arange(samples.size) / signal.fs, samples,
                                   color="0.3", linewidth=.45, alpha=.75, label="Tín hiệu")
    for boundary in result.predicted_boundaries:
        waveform.axvline(boundary, color="blue", linewidth=1.4)
    for boundary in signal.gt_boundaries:
        waveform.axvline(boundary, color="red", linestyle="--", linewidth=1.4)
    waveform.set_title(f"Dạng sóng tín hiệu + {feature_name} | Fs = {signal.fs:,} Hz | Thời lượng = {signal.duration_sec:.3f} s",
                       loc="left", fontsize=11)
    waveform.set_ylabel("Biên độ tín hiệu")

    # Keep feature values in their original units; only the axes share time.
    feature_line, = feature_axis.plot(times, values, color="seagreen", linewidth=1.2, label=feature_name)
    threshold_line = feature_axis.axhline(result.threshold_used, color="black", linestyle="--", linewidth=1.3,
                                         label="Ngưỡng T*")
    feature_axis.set_ylabel(f"Giá trị {feature_name}", color="seagreen")
    feature_axis.tick_params(axis="y", colors="seagreen")
    feature_axis.spines["right"].set_color("seagreen")
    feature_axis.spines[["top", "left"]].set_visible(False)
    feature_axis.grid(False)
    # Draw the combined legend on the uppermost twin so traces cannot cross its text.
    feature_axis.legend(handles=[
        waveform_line, feature_line, threshold_line,
        Line2D([], [], color="blue", label="Biên dự đoán"),
        Line2D([], [], color="red", linestyle="--", label="Biên Ground Truth"),
    ], loc="upper right", ncol=3, fontsize=9, framealpha=.95)

    _state_intervals(states, result.segments, 2, "blue")
    truth = [(segment.start, segment.end, segment.label) for segment in signal.gt_segments]
    _state_intervals(states, truth, 0, "red")
    states.set_title("Kết quả Speech/Silence sau hậu xử lý so với LAB", loc="left", fontsize=11)
    states.set_yticks([0, 1, 2, 3], ["LAB Silence", "LAB Speech", "Dự đoán Silence", "Dự đoán Speech"], fontsize=9)
    states.set_ylim(-.35, 3.45)
    states.set_xlabel("Thời gian (s)")
    for axis in (waveform, states):
        axis.set_xlim(0, signal.duration_sec)
        axis.grid(axis="x", color="0.88", linewidth=.6)
        axis.spines[["top", "right"]].set_visible(False)
    if output_path is not None:
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        figure.savefig(path, dpi=150, facecolor="white")
    return figure


def plot_test_report(
    report: dict[str, Any], output_directory: Path, *, show: bool = False,
) -> list[Path]:
    """Save one combined PNG per WAV from a frozen evaluation report.

    Reuse stored predictions, LAB intervals, boundaries and metrics. Load each
    waveform without LAB and reuse production framing/features to obtain a
    ShortTimeFeatures object, checking it against the report before plotting.
    No prediction, fitting, matching or parameter selection is repeated.
    show=True displays only these Figures, together in one pyplot.show call.
    """
    from src.pipeline import prepare_frames, extract_features

    rows = report["files"]
    names = [row["wav"] for row in rows]
    if (len(rows) != report["number_of_wavs"] or not rows
            or len(set(name.casefold() for name in names)) != len(names)
            or any(Path(name).name != name or Path(name).suffix.lower() != ".wav" for name in names)):
        raise ValueError("Report must contain one unique filename per evaluated WAV.")
    frozen = report["frozen_configuration"]
    params = frozen["parameters"]
    config = Config(
        feature_type=frozen["feature"], frame_duration_ms=params["frame_duration_ms"],
        frame_shift_ms=params["frame_shift_ms"], min_silence_ms=params["min_silence_ms"],
        epsilon=params["epsilon"], histogram_bins=params["num_bins"],
        histogram_smoothing_window=params["smooth_window"],
    )
    output_directory = Path(output_directory)
    figures, paths = [], []
    try:
        for row in rows:
            audio = load_audio(Path(report["test_directory"]) / row["wav"])
            features = extract_features(prepare_frames(audio, config), config)
            if (audio.fs != row["fs"] or not np.isclose(audio.duration_sec, row["duration_sec"], rtol=0, atol=1e-12)
                    or row["threshold"] != frozen["threshold"]
                    or features.values.size != row["frames"]
                    or not np.allclose(features.values, row["feature_values"], rtol=1e-12, atol=1e-12)
                    or not np.allclose(features.timestamps, row["timestamps_sec"], rtol=0, atol=1e-12)):
                raise ValueError(f"{row['wav']}: waveform/features no longer match the frozen evaluation report.")
            audio.gt_segments = [GroundTruthSegment(**segment) for segment in row["ground_truth_intervals"]]
            audio.gt_boundaries = row["ground_truth_boundaries"]
            result = SegmentationResult(
                audio.name, "histogram", frozen["threshold"], np.asarray(row["timestamps_sec"]),
                np.asarray(row["raw_predicted_frame_labels"]), np.asarray(row["predicted_frame_labels"]),
                row["predicted_boundaries"], [tuple(segment) for segment in row["predicted_segments"]],
            )
            evaluated = row["boundary_evaluation"]
            if "recording_environment" in row:
                environment = row["recording_environment"] or "unknown"
            else:
                environment = ("phone" if audio.is_phone else
                               "studio" if audio.wav_path.stem.lower().startswith("studio_") else "unknown")
            metrics = EvaluationMetrics(
                audio.name, environment, "histogram", frozen["threshold"],
                evaluated["mae_ms"] if evaluated["mae_ms"] is not None else float("nan"),
                evaluated["rmse_ms"] if evaluated["rmse_ms"] is not None else float("nan"),
                row["predicted_boundaries"], row["ground_truth_boundaries"],
                matched_count=evaluated["matched_count"],
                unmatched_predictions=len(evaluated["unmatched_predicted_boundaries"]),
                unmatched_ground_truth=len(evaluated["unmatched_gt_boundaries"]),
                matching_tolerance_ms=evaluated["tolerance_ms"],
            )
            path = output_directory / f"{Path(row['wav']).stem}.png"
            figure = plot_result(audio, features, result, path, metrics=metrics, interactive=show)
            figures.append(figure)
            paths.append(path)
        if show:
            from matplotlib import pyplot as plt
            plt.show()
    finally:
        for figure in figures:
            if show:
                from matplotlib import pyplot as plt
                plt.close(figure)
            else:
                figure.clear()
    return paths
