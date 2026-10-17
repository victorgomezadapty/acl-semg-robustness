# ENABL3S Kaggle extension — 2026-10-17

Dataset: [ENABL3S sEMG - Reproducible Methods Audit](https://www.kaggle.com/datasets/vctorandrsgmezlpez/enabl3s-semg-reproducible-methods-audit).

Notebook: [ENABL3S sEMG: Independent Methods Audit](https://www.kaggle.com/code/vctorandrsgmezlpez/enabl3s-semg-independent-methods-audit). Verified execution: [version 2, scriptVersionId 359285448](https://www.kaggle.com/code/vctorandrsgmezlpez/enabl3s-semg-independent-methods-audit?scriptVersionId=359285448).

Both artifacts are public. Kaggle confirmed publication of the dataset and saving of notebook sharing settings; the notebook Share button shows the public globe. Evidence: `kaggle_execution.jpg` and the actual downloaded `kaggle_execution_logs.txt`.

## Observed execution

Kaggle reported a successful 24.8-second CPU run of version 2, using Python 3.13.15. The displayed outputs verify derived-result and frozen-protocol hashes and retain nine assessed participants, six eligible, three excluded, eleven primary RMS specifications and two crossings of ratio 1. The report and figure were regenerated and displayed. This notebook reviews saved derived results; it does not recalculate original participant amplitudes or establish clinical validity.

Version 1 was imported using Quick Save before attaching the dataset; its successful status is not evidence of executing the analysis cells. Version 2 uses the attached ENABL3S dataset and actually executed the review cells.

## Source and publication decisions

The direct local ZIP upload remained pending and did not create a dataset. A remote-release URL attempt was rewritten by Kaggle to an invalid raw GitHub URL and failed. Those attempts were abandoned; the successful dataset uses Kaggle's **Import GitHub repository** option for `victorgomezadapty/acl-semg-robustness`, whose main branch was at `b5e8269` at import. Kaggle dataset version 1 contains 201 files, 11.57 MB; it is a repository snapshot, not the 186-file GitHub release ZIP. The published numeric results and frozen-file fingerprints match the intended artifacts.

Dataset description names Hu, Rouse and Hargrove, links [ENABL3S v2](https://doi.org/10.6084/m9.figshare.5362627.v2) and its [methods](https://doi.org/10.3389/frobt.2018.00014), states CC BY 4.0 for ENABL3S-derived artifacts and MIT for original project code/prose, and credits the prior Dryad source separately. License metadata is **Other (specified in description)** to preserve these component distinctions. Original participant archives are absent. The source snapshot includes prior Dryad outputs for context, but the cohorts are not pooled.

Kaggle's public-notebook dialog labels the original notebook wrapper Apache 2.0. This publication does not relicense the ENABL3S source or derived artifacts: their CC BY 4.0 attribution remains explicit, and bundled MIT code retains its notices. The distinction follows the existing Dryad notebook publication practice.

Regenerated review files are created in the notebook's temporary directory; they are displayed in the notebook but not retained as downloadable `/kaggle/working` outputs. Source results, tables and code are downloadable from the attached dataset and GitHub release. The first Dryad Kaggle delivery remains separate and public.

For the next scientific study, see the [clinical-validation roadmap](../../docs/clinical_validation_roadmap.md): synchronized sEMG/torque, repeat sessions, independent clinical measures and appropriate follow-up are required to address physiological and clinical validity.
