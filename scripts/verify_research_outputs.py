"""Independent provenance and eligibility checks; no source workbook mutation."""

import csv
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
checks = {}
for ident in ("30928694", "22139915"):
    folder = ROOT / f"data/external/figshare_{ident}"
    manifest = json.loads((folder / "download_manifest.json").read_text())
    for r in manifest:
        blob = (folder / r["name"]).read_bytes()
        assert hashlib.md5(blob).hexdigest() == r["md5"]
        assert hashlib.sha256(blob).hexdigest() == r["sha256"]
        assert len(blob) == r["bytes"]
    checks[f"figshare_{ident}_verified_files"] = len(manifest)
audit = json.loads(
    (ROOT / "reports/external_cohort_audit.json").read_text(encoding="utf-8")
)
emg = [f for f in audit if "EMG data from 17" in f["file"]]
assert len(emg) == 2
for f in emg:
    assert len(f["sheets"]) == 17
    assert {s["name"] for s in f["sheets"]} == {str(i) for i in range(1, 18)}
    assert all(
        s["rows"] == 102 and s["columns"] == 9 and s["nonfinite"] == 0
        for s in f["sheets"]
    )
    assert all("VL" in s["top_rows"][0] for s in f["sheets"])
basic = next(f for f in audit if f["file"].startswith("Basic"))
assert not any(
    "acl-rsi" in str(t["text"]).lower()
    for s in basic["sheets"]
    for t in s["text_labels"]
)
checks["exported_points_per_EMG_channel"] = 101
checks["external_direct_validation_eligible"] = False
with (ROOT / "reports/novelty_screening.csv").open(encoding="utf-8") as f:
    records = list(csv.DictReader(f))
assert len(records) == len({r["pmid"] for r in records}) == 44
checks["unique_pubmed_records"] = 44
bad = []
for name in (
    "picott_research_protocol.md",
    "scientific_novelty_review.md",
    "external_validation_feasibility.md",
    "data_request_draft.md",
):
    p = ROOT / "docs/history" / name
    for link in re.findall(r"\]\(([^)]+)\)", p.read_text(encoding="utf-8")):
        if (
            not link.startswith(("https:", "http:"))
            and not (p.parent / link).resolve().exists()
        ):
            bad.append((name, link))
assert not bad, bad
checks["local_research_links_valid"] = True
checks["clinical_validation_completed"] = False
checks["scientific_priority_established"] = False
(ROOT / "reports/research_quality_checks.json").write_text(
    json.dumps(checks, indent=2), encoding="utf-8"
)
print(json.dumps(checks))
