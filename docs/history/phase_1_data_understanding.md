# Phase 1 — Data Understanding
Completed 2026-10-04: acquisition, original README review and structural/numeric inspection of all 16 CSVs. No cleaning, analytical feature extraction or ML was performed. Documentation uncertainties remain unresolved.

## Provenance
The user supplied the full Dryad ZIP in the project root. It contains ACL_data.zip and README_acl.txt, copied unchanged into data/raw. Both match the official version-182584 SHA-256 hashes and sizes. Earlier validation HTML remains in reports/access_diagnostics.

## Structure and findings
Eight sEMG matrices: healthy/patient × iso90/iso180 × inv/uninv, with eight paired time CSVs. Healthy matrices have 10 participant columns, patient matrices 12. All 22 IDs have nonempty data in all four combinations: 88 recordings, not 88 independent people.

- No malformed row widths, internal/leading empty cells, invalid numbers or nonfinite sEMG values.
- All empty cells are trailing padding, consistent with the README's variable recording durations.
- Lengths: 3,848–76,960 samples. Endpoint spans: 1.99748–39.9595 seconds; problematic clocks limit timing precision.
- Every paired time/signal matrix has matching row counts.
- Six clocks increase strictly, with average implied rate around 1,925.9 samples/s.
- patient_iso180_inv_time.csv has 44,999 duplicate consecutive timestamps; patient_iso90_inv_time.csv has 54,569. No backwards steps. Median interval is zero for both.
- healthy8 / iso90 / uninv is the shortest record (~2 seconds); task completeness is unknown.

## Scope correction
The package contains sEMG and time only. No torque or IMU files exist; README explicitly excludes accelerometer data. Strength, strength LSI, torque–sEMG and IMU analyses cannot be executed from this release. No participant characteristics or longitudinal follow-up table is provided.

## Documentation problems
Sampling rate, precise Delsys preprocessing, calibration, normalization, control limb assignment, surgical/anatomical laterality, degrees/s interpretation, repetitions, timestamp precision and short-recording completeness are unresolved. README says no multiple versions; API reports version 2. Provenance is pinned to version 182584.

## Next phase proposed
1. Build a long-form loader preserving original labels and sample order, removing only padding.
2. Review representative waveforms and the shortest signal before selecting amplitude summaries.
3. Resolve clocks before filtering or spectral analysis. Prefer documented sample-rate/export information; a uniform reconstructed clock is an alternative assumption requiring explicit justification and sensitivity checks. Neither has been implemented.
4. Confirm preprocessing before considering RMS or mean absolute amplitude and justify aggregation windows and task boundaries.
5. Prioritize individual paired descriptions if normalization remains unavailable; interpret between-person amplitudes cautiously. Log any justified exclusions.

Obtain separate documented torque data if strength analysis is essential. No clinical conclusions or clearance labels follow from this audit.

