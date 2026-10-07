# Exploratory amplitude protocol — version 1

Defined 2026-10-04 before reviewing the generated group comparisons. Purpose: describe exported task recordings, not infer contraction-specific activation, strength, recovery stage or RTS clearance.

## Primary metrics

Per participant × condition × source limb label, remove only trailing blank padding. Use every remaining sample in original order. RMS = sqrt(mean(x²)); mean absolute value (MAV) = mean(abs(x)); both in volts. Plot in microvolts with explicit conversion ×1,000,000. No demean, filter, MVC normalization or resampling is applied. Record duration differences and QA flags separately.

Whole-record estimates include recorded rest and transitions. This is a deliberate limitation: no validated boundaries identify active contractions. Do not call these cycle-level or maximal activation metrics. No automatic active/rest split is implemented because acquisition preprocessing and task boundaries are insufficiently established. All participants remain in the primary analysis.

## Supporting and sensitivity summaries

Absolute median, absolute 95th percentile and peak absolute amplitude describe the exported distribution. Peak is not a primary endpoint. Nonoverlapping blocks of 256, 512 and 1,024 **samples**, from original index zero, yield median and 90th-percentile block RMS. Incomplete final blocks are omitted only from block summaries and their remainder counts are recorded. They are not seconds or repetitions. All samples remain in whole-record RMS/MAV. Sample-defined blocks can assess aggregation sensitivity but cannot establish a clinically meaningful duration.

A separate RMS with amplitudes capped at the within-record 99.5th percentile explores spike influence. A separate control iso90 analysis omits the flagged short pair. Neither replaces the primary values. No significance-driven selection of cleaning settings is permitted.

## Pairing and group summaries

Compute inv/uninv amplitude ratio separately within each participant and condition; zero denominator gives an undefined value. Also retain 100 × min(amplitude)/max(amplitude) as an orientation-independent balance description, alongside both absolute values. These are **sEMG amplitude ratios**, not strength LSI, and no 90% threshold or ready-to-play category is used. Control limb orientation remains unresolved.

Report n, median and IQR of participant ratios for each cohort/condition. A deterministic bootstrap samples participants within each cohort/condition (5,000 resamples, seed 20261004) and provides percentile 95% intervals for the median. This is descriptive exploratory uncertainty, not clinical reference ranges. Do not resample signal points as independent participants. Condition summaries from the same people are correlated; separate bootstrap intervals are not a test of a condition effect. No group p-values or predictive models are generated.

## Reproducibility

`src/features/amplitude.py` defines features. `scripts/exploratory_amplitude.py` reads hash-verified sources, writes both derived CSV tables, group summaries and plots. Run `python scripts/exploratory_amplitude.py` from the repository root. Dependencies are pinned in requirements.txt. Derived tables are regenerated locally; data/processed is excluded from Git by design.
