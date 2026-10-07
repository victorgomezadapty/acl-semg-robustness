# Data dictionary — verified Phase 1
Source: original README sections DATA & FILE OVERVIEW, METHODOLOGICAL INFORMATION and DATA-SPECIFIC INFORMATION; all 16 CSVs inspected. Both originals match the version-182584 Dryad hashes.

| File / field | Type | Meaning / units |
|---|---|---|
| healthy_iso{90,180}_{inv,uninv}.csv | Wide numeric table | Healthy-cohort sEMG; four files |
| patient_iso{90,180}_{inv,uninv}.csv | Wide numeric table | Patient-cohort sEMG; four files |
| healthy1 … healthy10 | Float, trailing blank padding | Participant sEMG, volts |
| patient1 … patient12 | Float, trailing blank padding | Participant sEMG, volts |
| *_time.csv: X [s] | Float | Time in seconds; eight paired files |

Each column is a participant ID (README). Pair it with the corresponding time file truncated to its nonempty length (explicit README instruction). No internal gaps exist; trailing blanks pad shorter recordings and must not be zero-filled.

## Parsed filename metadata
These are derived identifiers, not extra source columns: cohort = healthy/patient; condition = iso90/iso180; limb_label = inv/uninv (involved/uninvolved per README). IDs remain consistent across the four combinations in each cohort. Anatomical side, surgical-side key and control reference-leg assignment are absent. README calls the conditions 90/180 degrees; degrees/s is not explicitly documented.

## Documented signals
Bilateral vastus lateralis sEMG; sensor orientation follows muscle fibers at the distal third of the measured greater-trochanter to superior-lateral-patellar-pole distance. Delsys built-in software preprocessed data. Device model, filtering, rectification, envelope computation, calibration and MVC normalization are not documented. Do not label the export raw/unfiltered or normalized activation.

Sampling rate is not documented by the authors. Estimated per record as (samples − 1) / elapsed time, all 88 records give 1,923.9–1,925.9 Hz (median 1,925.9 Hz, the standard Delsys Trigno EMG rate); median-based estimates from consecutive differences vary with decimal precision and are not used. Both patient involved clocks have repeated timestamps: 44,999 for iso180 and 54,569 for iso90. Their median time difference is zero, yet their elapsed time gives the same rate as the other clocks, which is consistent with clock rounding rather than missing samples. The estimate is derived from the data, not a device specification. See [band-pass results](history/bandpass_results.md).

## Absent data
No torque, IMU axes, acceleration, demographics, mass, graft type, postoperative interval, repetition boundaries or clinical outcomes. README explicitly excludes accelerometer data. Strength LSI and torque–sEMG associations cannot be calculated. A future sEMG symmetry ratio requires a defined amplitude metric and limb interpretation and is not strength LSI.

## Audit fields

## Comprehensive derived fields

`semg_extended_features.csv` adds positive peak, signed mean, standard deviation and crest factor to amplitude metrics. Amplitudes retain volts; crest factor is peak absolute amplitude divided by RMS. `semg_extended_pairs.csv` retains both limbs, inv/uninv ×100, log(inv/uninv), and min/max ×100 for RMS, MAV and peaks. Nonpositive denominators yield undefined ratios, never artificial zeros.

`reports/exploratory_tests.csv` contains participant counts, mean differences, bootstrap intervals, test statistics, raw and family-adjusted p-values, standardized and rank effects. `exploratory_correlations.csv` contains Spearman associations. Block selection tables use sample counts and amplitude thresholds, not validated contraction timing. Definitions and test families are documented in [comprehensive methods](history/comprehensive_methods.md).

## Derived exploratory amplitude fields (2026-10-04)

`data/processed/semg_amplitude_features.csv`: rms_V, mav_V, median_abs_V, p95_abs_V, peak_abs_V (volts); capped RMS explicitly marked sensitivity; sample-defined block summaries with counts/remainders; QA flags. `semg_paired_amplitude.csv`: both limb values, inv/uninv ratios (unitless), min/max ×100 (percent amplitude balance). These are exported whole-task summaries, not normalized activation, contraction measurements or strength LSI. Full formulas and bootstrap definitions are in amplitude_methodology.md. Interpretation is in exploratory_results.md.
reports/signal_availability.csv records source file, participant_id, cohort, condition, limb_label, samples, empty cells, leading/internal/trailing padding, invalid and nonfinite counts, start/end/elapsed seconds, min/max volts, zero count and paired-row agreement. These are QA summaries, not clinical results. reports/schema_inventory.json retains exact headers; time_audit.json describes all clocks.

