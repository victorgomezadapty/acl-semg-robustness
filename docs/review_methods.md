# Methods

[Why each choice was made](decision_log.md) · [Reproduce from a clean checkout](reproducibility.md).

Endpoint rates are averages: timestamps must be finite and nondecreasing with positive span. Duplicate times remain allowed. Agreement between averages does not prove uniform sampling or establish rounding as the cause of duplicates; uniform sample spacing is a conditional assumption for this filter. RMS-retention thresholds identify attenuation for review, not its physiological cause or a frequency-energy partition.

Retrospective analysis of [Dryad 2022](https://doi.org/10.5061/dryad.66t1g1k4j): 12 patients, 10 controls, bilateral vastus lateralis and two exported conditions. Source hashes precede loading; only trailing padding is removed. Primary presentation uses within-person log-ratio sensitivity across 11 RMS variants; MAV variants are additional estimands. Exported and centered signals remain separate.

Centering and the primary presentation were revised retrospectively after advisor review, not preregistered. Mean removal is not proof of artefact or a physiological filter. [Detailed centering methods](history/centering_results.md).

The authors do not state the EMG sampling rate. It is estimated from every exported clock as (samples − 1) / elapsed time; all 88 agree within 0.11% (median 1,925.9 Hz, an average-rate estimate). A Butterworth prototype N=4, SOS 20–450 Hz band-pass (order 8 per direction; effective order 16 after forward/backward filtering) is then evaluated as an additional specification, alongside the exported baseline. The RMS retention (band-passed RMS / mean-centered RMS) is reported per record as a quality indicator; values below 0.8 are flagged for review, not excluded. The exact built-in Delsys preprocessing remains undocumented. [Band-pass methods and results](history/bandpass_results.md).

QA flags identify length below 25% of cohort-condition median, |mean|/RMS ≥0.1, RMS retention below 0.8 and existing peak/clock concerns. These are review heuristics, not clinical thresholds. One rule is used for the primary presentation: a participant-condition pair whose record falls below 25% of the cohort-condition median length is left out, because a whole-record ratio between a full task and a short fragment does not compare like with like. Only healthy8/iso90 meets it. This exclusion was decided retrospectively (2026-10-07); every analysis is also reported with all 44 pairs.

Fixed exploratory tests, effects, Holm adjustment and participant percentile-bootstrap intervals remain supplemental. Shapiro values are descriptive and never choose tests. Small-sample interval coverage is uncertain; BCa does not automatically establish calibration. Absolute between-cohort voltages are acquisition-dependent supplemental descriptions.

Eleven synthetic scenarios use 100 seeded realizations and 21 specifications. References are constructed targets, not clinical labels. Error is |log(observed/target)|; quantiles describe simulated variability. [Full experiment](history/synthetic_scenario_study.md).

Context: [CEDE normalization](https://doi.org/10.1016/j.jelekin.2020.102438), [processing choices](https://doi.org/10.1016/j.jelekin.2016.10.001), [specification curves](https://doi.org/10.1038/s41562-020-0912-z). The last source's full inferential procedure is not implemented.
