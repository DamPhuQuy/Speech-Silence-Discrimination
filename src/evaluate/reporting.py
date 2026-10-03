"""Display and export frozen Histogram results; no signal processing or fitting."""
from pathlib import Path
from typing import Any
import json
import math

from src.evaluate.snr import POWER_CONTRAST_NAME, POWER_CONTRAST_DEFINITION


def build_noise_vs_error_summary(report: dict[str, Any]) -> dict[str, Any]:
    """Summarize an evaluated batch without fitting or rematching boundaries.

    Reuse existing powers, errors and environment metadata. Unknown environments
    remain unknown. Nonfinite contrasts use a null value plus an explicit status,
    matching the evaluation JSON convention rather than exporting NaN/Infinity.
    """
    rows = []
    for row in report["files"]:
        metrics, noise = row["boundary_evaluation"], row["background_noise"]
        status = noise["contrast_status"]
        contrast = noise["contrast_db"] if status == "finite" else None
        if status == "finite" and (contrast is None or not math.isfinite(contrast)):
            contrast, status = None, "unavailable"
        rows.append({
            "file": row["wav"],
            "recording_environment": row.get("recording_environment"),
            "recording_environment_source": row.get("recording_environment_source"),
            "power_contrast_db": contrast, "power_contrast_status": status,
            "GT_boundary_count": metrics["gt_count"],
            "predicted_boundary_count": metrics["predicted_count"],
            "matched_boundary_count": metrics["matched_count"],
            "extra_predicted_boundaries": len(metrics["unmatched_predicted_boundaries"]),
            "missed_GT_boundaries": len(metrics["unmatched_gt_boundaries"]),
            "MAE_ms": metrics["mae_ms"], "RMSE_ms": metrics["rmse_ms"],
        })

    groups: dict[str, list[float]] = {}
    for row in rows:
        if row["recording_environment"] and row["power_contrast_db"] is not None:
            groups.setdefault(row["recording_environment"], []).append(row["power_contrast_db"])
    observations = [
        f"{environment}: mean contrast {math.fsum(values) / len(values):.3f} dB ({len(values)} files)"
        for environment, values in sorted(groups.items())
    ]
    interpretation = ("Environment-group observations (finite values only): " + "; ".join(observations) + ". "
                      if observations else "No environment-group comparison is available. ")
    if "phone" in groups and "studio" in groups:
        phone_mean = math.fsum(groups["phone"]) / len(groups["phone"])
        studio_mean = math.fsum(groups["studio"]) / len(groups["studio"])
        if phone_mean < studio_mean:
            interpretation += "The phone group has lower mean Speech/Silence Power Contrast than the studio group in this batch. "
    interpretation += (
        f"These are descriptive observations from {report['number_of_wavs']} test recordings, "
        "not evidence of a causal relationship between noise and boundary error. "
        "Environment groups follow supplied metadata; the project's phone/studio groups come from filename prefixes, "
        "not measured room conditions. Contrast also depends on speech level/content and is not clean-speech SNR. "
        "MAE/RMSE use matched boundaries only; extra and missed boundaries must also be considered."
    )
    return {
        "metric_name": POWER_CONTRAST_NAME, "metric_definition": POWER_CONTRAST_DEFINITION,
        "scope": "test_evaluation_only", "number_of_wavs": report["number_of_wavs"],
        "frozen_threshold": report["frozen_configuration"]["threshold"],
        "lock_sha256": report["lock_sha256"], "files": rows, "interpretation": interpretation,
    }


def _noise_summary_lines(report: dict[str, Any]) -> list[str]:
    """Use the same noise/error summary in console and Markdown reports."""
    summary = build_noise_vs_error_summary(report)
    lines = [
        "Noise vs. boundary error: " + summary["metric_name"], "",
        "| File | Environment | Speech/Silence Power Contrast (dB) | GT | Predicted | Matched | Extra | Missed | MAE (ms) | RMSE (ms) |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in summary["files"]:
        contrast = _contrast({"contrast_db": row["power_contrast_db"], "contrast_status": row["power_contrast_status"]})
        lines.append(
            f"| {row['file']} | {row['recording_environment'] or 'unknown'} | {contrast} | "
            f"{row['GT_boundary_count']} | {row['predicted_boundary_count']} | {row['matched_boundary_count']} | "
            f"{row['extra_predicted_boundaries']} | {row['missed_GT_boundaries']} | "
            f"{_number(row['MAE_ms'])} | {_number(row['RMSE_ms'])} |"
        )
    lines.extend(["", summary["interpretation"]])
    return lines


def _file_table_lines(report: dict[str, Any]) -> list[str]:
    """Shared per-file table for console and saved Markdown reports."""
    lines = [
        "| File | Fs (Hz) | Duration (s) | Frames | Predicted boundaries | GT boundaries | MAE (ms) | RMSE (ms) | Speech/Silence Power Contrast (dB) |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in report["files"]:
        metrics = row["boundary_evaluation"]
        lines.append(f"| {row['wav']} | {row['fs']} | {row['duration_sec']:.6f} | {row['frames']} | "
                     f"{metrics['predicted_count']} | {metrics['gt_count']} | {_number(metrics['mae_ms'])} | "
                     f"{_number(metrics['rmse_ms'])} | {_contrast(row['background_noise'])} |")
    return lines


def _number(value: float | None, digits: int = 3) -> str:
    return "unavailable" if value is None else f"{value:.{digits}f}"


def _contrast(noise: dict[str, Any]) -> str:
    if noise["contrast_status"] == "finite":
        return _number(noise["contrast_db"])
    return {"positive_infinity": "+inf", "negative_infinity": "-inf"}.get(noise["contrast_status"], "unavailable")


def render_results(report: dict[str, Any]) -> str:
    """Render the requested test table and disclose unmatched events and alignment."""
    frozen, aggregate = report["frozen_configuration"], report["aggregate_boundary_evaluation"]
    params = frozen["parameters"]
    lines = [
        "# Final frozen Histogram test evaluation", "",
        f"Processed {report['number_of_wavs']} test WAVs in one batch ({report['total_frames']} frames).",
        f"Frozen feature={frozen['feature']}, num_bins={params['num_bins']}, smooth_window={params['smooth_window']},",
        f"W={params['weight']:g}, T*={frozen['threshold']:.17g}.",
        f"Framing: {params['frame_duration_ms']:g} ms / {params['frame_shift_ms']:g} ms; minimum internal silence: {params['min_silence_ms']:g} ms.",
        "The training lock's SHA-256 was unchanged before/after evaluation. No fitting or tuning was performed.", "",
    ]
    if report["file_count_warning"]:
        lines.insert(3, report["file_count_warning"])
    lines.extend(_file_table_lines(report))
    lines.extend(["", *_noise_summary_lines(report), "",
                  "Speech/Silence Power Contrast uses the LAB-based observed speech/silence power ratio:",
                  "10*log10(P_observed_speech/P_silence). Speech includes recording noise; this is not clean-speech SNR.",
                  "sil denotes silence; v and uv denote speech. Powers include DC and exclude uncovered samples.", "",
                  "## Matching and completeness", "",
                  f"The frozen tolerance is {frozen['evaluation_tolerance_ms']:g} ms. Matching remains same-transition-type,",
                  "closest-first, one-to-one and noncrossing. MAE/RMSE use matched pairs only; no matches yields unavailable.",
                  "Missed and extra events are reported separately. Boundaries are midpoints between postprocessed frame centers.", "",
                  "| File | Matched / GT | Missed GT | Extra predicted |", "|---|---:|---:|---:|"])
    for row in report["files"]:
        metrics = row["boundary_evaluation"]
        lines.append(f"| {row['wav']} | {metrics['matched_count']} / {metrics['gt_count']} | "
                     f"{len(metrics['unmatched_gt_boundaries'])} | {len(metrics['unmatched_predicted_boundaries'])} |")
    lines.extend(["", f"Total matches: {aggregate['matched_count']} / {aggregate['gt_count']}; "
                  f"missed GT: {aggregate['unmatched_gt_count']}; extra predicted: {aggregate['unmatched_predicted_count']}.",
                  f"Pooled matched-boundary MAE: {_number(aggregate['mae_ms'])} ms; RMSE: {_number(aggregate['rmse_ms'])} ms.", "",
                  "## Background power and label alignment", "",
                  "| File | Silence power | Observed speech power | Uncovered samples | Uncovered frame centers |",
                  "|---|---:|---:|---:|---:|"])
    for row in report["files"]:
        noise = row["background_noise"]
        power = lambda value: "unavailable" if value is None else f"{value:.9g}"
        lines.append(f"| {row['wav']} | {power(noise['silence_noise_power'])} | {power(noise['observed_speech_power'])} | "
                     f"{noise['uncovered_samples']} | {row['frames'] - row['covered_frames']} |")
    lines.append("")
    for row in report["files"]:
        for warning in row["alignment_warnings"]:
            lines.append(f"- {row['wav']}: {warning}")
        if row["background_noise"].get("reason"):
            lines.append(f"- {row['wav']}: Speech/Silence Power Contrast unavailable: {row['background_noise']['reason']}")
    lines.extend(["", "Powers are squared PCM-normalized amplitude, not calibrated watts.",
                  "Uncovered LAB gaps/tails are excluded from noise and frame-label scoring; LABs are not extended.", "",
                  "## Saved artifacts", "",
                  "output/test/histogram_test_evaluation.json contains per-frame features, raw/filtered decisions, LAB intervals,",
                  "predicted/GT boundaries, matched pairs, individual time errors, unmatched events and background-noise powers.",
                  "output/test/noise_vs_error.json contains the environment groups, power contrasts, complete boundary counts and cautious interpretation.",
                  f"Training lock SHA-256: {report['lock_sha256']}",
                  "Reproduce with python -m scripts.run_test_evaluation; the driver exposes no tuning overrides.", ""])
    return "\n".join(lines)


def format_training_information(information: dict[str, Any]) -> str:
    """Print saved training choices and peaks without recalculating anything."""
    params = information["parameters"]
    lines = [
        "Training Histogram: loaded frozen training model",
        f"feature = {information['feature']}",
        f"num_bins = {params['num_bins']}",
        f"smooth_window = {params['smooth_window']}",
        f"W = {params['weight']:g}",
        f"M1 = {information['m1']:.17g}",
        f"M2 = {information['m2']:.17g}",
        f"T* = {information['threshold']:.17g}",
        f"Frame / shift = {params['frame_duration_ms']:g} / {params['frame_shift_ms']:g} ms",
        f"Minimum internal silence = {params['min_silence_ms']:g} ms",
        "The saved common T* will be reused for every test WAV.",
    ]
    if "number_of_wavs" in information and "total_combined_frames" in information:
        lines.insert(1, f"Training provenance: {information['number_of_wavs']} WAVs, {information['total_combined_frames']} pooled frames")
    return "\n".join(lines)


def format_final_table(report: dict[str, Any]) -> str:
    """Print test results and matched-only error limitations without tuning."""
    aggregate = report["aggregate_boundary_evaluation"]
    lines = [f"Final test results: {report['number_of_wavs']} WAVs, {report['total_frames']} frames"]
    if report["file_count_warning"]:
        lines.append(report["file_count_warning"])
    lines.extend(["", *_file_table_lines(report), "",
                  f"Matched {aggregate['matched_count']}/{aggregate['gt_count']} GT boundaries; "
                  f"missed {aggregate['unmatched_gt_count']}; extra predicted {aggregate['unmatched_predicted_count']}.",
                  f"Pooled MAE = {_number(aggregate['mae_ms'])} ms; RMSE = {_number(aggregate['rmse_ms'])} ms."])
    for row in report["files"]:
        metrics = row["boundary_evaluation"]
        extras, misses = len(metrics["unmatched_predicted_boundaries"]), len(metrics["unmatched_gt_boundaries"])
        if extras or misses:
            lines.append(f"{row['wav']}: matched {metrics['matched_count']}/{metrics['gt_count']}, extra {extras}, missed {misses}.")
    lines.extend(["", *_noise_summary_lines(report), "", "MAE/RMSE use matched boundaries only.",
                  "Speech/Silence Power Contrast is not clean-speech SNR.",
                  "Frozen training lock unchanged; no test fitting or parameter selection."])
    return "\n".join(lines)


def save_test_report(report: dict[str, Any], output_path: Path, notes_path: Path | None = None) -> Path:
    """Save evaluation and its noise/error summary, plus optional Markdown."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    summary_path = output_path.with_name("noise_vs_error.json")
    summary_path.write_text(json.dumps(build_noise_vs_error_summary(report), indent=2, allow_nan=False) + "\n", encoding="utf-8")
    if notes_path is not None:
        notes_path = Path(notes_path)
        notes_path.parent.mkdir(parents=True, exist_ok=True)
        notes_path.write_text(render_results(report), encoding="utf-8")
    return output_path

