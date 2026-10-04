# Final frozen Histogram test evaluation

Processed 4 test WAVs in one batch (1305 frames).
Frozen feature=logste, num_bins=40, smooth_window=1,
W=2, T*=-2.4375196566847372.
Framing: 25 ms / 10 ms; minimum internal silence: 200 ms.
The training lock's SHA-256 was unchanged before/after evaluation. No fitting or tuning was performed.

| File | Fs (Hz) | Duration (s) | Frames | Predicted boundaries | GT boundaries | MAE (ms) | RMSE (ms) | Speech/Silence Power Contrast (dB) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| phone_F2.wav | 16000 | 4.800000 | 478 | 4 | 2 | 45.000 | 46.704 | 24.773 |
| phone_M2.wav | 16000 | 2.800000 | 278 | 2 | 2 | 10.000 | 10.308 | 27.001 |
| studio_F2.wav | 44100 | 3.149478 | 313 | 2 | 2 | 2.506 | 2.506 | 49.296 |
| studio_M2.wav | 44100 | 2.381859 | 236 | 2 | 2 | 15.000 | 15.206 | 37.672 |

Noise vs. boundary error: Speech/Silence Power Contrast (dB)

| File | Environment | Speech/Silence Power Contrast (dB) | GT | Predicted | Matched | Extra | Missed | MAE (ms) | RMSE (ms) |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| phone_F2.wav | phone | 24.773 | 2 | 4 | 2 | 2 | 0 | 45.000 | 46.704 |
| phone_M2.wav | phone | 27.001 | 2 | 2 | 2 | 0 | 0 | 10.000 | 10.308 |
| studio_F2.wav | studio | 49.296 | 2 | 2 | 2 | 0 | 0 | 2.506 | 2.506 |
| studio_M2.wav | studio | 37.672 | 2 | 2 | 2 | 0 | 0 | 15.000 | 15.206 |

Environment-group observations (finite values only): phone: mean contrast 25.887 dB (2 files); studio: mean contrast 43.484 dB (2 files). The phone group has lower mean Speech/Silence Power Contrast than the studio group in this batch. These are descriptive observations from 4 test recordings, not evidence of a causal relationship between noise and boundary error. Environment groups follow supplied metadata; the project's phone/studio groups come from filename prefixes, not measured room conditions. Contrast also depends on speech level/content and is not clean-speech SNR. MAE/RMSE use matched boundaries only; extra and missed boundaries must also be considered.

Speech/Silence Power Contrast uses the LAB-based observed speech/silence power ratio:
10*log10(P_observed_speech/P_silence). Speech includes recording noise; this is not clean-speech SNR.
sil denotes silence; v and uv denote speech. Powers include DC and exclude uncovered samples.

## Matching and completeness

The frozen tolerance is 100 ms. Matching remains same-transition-type,
closest-first, one-to-one and noncrossing. MAE/RMSE use matched pairs only; no matches yields unavailable.
Missed and extra events are reported separately. Boundaries are midpoints between postprocessed frame centers.

| File | Matched / GT | Missed GT | Extra predicted |
|---|---:|---:|---:|
| phone_F2.wav | 2 / 2 | 0 | 2 |
| phone_M2.wav | 2 / 2 | 0 | 0 |
| studio_F2.wav | 2 / 2 | 0 | 0 |
| studio_M2.wav | 2 / 2 | 0 | 0 |

Total matches: 8 / 8; missed GT: 0; extra predicted: 2.
Pooled matched-boundary MAE: 18.126 ms; RMSE: 25.125 ms.

## Background power and label alignment

| File | Silence power | Observed speech power | Uncovered samples | Uncovered frame centers |
|---|---:|---:|---:|---:|
| phone_F2.wav | 3.82754366e-06 | 0.00114870468 | 0 | 0 |
| phone_M2.wav | 4.69317734e-06 | 0.00235283517 | 0 | 0 |
| studio_F2.wav | 2.47133344e-07 | 0.0210137405 | 418 | 0 |
| studio_M2.wav | 7.56925348e-07 | 0.00442843227 | 82 | 0 |

- studio_F2.wav: WAV end minus LAB end: 9.478 ms; labels are not extended.
- studio_M2.wav: WAV end minus LAB end: 1.859 ms; labels are not extended.

Powers are squared PCM-normalized amplitude, not calibrated watts.
Uncovered LAB gaps/tails are excluded from noise and frame-label scoring; LABs are not extended.

## Saved artifacts

output/test/histogram_test_evaluation.json contains per-frame features, raw/filtered decisions, LAB intervals,
predicted/GT boundaries, matched pairs, individual time errors, unmatched events and background-noise powers.
output/test/noise_vs_error.json contains the environment groups, power contrasts, complete boundary counts and cautious interpretation.
Training lock SHA-256: c4568831b70fa51e00516c8dafff94087abbc3abdbeef649540075501b91d052
Reproduce with python -m scripts.run_test_evaluation; the driver exposes no tuning overrides.
