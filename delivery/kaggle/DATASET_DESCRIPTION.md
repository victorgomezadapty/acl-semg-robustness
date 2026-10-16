# ACL sEMG: Dryad 2022 reproducibility bundle

This is a repackaged input bundle for an independent methodological portfolio study. It is **not a new data collection**, a competition entry, or a clinically validated return-to-sport tool.

## Original data and attribution

Gutierrez, Hart and Boukhechba (2022), Dryad: https://doi.org/10.5061/dryad.66t1g1k4j. The original measurements are released under **CC0**, as stated by the source metadata. The original ZIP and README are preserved. The project code and original documentation are **MIT licensed**; see `docs/CODE_LICENSE.md`. These component licenses remain distinct.

The export contains bilateral vastus lateralis surface EMG signals and time vectors for 22 participants (12 ACL reconstruction, 10 controls), yielding 88 records and 44 bilateral pairs. Signal units are volts and time units are seconds. Torque, MVC references, IMU measurements and clinical follow-up outcomes are unavailable. Control-side labels do not establish dominance.

## What the project adds

A retrospective audit compares 21 amplitude-summary specifications, centering and conditional 20–450 Hz filtering. Controlled synthetic scenarios test sensitivity to pauses, isolated spikes, noise and unequal sensor gains. This demonstrates methodological failure modes and reproducible analysis, without establishing clinical utility or scientific priority.

Across the original specifications, 13 of 44 pairs change direction; 10 do so across the 11 RMS specifications. A documented short-record rule leaves 43 primary pairs, with all 44 retained in sensitivity analyses. The synthetic experiment has 11 scenarios, 100 realizations and 21 specifications (23,100 results). Synthetic signals are explicitly simulations, not additional participants.

## Reproduce and review

Attach this dataset to the accompanying Python notebook and run all cells on CPU. Kaggle recursively expands ZIP archives. The original archive therefore travels as `data/raw/ACL_data.zip.bin`; the notebook restores its `.zip` filename without changing bytes before SHA-256 verification. The notebook uses attached files and requires no internet downloads.

The bundle includes `src/`, `scripts/`, `tests/`, and documentation. Read `docs/reproducibility.md` for commands, expected outputs and troubleshooting; `docs/decision_log.md` explains the reasons, alternatives and checks for each major decision. The review methods, results and limitations include scientific citations. Local pinned requirements describe the validated local environment; the notebook prints Kaggle runtime versions.

Filtering assumes approximately uniform acquisition; the exported clock does not prove this. RMS retention is an amplitude comparison, not a direct measure of energy outside the passband. Stable group medians can coexist with substantial individual changes. Exploratory nonsignificance does not establish equivalence. No result supports clinical clearance or predicts reinjury.

Published bundle SHA-256: `e26e10f3e7964b0e4eaba910ebe72e634e4a34132b677aaf5b9ae5504788bb94`.
