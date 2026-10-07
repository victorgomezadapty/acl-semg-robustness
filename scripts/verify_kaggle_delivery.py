"""Execute the exact delivered notebook against only its unpacked input bundle."""

import hashlib
import json
import os
import sys
import zipfile
from pathlib import Path

import nbformat
from jupyter_client import KernelManager
from nbclient import NotebookClient

ROOT = Path(__file__).resolve().parents[1]
delivery = ROOT / "delivery/kaggle"
bundle_digest = hashlib.sha256(
    (delivery / "acl_semg_input.zip").read_bytes()
).hexdigest()
verification = delivery / "verification" / bundle_digest
input_root = verification / "input"
output_root = verification / "working"
input_root.mkdir(parents=True, exist_ok=True)
with zipfile.ZipFile(delivery / "acl_semg_input.zip") as archive:
    # All members are generated from workspace-relative paths. Check containment.
    for name in archive.namelist():
        target = (input_root / name).resolve()
        if not target.is_relative_to(input_root.resolve()):
            raise ValueError("Unsafe member")
    archive.extractall(input_root)
os.environ["ACL_INPUT_ROOT"] = str(input_root)
os.environ["ACL_WORKING_ROOT"] = str(output_root)
notebook = nbformat.read(delivery / "acl_semg_robustness.ipynb", as_version=4)
nbformat.validate(notebook)
manager = KernelManager(kernel_name="python3")
manager.kernel_spec.argv = [
    sys.executable,
    "-m",
    "ipykernel_launcher",
    "-f",
    "{connection_file}",
]
try:
    NotebookClient(
        notebook,
        km=manager,
        timeout=900,
        resources={"metadata": {"path": str(ROOT)}},
    ).execute()
finally:
    if manager.has_kernel:
        manager.shutdown_kernel(now=True)
nbformat.write(notebook, delivery / "acl_semg_robustness_executed_local.ipynb")
summary = json.loads((output_root / "reports/robustness_summary.json").read_text())
assert summary["direction_changes"] == 13 and summary["rows"] == 924
centering = json.loads((output_root / "reports/centering_checks.json").read_text())
synthetic = json.loads(
    (output_root / "reports/synthetic_scenario_checks.json").read_text()
)
assert centering["recordings"] == 88 and centering["specification_rows"] == 1848
assert synthetic["evaluations"] == 23100 and synthetic["invariants_passed"]
result = {
    "exact_notebook_executed_locally": True,
    "isolated_bundle": True,
    "verification_python": sys.executable,
    "kaggle_execution_verified": False,
    "summary": summary,
    "centering": centering,
    "synthetic": synthetic,
    "bundle_sha256": hashlib.sha256(
        (delivery / "acl_semg_input.zip").read_bytes()
    ).hexdigest(),
}
(delivery / "local_verification.json").write_text(
    json.dumps(result, indent=2), encoding="utf-8"
)
print(json.dumps(result))
