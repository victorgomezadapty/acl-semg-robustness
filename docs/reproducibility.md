# Reproduce the project from a clean checkout

Start with the [case study](review_case.md). The [decision record](decision_log.md) explains why each step exists. This guide reproduces a measurement sensitivity analysis, not a clinical prediction model.

For the independent ENABL3S extension, follow the [delivery guide](../delivery/enabl3s/README.md): a lightweight notebook reviews verified derived results, while the separate raw-data route downloads approximately 5.9 GB and recalculates the nine-participant cohort. The two checks have distinct execution claims.

## 1. Obtain the exact source files

Download `ACL_data.zip` and `README_acl.txt` from [Dryad DOI 10.5061/dryad.66t1g1k4j](https://doi.org/10.5061/dryad.66t1g1k4j), the pinned release published 2022-06-10. Put both in `data/raw/` without extracting or editing the ZIP. They are excluded from Git; a repository checkout alone therefore does not supply measurements. Original data are CC0 according to source metadata; project code/docs have their [own license](CODE_LICENSE.md).

Expected SHA-256:

```text
ACL_data.zip: 7bac99ea5425cc356f261a641b2123bceeae323039c5a201d0f6cd0f5a1f2a24
README_acl.txt: de59715a6707972f45ba59e628b7dc85b6f23084eae2e3eb7d6eec89bfbefece
```

A hash mismatch stops the inspector/loader. Check the release and whether the download is an HTML page; do not bypass verification just to obtain results.

## 2. Install the tested environment

Tested on Windows with Python 3.14, NumPy 2.5.2, SciPy 1.18.1 and Matplotlib 3.11.2. Additional notebook/test dependencies are in `requirements-verification.txt`. Internet access is needed for installation and the original download; subsequent analysis is offline. No account tokens or GPU are needed.

In PowerShell, change to your checkout. Keep the environment outside OneDrive so package files are not synchronized. These variables are local shell variables, not credentials:

```powershell
cd '<your checkout path>'
$aclEnv = Join-Path $env:USERPROFILE '.venvs\acl-semg'
python -m venv $aclEnv
$aclPython = Join-Path $aclEnv 'Scripts\python.exe'
& $aclPython -m pip install -r requirements.txt -r requirements-verification.txt
& $aclPython -m pip check
```

Activation is unnecessary. Use a Python 3.14 executable for `python -m venv`; check `python --version` first. macOS/Linux equivalents are `python3.14 -m venv .venv`, `.venv/bin/python -m pip install -r requirements.txt -r requirements-verification.txt`, followed by the same scripts with `.venv/bin/python`. Those platforms have not been independently verified here.

## 3. Check, then regenerate

```powershell
& $aclPython scripts/inspect_dataset.py
& $aclPython -m pytest -q
& $aclPython -m ruff check src scripts tests
& $aclPython -m ruff format --check src scripts tests
& $aclPython scripts/run_all.py
```

The pipeline checks amplitude/statistical definitions, reviews exported signals, creates descriptive features and exploratory statistics, compares amplitude specifications, evaluates mean-centering and filtering, runs synthetic scenarios, and builds the viewer. It overwrites generated outputs; keep a snapshot or commit if you want to compare versions. The raw ZIP is not overwritten. Literature searches and external repository downloads are separate research-stage scripts, not offline pipeline requirements.

## 4. Check the expected output contract

| Output | Expected meaning/count |
|---|---|
| `reports/comprehensive_summary.json` | 88 recordings, 22 people, 44 participant-condition pairs, 60 exploratory comparisons |
| `reports/robustness_summary.json` | 924 evaluations; 43 primary pairs after the retrospective short-record rule; all 44 retained; 13 main crossings across 21 methods, 10 across RMS methods |
| `reports/centering_checks.json` | 1,848 evaluations; no whole-RMS direction reversal after centering |
| `reports/bandpass_checks.json` | 1,848 evaluations; average-rate estimate about 1,925.9 Hz; 1 main whole-RMS crossing, RMS-method crossings 10 exported versus 8 filtered |
| `reports/bandpass_signal_audit.csv` | 88 rows; `rms_retention_ratio` is amplitude retention; `filtered_mean_square_ratio` is its square |
| `reports/synthetic_scenario_checks.json` | 23,100 evaluations and passed constructed invariants |
| `reports/analysis_index.html` | Local participant signal viewer; open in a browser |

Interpret ratios with [methods](review_methods.md) and [limitations](review_limitations.md), not as clearance scores. Fixed seeds stabilize numerical simulation outputs in the tested environment. Different operating systems, dependency builds or plotting libraries can change bytes or tiny floating-point results; figure hash identity is not a scientific requirement.

## 5. Build and verify the publication package

```powershell
& $aclPython scripts/prepare_kaggle.py
& $aclPython scripts/verify_kaggle_delivery.py
```

Run these after `run_all.py` so outputs and documentation are current. Alternatively, `scripts/run_all.py --verify-delivery` regenerates and verifies everything. The verifier executes the supplied notebook against the unpacked input archive, using its invoking Python, then checks expected summaries. Generated verification folders are excluded from Git. `delivery/kaggle/local_verification.json` records the executed archive hash and local result; it is not proof of a Kaggle run.

For Kaggle, upload `acl_semg_input.zip` as a correctly attributed Dataset, import `acl_semg_robustness.ipynb`, attach that Dataset and run all cells on CPU. The notebook explains the decisions and shows the band-pass results. Preserve the original inner ZIP. Actual Kaggle verification stays `false` until the corresponding version runs there and its output is checked. See [upload instructions](../delivery/kaggle/UPLOAD_INSTRUCTIONS.md).

## Troubleshooting and adaptation

- **Missing file/hash error:** obtain the pinned original release, not another file renamed to match.
- **Import error:** run the same environment's Python for pip, tests and scripts; `pip check` identifies incompatible dependencies.
- **Clock error:** backward, nonfinite or nonadvancing times are rejected. Duplicates are allowed; agreement does not prove uniform acquisition.
- **Short/constant signal:** undefined block selections and zero denominators must remain undefined; do not replace them with fabricated values.
- **Multiple Kaggle inputs found:** attach exactly one source bundle or set the documented `ACL_INPUT_ROOT` for local verification.
- **Another dataset:** implement a separate provenance-checked loader and documented mappings for people, muscles, sides, units and tasks. Do not disable the Dryad hash check. Reconsider rates, eligibility and all thresholds; do not transfer clinical interpretations from these simulations.

The decision record and changelog distinguish inherited methods, retrospective choices and constructed scenarios. That distinction is part of reproducing the reasoning, not just the numbers.
