# Step 15: controlled training Histogram experiments

Only data/tinhieuhuanluyen WAVs were fitted; their LABs were read after prediction for evaluation.
Each fit pools all training frame features into one threshold shared by every recording.
LAB labels select parameters through training evaluation; the threshold fit itself receives no labels.

## Protocol

Baseline: logSTE, 40 bins, smoothing window 3, W=2 (the saved Step 9 fit).
Order: feature, bin count, smoothing window, weight. Each stage changes one factor while holding
the other three at the incoming winner. Candidate values were declared before execution.
This finite sequential search does not establish a global optimum or independent validation accuracy.

Selection rule: Require a successful fit/evaluation, complete LAB coverage of frame centers, and at least one boundary match. Minimize unmatched GT boundaries, then unmatched predicted boundaries, then pooled training MAE, then pooled training RMSE. Errors are rounded to 9 decimal places only for tie handling; exact ties keep the incoming configuration.

MAE and RMSE pool all matched boundary pairs across recordings, rather than averaging file RMSEs.
Matching uses existing same-transition, one-to-one, noncrossing, closest-first logic within 100 ms.
Missed and extra boundaries are recorded separately because matched-only errors can look misleadingly good.
Framing is 25 ms / 10 ms, minimum internal silence is 200 ms, epsilon is 1e-12.
Peak selection stays at minimum distance 4 bins and relative height 0.1 throughout.
Changing bin count changes the feature-space distance represented by those 4 bins; this heuristic was not tuned.

There are 14 unique fits and 17 stage observations; repeated points reuse their fit.

| Training WAV | Fs (Hz) | Frames |
|---|---:|---:|
| phone_F1.wav | 16000 | 322 |
| phone_M1.wav | 16000 | 414 |
| studio_F1.wav | 44100 | 284 |
| studio_M1.wav | 44100 | 271 |

Total pooled frames: 1291.

## All observations

| Stage | ID | Feature | Bins | Window | W | M1 | M2 | T | MAE (ms) | RMSE (ms) | Matches/GT | Extra | Failure status |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---|
| feature | config_01 | logste | 40 | 3 | 2 | -3.206248 | 1.867359 | -1.515046 | 14.376417 | 20.309399 | 8/8 | 2 | none |
| feature | config_02 | ste | 40 | 3 | 2 | 19.983088 | 25.140013 | 21.702063 | 67.494331 | 67.494331 | 1/8 | 5 | none |
| feature | config_03 | ma | 40 | 3 | 2 | 31.341970 | 51.127917 | 37.937286 | 31.498866 | 35.301223 | 5/8 | 9 | none |
| feature | config_04 | logma | 40 | 3 | 2 | -0.027982 | 1.113921 | 0.352652 | 23.333333 | 32.754253 | 6/8 | 2 | none |
| num_bins | config_01 | logste | 40 | 3 | 2 | -3.206248 | 1.867359 | -1.515046 | 14.376417 | 20.309399 | 8/8 | 2 | none |
| num_bins | config_05 | logste | 20 | 3 | 2 | -2.975630 | 0.714267 | -1.745664 | 14.376417 | 20.309399 | 8/8 | 2 | none |
| num_bins | config_06 | logste | 30 | 3 | 2 | -3.129375 | 1.790486 | -1.489421 | 14.376417 | 20.309399 | 8/8 | 2 | none |
| num_bins | config_07 | logste | 50 | 3 | 2 | -3.252372 | 1.544493 | -1.653417 | 14.376417 | 20.309399 | 8/8 | 2 | none |
| num_bins | config_08 | logste | 60 | 3 | 2 | -3.590612 | 1.944232 | -1.745664 | 14.376417 | 20.309399 | 8/8 | 2 | none |
| smooth_window | config_01 | logste | 40 | 3 | 2 | -3.206248 | 1.867359 | -1.515046 | 14.376417 | 20.309399 | 8/8 | 2 | none |
| smooth_window | config_09 | logste | 40 | 1 | 2 | -3.667485 | 0.022411 | -2.437520 | 10.626417 | 17.852381 | 8/8 | 2 | none |
| smooth_window | config_10 | logste | 40 | 5 | 2 | -3.206248 | 1.406122 | -1.668791 | 14.376417 | 20.309399 | 8/8 | 2 | none |
| smooth_window | config_11 | logste | 40 | 7 | 2 | -2.283774 | 0.944885 | -1.207554 | 16.876417 | 21.212870 | 8/8 | 6 | none |
| weight | config_09 | logste | 40 | 1 | 2 | -3.667485 | 0.022411 | -2.437520 | 10.626417 | 17.852381 | 8/8 | 2 | none |
| weight | config_12 | logste | 40 | 1 | 1 | -3.667485 | 0.022411 | -1.822537 | 13.126417 | 19.201758 | 8/8 | 2 | none |
| weight | config_13 | logste | 40 | 1 | 3 | -3.667485 | 0.022411 | -2.745011 | 12.500000 | 19.247622 | 7/8 | 2 | none |
| weight | config_14 | logste | 40 | 1 | 5 | -3.667485 | 0.022411 | -3.052502 | 8.928571 | 9.954444 | 7/8 | 0 | none |

## Stage selections

| Factor | Incoming value | Retained value | Configuration |
|---|---|---|---|
| feature | logste | logste | config_01 |
| num_bins | 40 | 40 | config_01 |
| smooth_window | 3 | 1 | config_09 |
| weight | 2.0 | 2.0 | config_09 |

The table above supplies the comparison behind each retained setting; the incoming point wins exact ties.

## FINAL TRAINING CONFIGURATION

```text
feature = logste
num_bins = 40
smooth_window = 1
W = 2
M1 = -3.66748502780843
M2 = 0.0224110855626378
T* = -2.43751965668474
locked = true
```

The retained configuration matches 8/8 GT boundaries
with 2 extras. Its pooled training MAE is 10.626417 ms
and RMSE is 17.852381 ms.
Baseline: 8/8 matches, 2 extras,
MAE 14.376417 ms, RMSE 20.309399 ms.
Each stage retains the best candidate under the declared rule; ties retain the incoming setting.

logSTE retained all 8 GT boundaries, whereas STE, MA and logMA matched only 1, 5 and 6 respectively
at the baseline settings. All tested bin counts produced identical boundary errors and counts,
so the existing 40-bin setting was retained. Window 1 reduced both errors with the same 8 matches
and 2 extras; it means the moving-average function leaves the histogram unchanged (no smoothing).
With this window, W=2 performed better than W=1; W=3 and W=5 each missed one GT boundary.
W=5's lower matched-only MAE/RMSE therefore did not justify selecting it.

The final model still produces two extra transitions in phone_F1.wav; these are recorded rather
than hidden. All 14 configurations successfully selected two peaks (no fit failures in this grid).
Training observations alone justify this choice; performance on unseen recordings is not established here.

## Final per-recording evaluation

| WAV | Matches/GT | Extra | MAE (ms) | RMSE (ms) |
|---|---|---:|---:|---:|
| phone_F1.wav | 2/2 | 2 | 5.000000 | 5.590170 |
| phone_M1.wav | 2/2 | 0 | 5.000000 | 5.590170 |
| studio_F1.wav | 2/2 | 0 | 2.505669 | 2.505669 |
| studio_M1.wav | 2/2 | 0 | 30.000000 | 34.728254 |

## Lock and reuse

output/training/final_histogram_configuration.json is the authoritative final lock, including the frozen threshold
and Histogram debug arrays. The runner refuses to overwrite it. Earlier training reports and notebook baseline
remain historical records; use the final lock for subsequent evaluation.

```python
from pathlib import Path
from src.config import load_locked_histogram
config, model = load_locked_histogram(Path("output/training/final_histogram_configuration.json"))
# Prediction reuses model.value; no fitting occurs when loading the lock.
```

Reproduce once in a fresh checkout without a final lock using python -m scripts.run_training_experiments.
Detailed matched pairs, individual errors and alignment warnings are in the experiment JSON.
Final per-frame predictions and ground truth are in histogram_final_training_evaluation.json.
No production signal-processing or Histogram function was changed for these experiments.

## Verification

python -m compileall -q . passed. The pytest regression suite passed with 124 tests and 128 subtests;
one test was deliberately deselected (test_all_project_wavs), because it reads both real datasets.
Synthetic tests check one-factor control, failure recording, boundary-count priority, pooled errors,
restoration of the frozen model and refusal to refit when a lock exists. Saved artifacts were also
checked for consistent frame counts, the common threshold and one-factor stage configurations.
