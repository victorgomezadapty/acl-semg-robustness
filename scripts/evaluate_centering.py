"""Preserve exported amplitudes and quantify record-mean sensitivity separately."""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import os

import numpy as np

from src.data.semg import recordings
from src.data.tables import write_csv
from src.features.amplitude import center_signal
from src.features.specifications import specifications

os.environ.setdefault("MPLCONFIGDIR", str(ROOT / ".mpl-cache"))
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def main():
    features, results, grouped = [], [], {}
    for record in recordings():
        x = record["semg_V"]
        centered = center_signal(x)
        rms = np.sqrt(np.mean(x * x))
        assert np.isclose(rms * rms, np.mean(centered * centered) + x.mean() ** 2)
        meta = {
            k: record[k]
            for k in ("participant_id", "cohort", "condition", "limb_label")
        }
        features.append(
            {
                **meta,
                "mean_V": x.mean(),
                "rms_exported_V": rms,
                "rms_centered_V": np.sqrt(np.mean(centered * centered)),
                "absolute_mean_over_rms": abs(x.mean()) / rms,
                "mean_square_fraction": (x.mean() / rms) ** 2,
            }
        )
        key = (record["participant_id"], record["cohort"], record["condition"])
        grouped.setdefault(key, {})[record["limb_label"]] = {
            "exported": specifications(x),
            "centered": specifications(centered),
        }
    pairs = []
    for (person, cohort, condition), limbs in sorted(grouped.items()):
        pair = {"participant_id": person, "cohort": cohort, "condition": condition}
        for preprocessing in ("exported", "centered"):
            logs = []
            for method, a in limbs["inv"][preprocessing].items():
                b = limbs["uninv"][preprocessing][method]
                ratio = a / b if b > 0 else np.nan
                results.append(
                    {
                        "participant_id": person,
                        "cohort": cohort,
                        "condition": condition,
                        "preprocessing": preprocessing,
                        "method": method,
                        "ratio": ratio,
                    }
                )
                if method.endswith("RMS") and np.isfinite(ratio) and ratio > 0:
                    logs.append(np.log(ratio))
            pair[preprocessing + "_whole_rms_ratio"] = (
                limbs["inv"][preprocessing]["whole_RMS"]
                / limbs["uninv"][preprocessing]["whole_RMS"]
            )
            pair[preprocessing + "_rms_log_range"] = max(logs) - min(logs)
        pair["whole_rms_direction_changes"] = bool(
            (pair["exported_whole_rms_ratio"] - 1)
            * (pair["centered_whole_rms_ratio"] - 1)
            < 0
        )
        pairs.append(pair)
    write_csv(ROOT / "reports/centering_signal_audit.csv", features)
    write_csv(ROOT / "reports/centering_specifications.csv", results)
    write_csv(ROOT / "reports/centering_paired_summary.csv", pairs)
    fig, ax = plt.subplots(figsize=(7, 5))
    for cohort, color in [("healthy", "tab:blue"), ("patient", "tab:orange")]:
        subset = [p for p in pairs if p["cohort"] == cohort]
        ax.scatter(
            [p["exported_whole_rms_ratio"] for p in subset],
            [p["centered_whole_rms_ratio"] for p in subset],
            label=cohort,
            color=color,
        )
    ax.plot([0.2, 50], [0.2, 50], color="gray", linestyle="--")
    ax.set(
        xscale="log",
        yscale="log",
        xlabel="Exported RMS ratio (inv/uninv)",
        ylabel="Mean-centered RMS ratio (inv/uninv)",
        title="Record-mean sensitivity: 44 paired records",
    )
    ax.legend()
    fig.tight_layout()
    fig.savefig(ROOT / "reports/figures/centering_ratio_sensitivity.png", dpi=160)
    plt.close(fig)
    h = next(
        p
        for p in pairs
        if p["participant_id"] == "healthy8" and p["condition"] == "iso90"
    )
    denominator = next(
        r
        for r in features
        if r["participant_id"] == "healthy8"
        and r["condition"] == "iso90"
        and r["limb_label"] == "uninv"
    )
    mean_square_pct = 100 * denominator["mean_square_fraction"]
    count = sum(p["whole_rms_direction_changes"] for p in pairs)
    summary = {
        "recordings": len(features),
        "pairs": len(pairs),
        "specification_rows": len(results),
        "whole_rms_direction_changes": count,
        "healthy8_iso90": h,
    }
    (ROOT / "reports/centering_checks.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )
    (ROOT / "docs/history/centering_results.md").write_text(
        f"""# Record-mean sensitivity

The exported analysis is retained as a reproducibility baseline. Mean-centering is an additional retrospective specification, not proof that the record mean is instrument artefact. It does not replace filtering or recover contraction boundaries.

All {len(features)} recordings and {len(pairs)} participant-condition pairs were assessed with 21 methods before and after centering ({len(results)} evaluations). Whole-RMS direction changes occurred in {count} pairs. Independent observations remain participants, not specifications or pairs across repeated conditions.

For healthy8/iso90 the ratio increases from {h["exported_whole_rms_ratio"]:.3f} to {h["centered_whole_rms_ratio"]:.3f}. Removing the mean makes the denominator smaller; it does not resolve the extreme ratio. For that denominator, the mean accounts for {mean_square_pct:.1f}% of the mean square, not 84% of the RMS amplitude. The identity RMS² = centered RMS² + mean² is checked for every recording.

![Centering sensitivity](../../reports/figures/centering_ratio_sensitivity.png)

Primary presentation: within-participant log-ratio sensitivity, including centering; cross-person absolute-voltage tests are supplemental acquisition-dependent descriptions. Centering is not declared physiologically correct by default. No band-pass is applied: exported processing is incompletely documented and some clocks have duplicate timestamps. A guessed sampling frequency would not establish suitability for physiological filtering.

QA rules now identify length below 25% of the cohort-condition median and |mean|/RMS ≥0.1. These are review heuristics chosen retrospectively, not clinical thresholds or automatic exclusions. All records remain included.

Percentile bootstrap intervals remain exploratory and are not guaranteed to have nominal coverage at this sample size. Shapiro values are descriptive diagnostics only and never choose tests. No stronger clinical conclusion follows from changing an interval method.

Context: [CEDE normalization](https://doi.org/10.1016/j.jelekin.2020.102438), [processing choices](https://doi.org/10.1016/j.jelekin.2016.10.001), [original data](https://doi.org/10.5061/dryad.66t1g1k4j). Numerical results are calculated in this project, not taken from those papers.
""",
        encoding="utf-8",
    )
    print(json.dumps(summary))


if __name__ == "__main__":
    main()
