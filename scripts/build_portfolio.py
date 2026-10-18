"""Build static portfolio data and original figures from saved audit results."""

import csv
import hashlib
import json
import os
import shutil
from pathlib import Path

os.environ.setdefault(
    "MPLCONFIGDIR", str(Path(__file__).resolve().parents[1] / ".mpl-cache")
)
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "portfolio/dist"


def main():
    assets = OUT / "assets"
    assets.mkdir(parents=True, exist_ok=True)
    cohort_path = ROOT / "reports/enabl3s_cohort_results_v1.json"
    cohort = json.loads(cohort_path.read_text(encoding="utf-8"))
    freeze = json.loads(
        (ROOT / "reports/enabl3s_cohort_protocol_freeze_v1.json").read_text(
            encoding="utf-8"
        )
    )
    for name, expected in freeze["files"].items():
        if hashlib.sha256((ROOT / name).read_bytes()).hexdigest() != expected:
            raise ValueError(f"Frozen protocol mismatch: {name}")
    verification = json.loads(
        (ROOT / "reports/enabl3s_cohort_review_verification_v1.json").read_text(
            encoding="utf-8"
        )
    )
    if (
        hashlib.sha256(cohort_path.read_bytes()).hexdigest()
        != verification["results_sha256"]
    ):
        raise ValueError("Saved result fingerprint mismatch")
    people = []
    for person in cohort["participants"]:
        if person["status"] != "eligible":
            continue
        analysis = next(a for a in person["analyses"] if a["primary"])
        people.append(
            {
                "id": person["participant"],
                "seconds": analysis["samples"] / 1000,
                "crosses": analysis["crosses_one"],
                "range": analysis["log_ratio_range"],
                "specifications": [
                    {"method": s["method"], "ratio": s["ratio"]}
                    for s in analysis["specifications"]
                ],
            }
        )
    dryad = json.loads((ROOT / "reports/robustness_summary.json").read_text())
    with (ROOT / "docs/literature_evidence_2026-10-18.csv").open(
        encoding="utf-8", newline=""
    ) as f:
        literature = list(csv.DictReader(f))
    payload = {
        "updated": "2026-10-18",
        "source_sha256": hashlib.sha256(cohort_path.read_bytes()).hexdigest(),
        "summary": cohort["summary"],
        "dryad": dryad,
        "people": people,
        "literature": literature,
    }
    (OUT / "data.js").write_text(
        "window.ACL_DATA = "
        + json.dumps(payload, ensure_ascii=False, indent=2)
        + ";\n",
        encoding="utf-8",
    )
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 11,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.spines.left": False,
            "axes.facecolor": "#f6f5ef",
            "figure.facecolor": "#f6f5ef",
            "text.color": "#182e2a",
            "axes.labelcolor": "#182e2a",
            "xtick.color": "#4b605a",
            "ytick.color": "#182e2a",
            "svg.fonttype": "none",
        }
    )
    fig, ax = plt.subplots(figsize=(7.2, 4.2), layout="constrained")
    for i, p in enumerate(people):
        ratios = [s["ratio"] for s in p["specifications"]]
        color = "#a35437" if p["crosses"] else "#126a57"
        ax.plot([min(ratios), max(ratios)], [i, i], color=color, lw=3, alpha=0.45)
        ax.scatter(
            ratios, np.full(len(ratios), i), s=32, color=color, alpha=0.7, zorder=3
        )
        ax.scatter(
            [ratios[0]],
            [i],
            s=90,
            facecolors="none",
            edgecolors="#182e2a",
            lw=1.5,
            zorder=4,
        )
    ax.axvline(1, ls="--", color="#788780", lw=1)
    ax.set(
        yticks=range(len(people)),
        yticklabels=[p["id"] for p in people],
        xlabel="Razón RMS derecha / izquierda",
    )
    ax.invert_yaxis()
    ax.grid(axis="x", alpha=0.13)
    ax.tick_params(axis="y", length=0, pad=12)
    fig.savefig(assets / "enabl3s-ranges.svg")
    fig.savefig(assets / "enabl3s-ranges.png", dpi=180)
    plt.close(fig)
    for name in [
        "robustness_matrix.png",
        "bandpass_sensitivity.png",
        "synthetic_scenario_matrix.png",
        "enabl3s_cohort_primary_v1.png",
    ]:
        shutil.copy2(ROOT / "reports/figures" / name, assets / name)
    for source in [
        "docs/literature_update_2026-10-18.md",
        "docs/literature_evidence_2026-10-18.csv",
        "docs/literature_search_2026-10-18.csv",
        "docs/clinical_validation_roadmap.md",
        "reports/enabl3s_cohort_primary_v1.csv",
        "DATA_SOURCES.md",
    ]:
        shutil.copy2(ROOT / source, assets / Path(source).name)
    print(
        f"Portfolio: {len(people)} eligible participants; {len(literature)} references; frozen hashes verified"
    )


if __name__ == "__main__":
    main()
