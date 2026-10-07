# Record-mean sensitivity

The exported analysis is retained as a reproducibility baseline. Mean-centering is an additional retrospective specification, not proof that the record mean is instrument artefact. It does not replace filtering or recover contraction boundaries.

All 88 recordings and 44 participant-condition pairs were assessed with 21 methods before and after centering (1848 evaluations). Whole-RMS direction changes occurred in 0 pairs. Independent observations remain participants, not specifications or pairs across repeated conditions.

For healthy8/iso90 the ratio increases from 25.214 to 46.509. Removing the mean makes the denominator smaller; it does not resolve the extreme ratio. For that denominator, the mean accounts for 70.7% of the mean square, not 84% of the RMS amplitude. The identity RMS² = centered RMS² + mean² is checked for every recording.

![Centering sensitivity](../../reports/figures/centering_ratio_sensitivity.png)

Primary presentation: within-participant log-ratio sensitivity, including centering; cross-person absolute-voltage tests are supplemental acquisition-dependent descriptions. Centering is not declared physiologically correct by default. Band-pass filtering is evaluated separately in [bandpass_results.md](bandpass_results.md), using a sampling rate estimated from all exported clocks.

QA rules now identify length below 25% of the cohort-condition median and |mean|/RMS ≥0.1. These are review heuristics chosen retrospectively, not clinical thresholds. Since 2026-10-07 a pair with a short record is left out of the primary presentation (currently only healthy8/iso90; see [bandpass_results.md](bandpass_results.md)); all records remain in the sensitivity analyses.

Percentile bootstrap intervals remain exploratory and are not guaranteed to have nominal coverage at this sample size. Shapiro values are descriptive diagnostics only and never choose tests. No stronger clinical conclusion follows from changing an interval method.

Context: [CEDE normalization](https://doi.org/10.1016/j.jelekin.2020.102438), [processing choices](https://doi.org/10.1016/j.jelekin.2016.10.001), [original data](https://doi.org/10.5061/dryad.66t1g1k4j). Numerical results are calculated in this project, not taken from those papers.
