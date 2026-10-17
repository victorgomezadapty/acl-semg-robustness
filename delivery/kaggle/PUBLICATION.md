# Kaggle publication: 2026-10-07

Both artifacts are public in the owner's Kaggle account:

- [Notebook: ACL sEMG: Robustness and Synthetic Scenarios](https://www.kaggle.com/code/vctorandrsgmezlpez/acl-semg-robustness-and-synthetic-scenarios)
- [Dataset: ACL sEMG Dryad 2022 - Reproducibility Bundle](https://www.kaggle.com/datasets/vctorandrsgmezlpez/acl-semg-dryad-2022-reproducibility-bundle)
- [Executed notebook version 356098386](https://www.kaggle.com/code/vctorandrsgmezlpez/acl-semg-robustness-and-synthetic-scenarios?scriptVersionId=356098386)

Kaggle reported **Successfully ran in 111.9s**, CPU, 32.97 MB of output. Runtime: Python 3.13.15, NumPy 2.1.3, SciPy 1.16.3, Matplotlib 3.10.0. The public notebook contains figures, methods, decision explanations and citations; its output contains the reproducible reports and local HTML viewer.

Observed logs verify both original file hashes, 88 records, 44 pairs, 43 primary pairs, 924 baseline specification results, 13 direction changes (10 RMS only), 1,848 centering/filtering rows per analysis, filtering crossings 10 to 8, and 23,100 synthetic evaluations with invariants passed. These match the local checks; floating-point rounding differences across environments are expected. This is actual Kaggle execution, separate from local notebook verification.

Evidence: `kaggle_execution_logs.txt` and `kaggle_execution.jpg`. Dataset version **2**, 72 files. Bundle SHA-256: `e26e10f3e7964b0e4eaba910ebe72e634e4a34132b677aaf5b9ae5504788bb94`.

## Publication decisions

The first private upload revealed that Kaggle expands nested ZIP files. Version 2 transports original ZIP bytes under `.zip.bin`. The notebook copies these identical bytes to the expected `.zip` filename, preserving the original SHA-256 verification. The first private notebook import ran before its data attachment; the completed public version above uses dataset version 2. No measurements were changed to accommodate Kaggle.

Dataset license metadata is **Other (specified in description)** because its original measurements are CC0 and project code/docs are MIT. The Kaggle public-notebook dialog labels the notebook **Apache 2.0**; this applies to the original notebook wrapper published there. Bundled MIT code/docs keep their notices and original CC0 data remain CC0. The dataset's description explicitly credits Gutierrez, Hart and Boukhechba and links the Dryad DOI. Kaggle ownership is not authorship of the original measurements.

The package is an independent methodological analysis, not a competition submission. No clinical validity, independent cohort validation or scientific priority is claimed. Public execution demonstrates reproducibility in the recorded Kaggle environment, not clinical usefulness.
