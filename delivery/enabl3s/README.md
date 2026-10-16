# ENABL3S methodological extension — v0.2.0

Prepared 2026-10-16. This delivery completes the independent methodological extension of the existing Dryad project. Start with the [portfolio case](../../docs/review_case.md), then the [full cohort report](../../docs/enabl3s_cohort_results_v1.md).

Nine non-pilot participants were assessed under rules fixed after AB191 but before the other outcomes. Six meet those rules and have all eleven primary RMS specifications; three are excluded. Two of six cross ratio 1 across methods. Sensitivities retain 11 undefined specification rows, six partial analysis sets and twelve unavailable sets due to insufficient length. Crossings are descriptive, not clinical thresholds.

## What is delivered

- Source code, tests, protocols, frozen-file hashes, results, figures and source/license attribution.
- `enabl3s_cohort_review.ipynb`: an executable review of the saved derived results. It verifies fingerprints, checks counts and regenerates the descriptive report/figure. It does **not** recompute amplitudes from the original participant archives.
- `acl-semg-robustness-v0.2.0.zip`: a source-and-results snapshot; `manifest.json` lists every packaged file and SHA-256; `checksums.txt` identifies the ZIP.

The ZIP omits original measurements, environments, credentials and local caches. ENABL3S original downloads total about 5.9 GB for the nine non-pilot participants. Attribution and separate licenses: [DATA_SOURCES.md](../../DATA_SOURCES.md).

## Review without downloading original measurements

Extract the ZIP, install `requirements.txt` and `requirements-verification.txt` into Python 3.14, then open this notebook from the extracted repository. Run all cells. It searches parent directories for the included results, so it does not require a particular Windows username. The recorded local dependency versions may need a compatible interpreter; printed runtime versions identify the environment actually used.

This notebook and ZIP are suitable for a proposed Kaggle update containing derived artifacts, with ENABL3S attribution and CC BY 4.0 for those artifacts. They have not yet been executed or published on Kaggle. The existing public Dryad notebook remains the first delivery.

## Recompute from original measurements

From the repository root, with dependencies installed:

```powershell
python scripts/fetch_enabl3s_cohort.py
python scripts/analyze_enabl3s_cohort.py
python scripts/report_enabl3s_cohort.py
python -m pytest -q
```

The downloader obtains pinned Figshare v2 metadata if absent; it does not require the pilot download. The analysis rechecks archive SHA-256 and the frozen protocol files. Download size, hashes and exclusions are explicit. Raw reproduction and review of already derived outputs are different checks.
