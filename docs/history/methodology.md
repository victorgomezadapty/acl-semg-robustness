# Methodology

## Phase 1 acquisition and provenance

Pin source version 182584 (version 2). Retain original bytes. Verify both SHA-256 digests from the official manifest before inspection. Record ZIP member names, uncompressed sizes and hashes. Do not extract paths from the archive automatically. Separate source documentation, observed structure and interpretation.

For text tables, enumerate headers, row counts, row-width anomalies and empty cells. Empty cells are only structural missingness: undocumented sentinels remain unresolved. Non-tabular text and unsupported binary formats require follow-up; the inventory is not proof of full semantic inspection.

## Planned analytical principles

Use participants as independent units. Preserve paired limbs and repeated test conditions. Define outcomes and repetition aggregation before comparisons. Avoid pooled time-sample inference. Report individual values, descriptive distributions, suitable confidence intervals and effect sizes; account for repeated measures and exploratory multiplicity. Small-sample estimates require transparent uncertainty.

Do not compare raw sEMG across people without evaluating scaling and normalization. Do not align sensors by row index without clock evidence. Define torque sign and extension phases before calculating peak values. Body-mass normalization requires observed documented mass.

Phase 1 structural and numeric QA is complete. Original files passed hash validation. On 2026-10-04 the first exploratory amplitude analysis added whole-record RMS/MAV, sample-block summaries, paired ratios and participant bootstrap intervals. The subsequent comprehensive extension added 60 exploratory comparisons with effect sizes and family-specific Holm adjustment, 24 correlations, peak measures, block-selection sensitivity, publication comparisons and 22 profiles. No temporal filtering, clock reconstruction or ML is performed. This release contains sEMG/time only. See [comprehensive methods](comprehensive_methods.md), [results](comprehensive_results.md) and [coverage](analysis_coverage.md) for the current scope; the earlier amplitude documents retain the first-stage protocol.

