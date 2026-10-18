"""Export the saved audit results used by the public site (site/assets/data.js).

Reads only derived report tables; no signal is recomputed here. Run after
`python scripts/run_all.py` whenever results change.
"""

import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"
OUT = ROOT / "site/assets/data.js"


def rows(name):
    with open(REPORTS / name, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def flag(value):
    return value.strip().lower() == "true"


def main():
    pairs = []
    for r in rows("robustness_participant_summary.csv"):
        pairs.append(
            {
                "id": f"{r['participant_id']}/{r['condition']}",
                "cohort": r["cohort"],
                "whole": round(float(r["whole_rms_ratio_pct"]) / 100, 4),
                "min": round(float(r["min_ratio_pct"]) / 100, 4),
                "max": round(float(r["max_ratio_pct"]) / 100, 4),
                "crosses": flag(r["direction_changes_across_specifications"]),
                "primary": flag(r["primary_pair"]),
            }
        )
    bandpass = [
        {
            "id": f"{r['participant_id']}/{r['condition']}",
            "exported": round(float(r["exported_whole_rms_ratio"]), 4),
            "filtered": round(float(r["bandpass_whole_rms_ratio"]), 4),
            "changes": flag(r["whole_rms_direction_changes"]),
        }
        for r in rows("bandpass_paired_summary.csv")
        if flag(r["primary_pair"])
    ]
    scenarios, methods, error = [], [], {}
    for r in rows("synthetic_scenario_summary.csv"):
        if r["scenario"] not in scenarios:
            scenarios.append(r["scenario"])
        if r["method"] not in methods:
            methods.append(r["method"])
        error[f"{r['scenario']}|{r['method']}"] = [
            round(float(r["median_absolute_log_error"]), 4),
            round(float(r["direction_mismatch_fraction"]), 3),
        ]
    cohort_path = REPORTS / "enabl3s_cohort_results_v1.json"
    verification = json.loads(
        (REPORTS / "enabl3s_cohort_review_verification_v1.json").read_text(
            encoding="utf-8"
        )
    )
    if (
        hashlib.sha256(cohort_path.read_bytes()).hexdigest()
        != verification["results_sha256"]
    ):
        raise ValueError("Saved ENABL3S result fingerprint mismatch")
    cohort = json.loads(cohort_path.read_text(encoding="utf-8"))
    people = []
    for person in cohort["participants"]:
        if person["status"] != "eligible":
            continue
        analysis = next(a for a in person["analyses"] if a["primary"])
        people.append(
            {
                "id": person["participant"],
                "crosses": analysis["crosses_one"],
                "range": round(analysis["log_ratio_range"], 4),
                "specs": [
                    [s["method"], round(s["ratio"], 4)]
                    for s in analysis["specifications"]
                ],
            }
        )
    primary = [p for p in pairs if p["primary"]]
    data = {
        "source": "reports/ (derived results); ENABL3S results hash verified",
        "pairs": pairs,
        "bandpass": bandpass,
        "synthetic": {"scenarios": scenarios, "methods": methods, "error": error},
        "people": people,
        "summary": {
            "participants": 22,
            "recordings": 88,
            "specifications": 21,
            "primary_pairs": len(primary),
            "primary_crossings": sum(p["crosses"] for p in primary),
            "synthetic_evaluations": len(scenarios) * len(methods) * 100,
            "enabl3s_eligible": len(people),
            "enabl3s_crossings": sum(p["crosses"] for p in people),
        },
    }
    assert data["summary"]["primary_pairs"] == 43
    assert data["summary"]["primary_crossings"] == 13
    assert data["summary"]["synthetic_evaluations"] == 23100
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(
        "window.ACL = " + json.dumps(data, separators=(",", ":")) + ";\n",
        encoding="utf-8",
    )
    print(json.dumps(data["summary"]))


if __name__ == "__main__":
    main()
