"""Generate diagnostic plots and QA metrics; no filters, time repair or exclusions."""

import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from src.data.semg import recordings


def longest_run(mask):
    padded = np.r_[False, mask, False].astype(int)
    starts = np.flatnonzero(np.diff(padded) == 1)
    ends = np.flatnonzero(np.diff(padded) == -1)
    return int((ends - starts).max()) if len(starts) else 0


def main():
    output = ROOT / "reports/figures"
    output.mkdir(exist_ok=True)
    plt.rcParams.update(
        {"font.size": 9, "axes.spines.top": False, "axes.spines.right": False}
    )
    rows = []
    for cohort in ["healthy", "patient"]:
        for condition in ["iso90", "iso180"]:
            selected = [
                r
                for r in recordings()
                if r["cohort"] == cohort and r["condition"] == condition
            ]
            ids = sorted(
                {r["participant_id"] for r in selected},
                key=lambda s: int(s[len(cohort) :]),
            )
            fig, axes = plt.subplots(
                len(ids), 2, figsize=(13, 1.5 * len(ids)), squeeze=False
            )
            for record in selected:
                values = record["semg_V"]
                times = record["time_exported_s"]
                ax = axes[
                    ids.index(record["participant_id"]),
                    0 if record["limb_label"] == "inv" else 1,
                ]
                # A min/max envelope preserves short spikes when reducing visual density.
                edges = np.linspace(
                    0, len(values), min(801, len(values) + 1), dtype=int
                )
                centers = []
                low = []
                high = []
                for a, b in zip(edges[:-1], edges[1:]):
                    centers.append((a + b - 1) / 2)
                    low.append(values[a:b].min() * 1000)
                    high.append(values[a:b].max() * 1000)
                ax.fill_between(centers, low, high, color="#236a8d", alpha=0.8)
                ax.set_title(
                    f"{record['participant_id']} / {record['limb_label']} / n={len(values):,}",
                    loc="left",
                    fontsize=8,
                )
                ax.set_ylabel("sEMG (mV)")
                ax.set_xlabel("Original sample index")
                ax.grid(alpha=0.15)
                differences = np.diff(times)
                rows.append(
                    {
                        **{
                            k: record[k]
                            for k in [
                                "source_file",
                                "participant_id",
                                "cohort",
                                "condition",
                                "limb_label",
                            ]
                        },
                        "samples": len(values),
                        "padding_removed": record["padding_removed"],
                        "negative_fraction": float(np.mean(values < 0)),
                        "zero_fraction": float(np.mean(values == 0)),
                        "longest_zero_run_samples": longest_run(values == 0),
                        "longest_equal_step_run": longest_run(np.diff(values) == 0),
                        "duplicate_time_steps": int(np.sum(differences == 0)),
                        "negative_time_steps": int(np.sum(differences < 0)),
                        "whole_record_rms_V_QA_only": float(
                            np.sqrt(np.mean(values**2))
                        ),
                        "whole_record_MAV_V_QA_only": float(np.mean(np.abs(values))),
                        "peak_abs_V_QA_only": float(np.max(np.abs(values))),
                    }
                )
            fig.suptitle(
                f"{cohort} / {condition}: all exported signals; min-max envelope; independent vertical scales",
                fontsize=12,
            )
            fig.tight_layout(rect=[0, 0, 1, 0.98])
            fig.savefig(output / f"{cohort}_{condition}_signal_review.png", dpi=100)
            plt.close(fig)
    with (ROOT / "reports/signal_quality.csv").open(
        "w", newline="", encoding="utf-8"
    ) as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    for condition, color in [("iso90", "#b65139"), ("iso180", "#236a8d")]:
        example = next(
            r
            for r in recordings()
            if r["participant_id"] == "patient1"
            and r["condition"] == condition
            and r["limb_label"] == "inv"
        )
        t = example["time_exported_s"]
        index = example["sample_index"]
        axes[0].plot(index, t, label=condition, color=color)
        mask = (t >= 9.98) & (t <= 10.12)
        axes[1].plot(
            index[mask], t[mask], ".-", label=condition, color=color, markersize=2
        )
    for ax in axes:
        ax.set_xlabel("Original sample index")
        ax.set_ylabel("Exported time (s)")
        ax.legend()
        ax.grid(alpha=0.2)
    axes[0].set_title("Patient1 involved: original clocks")
    axes[1].set_title("Detail near 10 seconds: timestamp plateaus")
    fig.tight_layout()
    fig.savefig(output / "patient_involved_time_review.png", dpi=110)
    plt.close(fig)
    summary = {
        "records": len(rows),
        "all_signals_have_negative_values": all(
            r["negative_fraction"] > 0 for r in rows
        ),
        "longest_zero_run_samples": max(r["longest_zero_run_samples"] for r in rows),
        "max_zero_fraction": max(r["zero_fraction"] for r in rows),
        "excluded_records": 0,
        "time_reconstructed": False,
        "filtered": False,
        "note": "RMS/MAV describe full exported tasks for QA only; not normalized activation or contraction-cycle features.",
    }
    (ROOT / "reports/signal_review_summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
