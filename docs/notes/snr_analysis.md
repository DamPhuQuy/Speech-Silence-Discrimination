# Speech/Silence Power Contrast (dB): background-noise analysis

The assignment asks for environmental noise/SNR analysis but does not define
an operational formula. The original `snr.py` skeleton explicitly leaves the
power convention pending. CS425 Audio and Speech Processing (PDF page 34)
describes maximum waveform dB level relative to a noise floor; it does not
specify averaging all LAB speech samples or subtracting noise power. These
quantities must not silently be treated as interchangeable.

The lecturer's requirement is: "Chú ý khảo sát ảnh hưởng của mức nhiễu nền
(SNR) của môi trường thu âm." See
[assignment](../assignments/Hướng%20dẫn%20BT%20-%20Phân%20đoạn%20tín%20hiệu%20thành%20tiếng%20nói%20và%20khoảng%20lặng_XLTHS_GK%202026.docx).
It provides no clean reference, noise-only reference or specific SNR formula.
The roadmap and supplied references do not prescribe a numerical LAB-based
clean-SNR calculation either. The user-facing metric is therefore named
**Speech/Silence Power Contrast (dB)** throughout final reports.

The supported analysis justified by the existing labeled-speech/silence API is:

- Silence background power: mean(x[n]**2) over all LAB `sil` samples.
- Observed speech power: mean(x[n]**2) over all LAB `v` and `uv` samples.
- Powers pool samples, not equally weighted interval means. DC is included.
- PCM-scaled inputs have squared normalized-amplitude units, not watts. Different
  microphones/gains prevent interpreting these powers as calibrated acoustic levels.
- Sample n is at n/Fs seconds. Intervals are [start, end); gaps/unlabeled tails
  are excluded and counted, never filled from detected labels.

`analyze_background_noise(audio)` reports those quantities without selecting an
SNR metric. The existing `estimate_snr_db` and `report_snr` entry points require
an explicit `definition="speech_to_silence_power"` to compute:

    observed_power_contrast_db = 10 * log10(P_observed_speech / P_silence)

Those function names are retained for backward compatibility; their result is
the observed power contrast, not an estimate of clean-speech SNR.

This opt-in convention is an analysis proxy, not a prescribed assignment formula
or clean-speech SNR. Speech intervals still contain noise. No clean-signal power
subtraction, peak-based noise-floor metric, DC removal, or stationary-noise model
is introduced. The ratio cancels a shared recording gain, but depends on speech
level/content as well as noise. It cannot alone prove that one environment is
noisier than another.

Missing LAB speech/silence samples yield an unavailable power (`None`); the ratio
raises `ValueError`. Exact zero silence power with positive observed speech gives
+infinity; the converse gives -infinity. Both zero is undefined and raises. No
arbitrary epsilon changes these cases. Callers exporting JSON must encode
nonfinite ratios explicitly rather than emit invalid numeric values.

All analysis operates on already loaded AudioSignal data. LAB is evaluation-only;
these helpers do not import or call Histogram training, thresholding, prediction,
or dataset loaders. No test recordings are needed to verify the implementation.

## Noise versus boundary error

`python main.py --no-show` reuses the frozen training model, evaluates all actual
test files and saves `output/test/noise_vs_error.json` beside the complete
evaluation JSON. The console and Markdown report show the same concise table:
filename, recording group, contrast/status, GT/predicted/matched boundary counts,
extra/missed events and matched-boundary MAE/RMSE in milliseconds.

Recording groups `phone` and `studio` come only from recognized filename
prefixes. They identify dataset groups, not measured room conditions or known
microphones. Unknown names retain null metadata and display as `unknown`;
their contrast/error values remain in the table. Group means exclude unavailable
or infinite contrasts and unknown groups. The interpretation reports the number
of recordings and states that the observations do not establish a causal
relationship between noise and boundary error. No parameters are selected from
this table and the training lock remains unchanged.
