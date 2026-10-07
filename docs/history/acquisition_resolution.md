# Acquisition and quality decisions — 2026-10-04

Sources: original README; all 16 source CSVs; [Gutierrez et al., AHFE 2022](https://doi.org/10.54941/ahfe1001471), study-design section; [Khafagy and Hamza, 2026](https://doi.org/10.25259/JMSR_129_2026), dataset/methods sections. This update distinguishes established facts from related-study context.

| Question | Evidence obtained | Resolution and consequence |
|---|---|---|
| Device | Related original-author paper uses Delsys Trigno and Biodex | Context, not proof of exact model/configuration for every ZIP recording |
| Sampling frequency | Six exported clocks imply ~1,925.9 samples/s; original-author article does not provide exact EMG sampling for this export | Unresolved; no temporal filters, spectral analysis or invented Hz |
| Filters/normalization | README says built-in Delsys preprocessing; related article does not resolve settings | Unresolved; retain signed exported volts and avoid MVC claims |
| Test conditions | Reuse article explicitly describes 90/180°/s | Publication-level support; preserve iso90/iso180 identifiers and original README ambiguity |
| Patient limb labels | README uses involved/uninvolved; reuse article describes reconstructed/contralateral | Supports patient interpretation, but no anatomical side mapping |
| Healthy limb labels | Related paper compares dominant/non-dominant for a gait example | Does not identify which ZIP label is dominant; do not map inv/uninv automatically |
| Follow-up visits | Original-author paper describes a broader ongoing study, 11 patients and two planned assessments | Cannot assign visits/postoperative months to this 12-patient export |
| Short record | healthy8/iso90/uninv has 3,848 samples and unusually low amplitude in visual review | Flag and preserve; conduct explicitly labeled sensitivity analysis, no primary exclusion |
| Prominent transients | Visual review found isolated prominent peaks in several recordings | Flag with a transparent heuristic; no confirmed saturation or automatic removal |
| Duplicate clock values | All original sEMG samples remain available | Preserve samples and clocks; use sample index for ordering |

## QA policy

Primary data include all 88 recordings. A short-record review flag specifically identifies the observed healthy8/iso90/uninv case. Duplicate-time flags report observed equal consecutive times. A peak-review flag uses peak absolute amplitude >10 × the 95th percentile of absolute amplitude. This is an exploratory, analyst-defined screening heuristic, not a validated artifact detector. Extreme peaks may be physiological or acquisition artifacts; no exclusion follows from the flag.

The capped-amplitude sensitivity limits absolute values to their recording-specific 99.5th percentile **only in a separate feature calculation**. Original signals and primary metrics are unchanged. It measures influence of extreme values; it is not validated signal cleaning. The short-record sensitivity omits the affected control pair only from a separate iso90 descriptive summary (n=9 instead of 10).

## Remaining route to resolution

Exact hardware settings, processing/export history, control-limb mapping and task completeness require original protocol details or confirmation by the data custodians. No messages have been sent to authors. No public source inspected establishes these facts for this export. The three requested steps proceed through time-independent, explicitly exploratory analysis rather than treating these uncertainties as solved.
