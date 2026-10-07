# Methods

Retrospective analysis of [Dryad 2022](https://doi.org/10.5061/dryad.66t1g1k4j): 12 patients, 10 controls, bilateral vastus lateralis and two exported conditions. Source hashes precede loading; only trailing padding is removed. Primary presentation uses within-person log-ratio sensitivity across 11 RMS variants; MAV variants are additional estimands. Exported and centered signals remain separate.

Centering and the primary presentation were revised retrospectively after advisor review, not preregistered. Mean removal is not proof of artefact or a physiological filter. Sampling and processing are incompletely documented; no band-pass based on assumed sampling is applied. [Detailed centering methods](history/centering_results.md).

QA flags identify length below 25% of cohort-condition median, |mean|/RMS ≥0.1 and existing peak/clock concerns. These are review heuristics, not clinical thresholds or automatic exclusions.

Fixed exploratory tests, effects, Holm adjustment and participant percentile-bootstrap intervals remain supplemental. Shapiro values are descriptive and never choose tests. Small-sample interval coverage is uncertain; BCa does not automatically establish calibration. Absolute between-cohort voltages are acquisition-dependent supplemental descriptions.

Eleven synthetic scenarios use 100 seeded realizations and 21 specifications. References are constructed targets, not clinical labels. Error is |log(observed/target)|; quantiles describe simulated variability. [Full experiment](history/synthetic_scenario_study.md).

Context: [CEDE normalization](https://doi.org/10.1016/j.jelekin.2020.102438), [processing choices](https://doi.org/10.1016/j.jelekin.2016.10.001), [specification curves](https://doi.org/10.1038/s41562-020-0912-z). The last source's full inferential procedure is not implemented.
