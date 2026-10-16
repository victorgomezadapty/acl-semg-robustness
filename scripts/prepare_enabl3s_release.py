"""Build and execute a portable derived-results review delivery."""

import hashlib
import json
import platform
import subprocess
import sys
import zipfile
from pathlib import Path

import nbformat
from jupyter_client import KernelManager
from nbclient import NotebookClient

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "delivery/enabl3s"


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    nb = nbformat.v4.new_notebook(
        cells=[
            nbformat.v4.new_markdown_cell("""# ENABL3S: independent methodological audit

Nine non-pilot healthy participants, six eligible under fixed rules, three excluded. This notebook reviews **saved derived results** and regenerates their report. It does not recompute original EMG amplitudes. Full raw reproduction requires the separate downloader and analysis (about 5.9 GB).

Source: Hu, Rouse & Hargrove, [ENABL3S v2](https://doi.org/10.6084/m9.figshare.5362627.v2), CC BY 4.0. Original project code/prose: MIT. Derived ENABL3S artifacts: CC BY 4.0; see DATA_SOURCES.md. No clinical validity or scientific-priority claim is made."""),
            nbformat.v4.new_code_cell("""from pathlib import Path
import hashlib, json, subprocess, sys
from IPython.display import display, Markdown, Image
roots = [Path.cwd(), *Path.cwd().parents]
if Path('/kaggle/input').exists():
    roots += [p.parents[1] for p in Path('/kaggle/input').rglob('reports/enabl3s_cohort_results_v1.json')]
root = next((p for p in roots if (p/'reports/enabl3s_cohort_results_v1.json').exists() and (p/'scripts/report_enabl3s_cohort.py').exists()), None)
if root is None:
    raise RuntimeError('Extract and attach the full source-and-results bundle; the notebook alone is insufficient.')
print('Python:', sys.version)
results_path = root/'reports/enabl3s_cohort_results_v1.json'
review = json.loads((root/'reports/enabl3s_cohort_review_verification_v1.json').read_text(encoding='utf-8'))
assert hashlib.sha256(results_path.read_bytes()).hexdigest() == review['results_sha256']
freeze = json.loads((root/'reports/enabl3s_cohort_protocol_freeze_v1.json').read_text(encoding='utf-8'))
for name, expected in freeze['files'].items():
    assert hashlib.sha256((root/name).read_bytes()).hexdigest() == expected, name
data = json.loads(results_path.read_text(encoding='utf-8'))
assert data['summary']['participants_expected'] == 9
assert data['summary']['complete_primary'] == 6
assert data['summary']['excluded'] == 3
assert data['summary']['primary_crossings_of_one'] == 2
print(data['summary'])
print('Derived-artifact hashes checked; original participant archives were not re-read.')"""),
            nbformat.v4.new_markdown_cell("""## Regenerate the descriptive report

On Kaggle, copy the attached bundle to the writable working directory before regenerating. The source bundle remains untouched. Shared selections with no common blocks remain undefined. Alternative margins use the same original segment."""),
            nbformat.v4.new_code_cell("""import shutil, tempfile
working = Path(tempfile.mkdtemp(prefix='enabl3s-review-'))/'source'
working.mkdir(parents=True)
package_manifest = json.loads((root/'delivery/enabl3s/manifest.json').read_text(encoding='utf-8'))
for name in package_manifest['files']:
    relative = Path(name)
    if relative.is_absolute() or '..' in relative.parts:
        raise RuntimeError('Unsafe packaged path')
    destination = working/relative
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(root/relative, destination)
subprocess.run([sys.executable, str(working/'scripts/report_enabl3s_cohort.py')], cwd=working, check=True)
display(Markdown((working/'docs/enabl3s_cohort_results_v1.md').read_text(encoding='utf-8')))
display(Image(filename=str(working/'reports/figures/enabl3s_cohort_primary_v1.png')))
print('Regenerated review:', working)
"""),
            nbformat.v4.new_markdown_cell("""## Recompute from original measurements

From the repository root with dependencies installed, run `python scripts/fetch_enabl3s_cohort.py`, `python scripts/analyze_enabl3s_cohort.py`, then `python scripts/report_enabl3s_cohort.py`. The downloader fetches pinned v2 metadata if absent, verifies each ZIP and records SHA-256. The analysis verifies the frozen protocol before reading signals.

This is methodological transport to healthy walking, not clinical validation in ACL reconstruction. A crossing of ratio 1 may be arbitrarily small. The six eligible participants are a selected subset; blocks and methods are not independent people. The existing Dryad Kaggle release and this extension have separate execution records."""),
        ]
    )
    nb.metadata.kernelspec = {
        "name": "python3",
        "display_name": "Python 3",
        "language": "python",
    }
    for index, cell in enumerate(nb.cells):
        cell.id = f"enabl3s-{index:02d}"
    notebook_path = OUT / "enabl3s_cohort_review.ipynb"
    nbformat.write(nb, notebook_path)
    listing = (
        subprocess.check_output(
            ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
            cwd=ROOT,
        )
        .decode()
        .split("\0")
    )
    base = {
        "README.md",
        "DATA_SOURCES.md",
        ".gitattributes",
        ".gitignore",
        "requirements.txt",
        "requirements-verification.txt",
        "pytest.ini",
        "ruff.toml",
        "CHANGELOG.md",
    }
    files = sorted(
        {
            name
            for name in listing
            if name
            and (
                name in base
                or name.split("/")[0]
                in {"src", "scripts", "tests", "docs", "config", "reports"}
                or name
                in {
                    "delivery/enabl3s/README.md",
                    "delivery/enabl3s/RELEASE_NOTES.md",
                    "delivery/enabl3s/enabl3s_cohort_review.ipynb",
                    "delivery/kaggle/PUBLICATION.md",
                }
            )
            and (ROOT / name).is_file()
        }
    )
    manifest = {
        "version": "v0.2.0",
        "prepared_on": "2026-10-16",
        "original_measurements_included": False,
        "files": {
            name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
            for name in files
        },
    }
    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    bundle = OUT / "acl-semg-robustness-v0.2.0.zip"
    print("Building source/results ZIP", flush=True)
    with zipfile.ZipFile(bundle, "w", zipfile.ZIP_DEFLATED) as archive:
        for name in files:
            archive.write(ROOT / name, name)
        archive.write(OUT / "manifest.json", "delivery/enabl3s/manifest.json")
    digest = hashlib.sha256(bundle.read_bytes()).hexdigest()
    (OUT / "checksums.txt").write_text(f"{digest}  {bundle.name}\n", encoding="utf-8")
    extracted = OUT / "verification/source"
    extracted.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(bundle) as archive:
        archive.extractall(extracted)
    for name, expected in manifest["files"].items():
        if hashlib.sha256((extracted / name).read_bytes()).hexdigest() != expected:
            raise ValueError(f"Packaged hash mismatch: {name}")
    print(f"Verified {len(files)} packaged files; starting notebook kernel", flush=True)
    kernel = KernelManager(kernel_name="python3")
    kernel.kernel_spec.argv = [
        sys.executable,
        "-m",
        "ipykernel_launcher",
        "-f",
        "{connection_file}",
    ]
    client = NotebookClient(
        nb, km=kernel, timeout=180, resources={"metadata": {"path": str(extracted)}}
    )
    executed = client.execute()
    nbformat.write(executed, OUT / "enabl3s_cohort_review_executed.ipynb")
    verification = {
        "verified_on": "2026-10-16",
        "bundle_sha256": digest,
        "packaged_files_verified": len(files),
        "derived_review_notebook_executed_locally": True,
        "original_signal_analysis_rerun_by_notebook": False,
        "kaggle_extension_published": False,
        "python": platform.python_version(),
    }
    (OUT / "verification.json").write_text(
        json.dumps(verification, indent=2), encoding="utf-8"
    )
    print(json.dumps(verification, indent=2))


if __name__ == "__main__":
    main()
