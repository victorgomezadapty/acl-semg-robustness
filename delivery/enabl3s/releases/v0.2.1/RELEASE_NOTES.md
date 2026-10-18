# v0.2.1 — Portable delivery, critical literature review and portfolio

2026-10-18. This delivery improves presentation and reproducibility; scientific endpoints and the frozen v1 protocol are unchanged.

- Export a downloadable derived-evidence ZIP under `/kaggle/working`; use absolute links in the displayed report.
- Require a new version and empty output directory. Preserve v0.2.0 publication evidence and record the actual UTC preparation date.
- Verify exact packaged SHA-256, with explicitly listed CRLF/LF equivalence for nonfrozen UTF-8 files imported from GitHub. Frozen protocol and ENABL3S JSON still require exact bytes.
- Add a targeted critical review of twelve sources, search/evidence logs and a research roadmap. OSF HV6X2 is a candidate awaiting file/license audit; previously inspected 101-point ACLR exports remain ineligible for the existing windows.
- Add a responsive static portfolio with original figures, six-person method exploration and downloadable documentation. Source: `portfolio/dist/`; rebuild data with `python scripts/build_portfolio.py`.

Local checks: 27 tests passed; Ruff lint/format and JavaScript syntax passed; 209 package files checked; derived-review notebook executed using Python 3.14.6. The Git transport fingerprint check accepts only recorded content/line-ending equivalents. A separate record will identify actual Kaggle execution; this local evidence does not certify it.

Source/results ZIP SHA-256: `13eae64a31b659c26f43786a526f61a3e2b76675ab984fa0d2667fe4a296178e`.

The notebook reviews saved derived outputs and regenerates their report. It does not rerun original EMG amplitude calculations. Raw reproduction requires the separate verified archives and analysis scripts. There are no new patient data or clinical-utility claims. Code/original prose: MIT; ENABL3S-derived artifacts: CC BY 4.0, with source attribution in DATA_SOURCES.md. Literature retains separate rights; third-party article figures and questionnaires are not included.

Actual Kaggle execution subsequently verified: [notebook version 4](https://www.kaggle.com/code/vctorandrsgmezlpez/enabl3s-semg-independent-methods-audit?scriptVersionId=359679003), Save & Run All successful in 28.0 seconds using dataset v2. Published Output contains `enabl3s-review-artifacts.zip` (108,061 bytes), report evidence and the source copy. [Publication record](https://github.com/victorgomezadapty/acl-semg-robustness/blob/main/delivery/enabl3s/releases/v0.2.1/PUBLICATION.md) separates the stalled/cancelled v3 attempt from the successful v4. The output ZIP was visible with a download control; the browser download helper timed out, so a downloaded-output checksum is not claimed.
