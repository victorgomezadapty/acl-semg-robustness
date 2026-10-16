# Kaggle delivery

Published and executed on Kaggle on 2026-10-07. See [PUBLICATION.md](PUBLICATION.md) for the public links, executed version, runtime and evidence. The preparation instructions below also support future rebuilds; rebuilding creates a new unverified bundle.

1. Create a Dataset from acl_semg_input.zip. Title: ACL Reconstruction sEMG — Dryad 2022, Reproducibility Bundle.
   The original ZIP is transported as ACL_data.zip.bin because Kaggle recursively expands ZIP files. The notebook copies identical bytes to ACL_data.zip before hash verification.
2. Attribute Gutierrez, Hart & Boukhechba and link DOI 10.5061/dryad.66t1g1k4j. State that source data are CC0; this upload is a repackaged analysis bundle, not newly collected data. Dataset metadata ownership is not authorship of measurements.
3. This bundle also includes project code and documentation under MIT (see CODE_LICENSE.md). Explain the separate licenses in the dataset description; do not relabel all bundled content CC0.
4. Import acl_semg_robustness.ipynb into a Python Notebook and attach that Dataset.
5. Run all cells on CPU. Verify 88 records, 44 pairs and 924 specification results; inspect the displayed figures. No outputs are fabricated or pre-executed in the supplied notebook.
6. Save an executed version; set Dataset and Notebook visibility deliberately. For public reproducibility the required input must be accessible to readers.
7. Publish as an independent analysis, with no claim of competition ranking, scientific priority or clinical clearance.

The notebook has been prepared and locally verified separately; actual execution/publication on Kaggle is still pending. Original requirements record the local tested versions; the notebook prints Kaggle runtime versions instead of forcing unsupported package pins.
