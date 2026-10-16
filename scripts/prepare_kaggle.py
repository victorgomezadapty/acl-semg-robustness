"""Build a portable, attributed Kaggle input bundle and unexecuted notebook."""

import hashlib
import json
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "delivery/kaggle"
OUT.mkdir(parents=True, exist_ok=True)


def markdown(text):
    return {"cell_type": "markdown", "metadata": {}, "source": text.splitlines(True)}


def code(text):
    return {
        "cell_type": "code",
        "metadata": {},
        "source": text.splitlines(True),
        "outputs": [],
        "execution_count": None,
    }


cells = [
    markdown("""# ACL Rehabilitation: sEMG Asymmetry and Robustness

An independent portfolio study, not a competition submission or clinical clearance tool.
Data: Gutierrez, Hart & Boukhechba (2022), [Dryad DOI](https://doi.org/10.5061/dryad.66t1g1k4j), CC0 per original metadata.
The published secondary analysis uses related standard measures. Our additional contribution is a retrospective specification-sensitivity audit; novelty and clinical validity are not established.

Attach the uploaded input bundle **acl_semg_input.zip** as a Kaggle Dataset. Kaggle recursively expands ZIP files, so original archive bytes travel as ACL_data.zip.bin. This notebook restores the .zip filename before the existing SHA-256 checks. CPU is sufficient; no credentials or internet downloads are required by this notebook.
"""),
    code("""from pathlib import Path
import shutil, sys, subprocess, json, os
from IPython.display import display, Markdown, Image
search_root = Path(os.environ.get('ACL_INPUT_ROOT', '/kaggle/input' if Path('/kaggle/input').exists() else str(Path.cwd())))
candidates = list(search_root.rglob('scripts/evaluate_robustness.py'))
if len(candidates) != 1:
    raise RuntimeError(f'Expected one attached source bundle, found {len(candidates)}. Attach the prepared Kaggle Dataset.')
source_root = candidates[0].parents[1]
working = Path(os.environ.get('ACL_WORKING_ROOT', '/kaggle/working/acl_semg_analysis' if Path('/kaggle/working').exists() else str(Path.cwd()/'kaggle_local_run')))
working.mkdir(parents=True, exist_ok=True)
for folder in ('src','scripts','docs','data','tests'):
    shutil.copytree(source_root/folder, working/folder, dirs_exist_ok=True)
transport_archive = working/'data/raw/ACL_data.zip.bin'
if transport_archive.exists():
    shutil.copyfile(transport_archive, working/'data/raw/ACL_data.zip')
for filename in ('README.md','requirements.txt','requirements-verification.txt','CHANGELOG.md','pytest.ini','ruff.toml'):
    shutil.copy2(source_root/filename, working/filename)
for folder in ('reports/figures/profiles','data/processed'):
    (working/folder).mkdir(parents=True, exist_ok=True)
os.environ.setdefault('MPLCONFIGDIR', str(working/'.mpl-cache'))
import numpy, scipy, matplotlib
print({'Python':sys.version, 'numpy':numpy.__version__, 'scipy':scipy.__version__, 'matplotlib':matplotlib.__version__})
"""),
    markdown("""## Question and data

How dependent are descriptive bilateral sEMG interpretations on amplitude-summary choices? All 22 participants and 88 records are retained. Samples and specifications are not independent people. No torque, IMU or clinical outcomes exist in this export. Labels iso90/iso180 and inv/uninv are retained without inventing control dominance.
"""),
    code("""for script in ('inspect_dataset.py','check_amplitude.py','check_statistics.py','exploratory_amplitude.py','comprehensive_semg.py','evaluate_robustness.py','evaluate_centering.py','evaluate_bandpass.py','simulate_measurement_scenarios.py','build_analysis_report.py'):
    print('Running', script, flush=True)
    subprocess.run([sys.executable, str(working/'scripts'/script)], cwd=working, check=True)
"""),
    markdown("""## Baseline analysis and publication comparison

Whole-record summaries differ from published contraction-based summaries. The short control denominator demonstrably changes our mean; undocumented boundaries and processing are possible explanations for the publication discrepancy, not confirmed causes. No comparison remains below family-specific Holm p=0.05; that is not evidence of equivalence.
"""),
    code("""display(Markdown((working/'docs/review_results.md').read_text(encoding='utf-8')))
for figure in ('rms_V_paired_amplitude.png','extended_balance_distributions.png','block_ratio_sensitivity.png'):
    display(Image(filename=str(working/'reports/figures'/figure)))
"""),
    markdown("""## Additional contribution: interpretation sensitivity

21 explicit specifications: whole RMS, whole MAV, capped RMS and 18 block variants. Sign changes can be arbitrarily small; they are descriptive, not clinically important by definition. Separate RMS-only results help distinguish feature choice from within-RMS summary choice. Synthetic perturbations test mathematical behavior, not physiological validity.
"""),
    code("""display(Markdown((working/'docs/review_methods.md').read_text(encoding='utf-8')))
display(Image(filename=str(working/'reports/figures/robustness_matrix.png')))
print(json.loads((working/'reports/robustness_summary.json').read_text()))
"""),
    markdown("""## Individual signals and downloadable outputs

Profiles retain both limbs and conditions without synchronizing contractions. Control references are descriptive and include the person itself for control profiles. Generated CSVs, profiles and the local HTML viewer remain in the notebook output folder.
"""),
    code("""display(Image(filename=str(working/'reports/figures/profiles/patient12.png')))
for p in sorted((working/'reports').glob('robustness*')):
    print(p)
"""),
    markdown("""## Limits and sources

Retrospective choices were made after seeing the dataset. No independent cohort validation, clinical score, prediction or longitudinal claim is made. Amplitude normalization, contraction boundaries and control dominance remain undocumented. The sensitivity audit adds traceability, not a new validated EMG method.

- [Original data](https://doi.org/10.5061/dryad.66t1g1k4j)
- [Secondary dataset analysis, 2026](https://doi.org/10.25259/JMSR_129_2026)
- [Specification curve analysis, Simonsohn et al. 2020](https://doi.org/10.1038/s41562-020-0912-z): established background for examining analytical choices. This notebook is a descriptive sensitivity audit, not its full inferential procedure.

Next study: independently documented sEMG with participant-level clinical covariates. Cohorts must remain separate.
"""),
]
cells.insert(
    -2,
    markdown("""## Centering and controlled synthetic scenarios

Within-person ratio sensitivity is the primary interpretation. Absolute between-cohort voltage comparisons are supplemental and acquisition-dependent. Centering is a retrospective sensitivity, not proof of instrument artefact. Synthetic references are constructed, not clinical ground truth.
"""),
)
cells.insert(
    -2,
    code("""display(Markdown((working/'docs/history/centering_results.md').read_text(encoding='utf-8')))
display(Markdown((working/'docs/review_limitations.md').read_text(encoding='utf-8')))
for figure in ('centering_ratio_sensitivity.png','synthetic_scenario_matrix.png'):
    display(Image(filename=str(working/'reports/figures'/figure)))
"""),
)
cells.insert(
    3,
    markdown("""## Why these choices were made

The decision record describes choices, reasons, alternatives and checks. Choices remain retrospective. The short-record rule defines 43 primary pairs while all 44 remain available. Clock-derived average rates permit conditional filtering sensitivity, not proof of uniform acquisition. RMS retention is an amplitude comparison, not energy outside a band. Stable group medians can coexist with large individual changes.

The archive includes docs/reproducibility.md with hashes, commands, expected outputs and troubleshooting. This notebook runs offline once its input is attached.
"""),
)
cells.insert(
    4,
    code("""display(Markdown((working/'docs/decision_log.md').read_text(encoding='utf-8')))
"""),
)
cells.insert(
    -1,
    markdown("""## Band-pass sensitivity: individuals and groups

SciPy butter(N=4, bandpass, output='sos') followed by sosfiltfilt gives order 8 per pass and effective forward/backward order 16. RMS retention compares filtered and centered RMS; its square compares mean squares, including transition and edge effects. Review flags are not diagnoses. The report preserves all pairs alongside the primary subset.
"""),
)
cells.insert(
    -1,
    code("""display(Markdown((working/'docs/history/bandpass_results.md').read_text(encoding='utf-8')))
display(Image(filename=str(working/'reports/figures/bandpass_sensitivity.png')))
print(json.loads((working/'reports/bandpass_checks.json').read_text()))
"""),
)
notebook = {
    "cells": cells,
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3",
        },
        "language_info": {"name": "python"},
    },
    "nbformat": 4,
    "nbformat_minor": 5,
}
# Stable cell ids required by notebook format 4.5.
for i, cell in enumerate(cells):
    cell["id"] = f"acl-cell-{i:02d}"
(OUT / "acl_semg_robustness.ipynb").write_text(
    json.dumps(notebook, indent=2), encoding="utf-8"
)
files = []
for folder in ("src", "scripts", "docs", "tests"):
    files.extend(
        p
        for p in (ROOT / folder).rglob("*")
        if p.is_file()
        and "__pycache__" not in p.parts
        and p.suffix in (".py", ".md", ".csv")
    )
files.extend(
    [
        ROOT / "README.md",
        ROOT / "requirements.txt",
        ROOT / "requirements-verification.txt",
        ROOT / "CHANGELOG.md",
        ROOT / "pytest.ini",
        ROOT / "ruff.toml",
        ROOT / "data/raw/ACL_data.zip",
        ROOT / "data/raw/README_acl.txt",
    ]
)
with zipfile.ZipFile(OUT / "acl_semg_input.zip", "w", zipfile.ZIP_DEFLATED) as archive:
    for p in sorted(files):
        archive_name = p.relative_to(ROOT).as_posix()
        if archive_name == "data/raw/ACL_data.zip":
            archive_name += ".bin"
        archive.write(p, archive_name)
manifest = {
    "files": len(files),
    "bundle_sha256": hashlib.sha256(
        (OUT / "acl_semg_input.zip").read_bytes()
    ).hexdigest(),
    "source_doi": "10.5061/dryad.66t1g1k4j",
    "source_archive_transport": "data/raw/ACL_data.zip.bin",
    "kaggle_execution_verified": False,
    "notebook_outputs": False,
}
(OUT / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
(OUT / "UPLOAD_INSTRUCTIONS.md").write_text(
    """# Kaggle delivery

1. Create a Dataset from acl_semg_input.zip. Title: ACL Reconstruction sEMG — Dryad 2022, Reproducibility Bundle.
   The original ZIP is transported as ACL_data.zip.bin because Kaggle recursively expands ZIP files. The notebook copies identical bytes to ACL_data.zip before hash verification.
2. Attribute Gutierrez, Hart & Boukhechba and link DOI 10.5061/dryad.66t1g1k4j. State that source data are CC0; this upload is a repackaged analysis bundle, not newly collected data. Dataset metadata ownership is not authorship of measurements.
3. This bundle also includes project code and documentation under MIT (see CODE_LICENSE.md). Explain the separate licenses in the dataset description; do not relabel all bundled content CC0.
4. Import acl_semg_robustness.ipynb into a Python Notebook and attach that Dataset.
5. Run all cells on CPU. Verify 88 records, 44 pairs and 924 specification results; inspect the displayed figures. No outputs are fabricated or pre-executed in the supplied notebook.
6. Save an executed version; set Dataset and Notebook visibility deliberately. For public reproducibility the required input must be accessible to readers.
7. Publish as an independent analysis, with no claim of competition ranking, scientific priority or clinical clearance.

The notebook has been prepared and locally verified separately; actual execution/publication on Kaggle is still pending. Original requirements record the local tested versions; the notebook prints Kaggle runtime versions instead of forcing unsupported package pins.
""",
    encoding="utf-8",
)
print(json.dumps(manifest))
