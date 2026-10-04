# Step 18: one-command Histogram demonstration

From the project root, run:

```powershell
python main.py
```

This loads the already trained model from
output/training/final_histogram_configuration.json. It prints the training
feature, num_bins, smooth_window, W, M1, M2 and T* before processing test data.
The final demonstration deliberately uses this frozen model rather than
training again. A missing/invalid lock or unavailable data fails explicitly;
there is no fallback that estimates a threshold from test recordings.

The existing training choices are:

```text
feature = logste
num_bins = 40
smooth_window = 1
W = 2
M1 = -3.667485027808425
M2 = 0.022411085562637822
T* = -2.4375196566847372
```

All WAVs in data/tinhieukiemthu follow the same load, frame, feature, prediction,
200 ms postprocessing and boundary evaluation path. Frame duration/shift are
25/10 ms using each recording's actual Fs. Every recording uses the same T*;
LAB is read after prediction for evaluation and background-power analysis.

The command prints a final table with filename, Fs, duration, frame count,
predicted/GT boundary counts, MAE/RMSE and the documented noise contrast.
It reports unmatched boundaries separately from matched-only errors.
It saves one two-panel Figure per WAV, the detailed JSON report and Markdown.
The upper panel overlays the waveform with the selected feature and T* on a
second vertical axis, plus predicted boundaries in blue and LAB boundaries in
red. The lower panel compares the predicted and ground-truth Speech/Silence
regions. Titles include the filename, frozen feature/threshold and MAE/RMSE:

- output/test/figures/*.png
- output/test/histogram_test_evaluation.json
- docs/notes/histogram_test_evaluation.md

The default command saves and displays all four final Figures together.
The result table and reports are ready before the display waits for the windows
to close. Use python main.py --no-show when only saved artifacts are needed.
The older python main.py --show command remains accepted, but is unnecessary.
There are no intermediate Histogram windows or parameter override options.
Runtime dependencies are declared in requirements.txt.

main.py imports only standard-library and src modules. Configuration/model
loading lives in src/config.py, evaluation and freeze checks in src/pipeline.py,
plotting in src/evaluate/plot.py, and formatting/export in src/evaluate/reporting.py.
Earlier research commands still delegate to these shared APIs. No Histogram or
STE/MA mathematics is implemented in main.py, and no legacy algorithm imports
or branches remain.

## Verified execution

python -m compileall . and the complete pytest suite passed; no tests were
excluded. Integration tests cover use of a
saved model without a training-data directory, the printed training information,
the final table/artifacts, default display of four Figures, save-only mode,
invalid locks, missing data and mutation rejection.

The real demonstration processed four WAVs / 1305 frames and saved four Figures.
It matched 8/8 GT boundaries, with two extra predictions in phone_F2. Pooled
matched-boundary MAE/RMSE were 18.126/25.125 ms. The original training lock's hash
remained unchanged, and no tuning was performed.

See [the full result table](histogram_test_evaluation.md) and
[the Figure gallery](histogram_final_visualization.md).

## Project cleanup

Removed the unused src/audio/dataset.py skeleton and the unfinished legacy
load_datasets, train_method, predict_signal and run_pipeline functions.
Removed the unused normalize() placeholder while retaining log_transform(),
which the feature pipeline, notebook and tests import.
Removed the unreferenced training_speech_mask() and evaluate_predictions()
helpers from src/pipeline.py; the shared training/test evaluation path remains.
The duplicate test/sampleFigure BMPs illustrated an unrelated filtering task
and were not fixtures or project references; both were removed.

Package __init__.py files remain, with brief descriptions. They identify the
audio, features, segmentation and evaluation packages; empty package markers
were intentional, not unfinished signal-processing code. Keep training records,
the frozen model, notebook, experiment scripts and assignment/reference documents
for reproducibility and presentation. Python/pytest caches can be regenerated
and are ignored alongside temporary Word lock files.
