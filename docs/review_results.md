# Results

All 88 recordings are analysed. The primary presentation uses 43 participant-condition pairs; healthy8/iso90 is excluded because its uninv record lasts 2.0 s (next shortest of 88: 10.5 s). Thirteen primary pairs (11 people) cross ratio 1 across 21 specifications; ten cross across the 11 RMS specifications. With all 44 pairs the counts are identical, because the excluded pair never crosses 1. This is not clinical reclassification. [Baseline audit](history/robustness_results.md).

Centering adds 1,848 evaluations and changes no whole-RMS direction. The excluded healthy8/iso90 ratio increases from 25.214 to 46.509. Its denominator mean accounts for 70.7% of mean square; this alone does not establish instrument artefact. [Centering outputs](history/centering_results.md).

All 88 exported clocks imply average rates of 1,923.9–1,925.9 Hz. A 20–450 Hz band-pass (1,848 further evaluations) changes the whole-RMS direction in 1 of 43 primary pairs (patient7/iso180, 0.995 → 1.000). RMS-specification crossings fall from 10 to 8. Primary median whole-RMS ratios move by at most 0.05 (healthy iso180: 0.933 → 0.981; other cells ≤0.004). Median RMS retention is 0.986; four control uninv records fall below 0.8 (healthy9 iso90 0.62, healthy9 iso180 0.70, healthy8 iso90 0.71, healthy3 iso180 0.79). Group medians remain relatively stable, but individual ratios change: healthy9/iso90 rises from 0.208 to 0.333 (about 60%). Low RMS retention does not identify the cause of attenuation or quantify energy outside a frequency band. [Band-pass outputs](history/bandpass_results.md).

Among 23,100 synthetic evaluations, a constructed spike reverses RMS direction in 100/100 realizations versus 0/100 with limited RMS. Limiting also distorts a desired sustained event. Unknown unequal gain remains across all methods. [All scenarios and assumptions](history/synthetic_scenario_study.md).

No baseline comparison survives family-specific Holm adjustment; this is not equivalence. Two inspected external repositories cannot execute direct validation. [Eligibility evidence](history/external_validation_feasibility.md). Numerical results are generated locally, not taken from cited articles.
