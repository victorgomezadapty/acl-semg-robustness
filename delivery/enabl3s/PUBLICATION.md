# GitHub publication — v0.2.0

2026-10-16. Published [release v0.2.0](https://github.com/victorgomezadapty/acl-semg-robustness/releases/tag/v0.2.0) in [victorgomezadapty/acl-semg-robustness](https://github.com/victorgomezadapty/acl-semg-robustness). GitHub API confirms draft=false, prerelease=false and all six assets uploaded.

Release target: `f8515ba76fa4811cc2fedb70d93f1be18f66c289`. The main branch was updated by fast-forward from `35111669bf3e101da7b491c00f6d8736c842d3c5`; no remote history was rewritten. This publication receipt is a later documentation update and does not change the release snapshot.

## Downloadable artifacts

- `acl-semg-robustness-v0.2.0.zip`: 9,320,768 bytes, source and derived-results snapshot, 186 file fingerprints checked after extraction.
- `enabl3s_cohort_review.ipynb`: executable source notebook.
- `enabl3s_cohort_review_executed.ipynb`: actual local execution output.
- `manifest.json`, `checksums.txt`, `verification.json`: file inventory, ZIP fingerprint and execution record.

ZIP SHA-256, independently reported by GitHub and matched to the local verification:

```text
6022b205f3ecc7debca4d0ac5f1b815fa31c349496e49213933ce4b693442c82
```

## Verification and scope

27 tests passed, Ruff checks and formatting passed. The notebook ran on Python 3.14.6 against the extracted package and regenerated the derived-results report and figure. The first restricted run could not start its kernel; it was stopped and the successful local verification was run outside that restricted environment. No result values were changed to complete packaging.

The notebook verifies saved derived artifacts and the protocol hashes; it does not recompute original participant EMG. The raw-data analysis was completed separately and retains its provenance, six eligible participants, three exclusions, partial sensitivities and undefined cases. This delivery establishes an inspectable methodological extension, not clinical usefulness or scientific priority.

Original measurements are excluded from this GitHub package. [Attribution and licenses](../../DATA_SOURCES.md) distinguish ENABL3S-derived artifacts (CC BY 4.0) from original code/prose (MIT). The existing Dryad Kaggle release remains public; this ENABL3S notebook has not yet been published or executed on Kaggle.
