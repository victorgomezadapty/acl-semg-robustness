"""Build and execute a portable derived-results review delivery."""

import argparse
import hashlib
import json
import platform
import re
import subprocess
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

import nbformat
from jupyter_client import KernelManager
from nbclient import NotebookClient

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", required=True, help="New release, e.g. v0.2.1")
    parser.add_argument("--output", type=Path, help="New, empty output directory")
    args = parser.parse_args()
    if not re.fullmatch(r"v\d+\.\d+\.\d+", args.version):
        parser.error("--version must have the form vMAJOR.MINOR.PATCH")
    out = args.output or ROOT / "delivery/enabl3s/releases" / args.version
    if out.exists() and any(out.iterdir()):
        parser.error(f"Refusing to overwrite an existing delivery: {out}")
    out.mkdir(parents=True, exist_ok=True)
    prepared_on = datetime.now(timezone.utc).date().isoformat()
    nb = nbformat.v4.new_notebook(
        cells=[
            nbformat.v4.new_markdown_cell("""# ENABL3S: independent methodological audit

Nine non-pilot healthy participants, six eligible under fixed rules, three excluded. This notebook reviews **saved derived results** and regenerates their report. It does not recompute original EMG amplitudes. Full raw reproduction requires the separate downloader and analysis (about 5.9 GB).

Source: Hu, Rouse & Hargrove, [ENABL3S v2](https://doi.org/10.6084/m9.figshare.5362627.v2), CC BY 4.0. Original project code/prose: MIT. Derived ENABL3S artifacts: CC BY 4.0; see DATA_SOURCES.md. No clinical validity or scientific-priority claim is made."""),
            nbformat.v4.new_code_cell("""from pathlib import Path
import hashlib, json, subprocess, sys
from IPython.display import display, Markdown, Image, FileLink
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
            nbformat.v4.new_code_cell(
                r"""import shutil, tempfile, re
base = Path('/kaggle/working') if Path('/kaggle/working').is_dir() else Path(tempfile.mkdtemp(prefix='enabl3s-review-'))
working = Path(tempfile.mkdtemp(prefix='source-', dir=base))
manifest_paths = [root/'delivery/enabl3s/releases/RELEASE_VERSION/manifest.json', root/'delivery/enabl3s/manifest.json']
manifest_path = next(p for p in manifest_paths if p.is_file())
package_manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
for name in package_manifest['files']:
    relative = Path(name)
    if relative.is_absolute() or '..' in relative.parts:
        raise RuntimeError('Unsafe packaged path')
    destination = working/relative
    destination.parent.mkdir(parents=True, exist_ok=True)
    source = manifest_path.parent/'enabl3s_cohort_review.ipynb' if name == 'delivery/enabl3s/enabl3s_cohort_review.ipynb' else root/relative
    content = source.read_bytes()
    if hashlib.sha256(content).hexdigest() != package_manifest['files'][name]:
        normalized_expected = package_manifest.get('nonfrozen_utf8_lf_sha256', {}).get(name)
        if normalized_expected is None or hashlib.sha256(content.replace(b'\r\n', b'\n')).hexdigest() != normalized_expected:
            raise RuntimeError(f'Packaged hash mismatch: {name}')
    shutil.copy2(source, destination)
subprocess.run([sys.executable, str(working/'scripts/report_enabl3s_cohort.py')], cwd=working, check=True)
report = (working/'docs/enabl3s_cohort_results_v1.md').read_text(encoding='utf-8')
from urllib.parse import urljoin
source_docs = 'https://github.com/victorgomezadapty/acl-semg-robustness/blob/main/docs/'
report = re.sub(r'\]\(([^)]+)\)', lambda m: ']('+urljoin(source_docs, m.group(1))+')', report)
display(Markdown(report))
display(Image(filename=str(working/'reports/figures/enabl3s_cohort_primary_v1.png')))
exports = base/'enabl3s-review-artifacts'
exports.mkdir(exist_ok=True)
for name in ['docs/enabl3s_cohort_results_v1.md', 'docs/enabl3s_cohort_protocol_v1.md',
             'reports/enabl3s_cohort_results_v1.json', 'reports/enabl3s_cohort_primary_v1.csv',
             'reports/enabl3s_cohort_sensitivity_summary_v1.json', 'reports/enabl3s_cohort_download_manifest.json',
             'reports/enabl3s_cohort_protocol_freeze_v1.json', 'reports/enabl3s_cohort_review_verification_v1.json',
             'reports/figures/enabl3s_cohort_primary_v1.png', 'DATA_SOURCES.md', 'docs/CODE_LICENSE.md']:
    destination = exports/name
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(working/name, destination)
archive = Path(shutil.make_archive(str(base/'enabl3s-review-artifacts'), 'zip', exports))
print('Downloadable derived artifacts:', archive, archive.stat().st_size, 'bytes')
if base == Path('/kaggle/working'):
    display(FileLink('enabl3s-review-artifacts.zip'))
print('Regenerated review:', working)
""".replace("RELEASE_VERSION", args.version)
            ),
            nbformat.v4.new_markdown_cell("""## Recompute from original measurements

From the repository root with dependencies installed, run `python scripts/fetch_enabl3s_cohort.py`, `python scripts/analyze_enabl3s_cohort.py`, then `python scripts/report_enabl3s_cohort.py`. The downloader fetches pinned v2 metadata if absent, verifies each ZIP and records SHA-256. The analysis verifies the frozen protocol before reading signals.

This is methodological transport to healthy walking, not clinical validation in ACL reconstruction. A crossing of ratio 1 may be arbitrarily small. The six eligible participants are a selected subset; blocks and methods are not independent people. The existing Dryad Kaggle release and this extension have separate execution records."""),
            nbformat.v4.new_markdown_cell("""## Literature, decisions and next research

The [critical literature update](https://github.com/victorgomezadapty/acl-semg-robustness/blob/main/docs/literature_update_2026-10-18.md) records twelve selected primary sources, access limitations and a search/evidence matrix. This is a targeted review, not an exhaustive systematic review or proof of scientific novelty.

[CEDE-Check (2024)](https://doi.org/10.1016/j.jelekin.2024.102874) informs reporting; [CEDE force estimation (2024)](https://doi.org/10.1016/j.jelekin.2024.102910) explains why electrical amplitude cannot simply be called muscle force. [Cobian et al. (2024)](https://doi.org/10.1177/23259671241253843) provides a design precedent with measured torque and repeated visits, using different endpoints. [Sherman et al. (2025)](https://doi.org/10.1152/japplphysiol.00641.2024) links a public OSF project for motor-unit/EEG data; its files, license and suitability for our bilateral amplitude question remain to be audited.

Our [decision log](https://github.com/victorgomezadapty/acl-semg-robustness/blob/main/docs/decision_log.md) explains choices and alternatives. The [clinical research roadmap](https://github.com/victorgomezadapty/acl-semg-robustness/blob/main/docs/clinical_validation_roadmap.md) distinguishes measurement validity, repeatability and clinical usefulness. No new patient measurements or clinical outcomes were analyzed in this delivery. Figures are generated from our analyses; literature figures and questionnaires are not redistributed."""),
        ]
    )
    nb.metadata.kernelspec = {
        "name": "python3",
        "display_name": "Python 3",
        "language": "python",
    }
    for index, cell in enumerate(nb.cells):
        cell.id = f"enabl3s-{index:02d}"
    notebook_path = out / "enabl3s_cohort_review.ipynb"
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
                or name.startswith("portfolio/dist/")
                or name == "portfolio/README.md"
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
        "version": args.version,
        "prepared_on": prepared_on,
        "original_measurements_included": False,
        "files": {
            name: hashlib.sha256(
                (
                    notebook_path
                    if name == "delivery/enabl3s/enabl3s_cohort_review.ipynb"
                    else ROOT / name
                ).read_bytes()
            ).hexdigest()
            for name in files
        },
    }
    # GitHub imports can normalize line endings. Frozen files and ENABL3S JSON
    # provenance retain exact byte checks; other UTF-8 files may differ only in CRLF.
    freeze = json.loads(
        (ROOT / "reports/enabl3s_cohort_protocol_freeze_v1.json").read_text(
            encoding="utf-8"
        )
    )
    normalized = {}
    for name in files:
        if name in freeze["files"] or (
            name.startswith("reports/enabl3s") and name.endswith(".json")
        ):
            continue
        content = (
            notebook_path
            if name == "delivery/enabl3s/enabl3s_cohort_review.ipynb"
            else ROOT / name
        ).read_bytes()
        try:
            content.decode("utf-8")
        except UnicodeDecodeError:
            continue
        normalized[name] = hashlib.sha256(content.replace(b"\r\n", b"\n")).hexdigest()
    manifest["nonfrozen_utf8_lf_sha256"] = normalized
    manifest["transport_policy"] = (
        "Exact file SHA-256; optional CRLF-to-LF equivalence only for listed nonfrozen UTF-8 files. Frozen protocol and ENABL3S JSON require exact bytes."
    )
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    bundle = out / f"acl-semg-robustness-{args.version}.zip"
    print("Building source/results ZIP", flush=True)
    with zipfile.ZipFile(bundle, "w", zipfile.ZIP_DEFLATED) as archive:
        for name in files:
            archive.write(
                notebook_path
                if name == "delivery/enabl3s/enabl3s_cohort_review.ipynb"
                else ROOT / name,
                name,
            )
        archive.write(out / "manifest.json", "delivery/enabl3s/manifest.json")
    digest = hashlib.sha256(bundle.read_bytes()).hexdigest()
    (out / "checksums.txt").write_text(f"{digest}  {bundle.name}\n", encoding="utf-8")
    extracted = out / "verification/source"
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
    nbformat.write(executed, out / "enabl3s_cohort_review_executed.ipynb")
    verification = {
        "verified_on": prepared_on,
        "bundle_sha256": digest,
        "packaged_files_verified": len(files),
        "derived_review_notebook_executed_locally": True,
        "original_signal_analysis_rerun_by_notebook": False,
        "kaggle_execution_status": "not_verified_for_this_new_bundle",
        "python": platform.python_version(),
    }
    (out / "verification.json").write_text(
        json.dumps(verification, indent=2), encoding="utf-8"
    )
    print(json.dumps(verification, indent=2))


if __name__ == "__main__":
    main()
