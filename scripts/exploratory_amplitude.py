"""Participant-level descriptive sEMG EDA, deterministic bootstrap and QA sensitivities."""

import csv
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault("MPLCONFIGDIR", str(ROOT / ".mpl-cache"))
sys.path.insert(0, str(ROOT))
import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from src.data.semg import recordings
from src.features.amplitude import ratio, summarize


def save_csv(path, rows):
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def boot_median(values, rng):
    x = np.asarray(values, dtype=float)
    medians = np.median(rng.choice(x, size=(5000, len(x)), replace=True), axis=1)
    return [float(v) for v in np.quantile(medians, [0.025, 0.975])]


def main():
    records = list(recordings())
    features = []
    for record in records:
        x = record["semg_V"]
        n = len(x)
        flags = []
        reference_length = np.median(
            [
                len(r["semg_V"])
                for r in records
                if r["cohort"] == record["cohort"]
                and r["condition"] == record["condition"]
            ]
        )
        if n < 0.25 * reference_length:
            flags.append("short_record_review")
        rms = np.sqrt(np.mean(x * x))
        if rms > 0 and abs(x.mean()) / rms >= 0.1:
            flags.append("mean_gt10pct_rms_review")
        if np.any(np.diff(record["time_exported_s"]) == 0):
            flags.append("duplicate_exported_time")
        # QA heuristic only: unusually extreme peaks need review, not automatic deletion.
        p95 = np.quantile(np.abs(x), 0.95)
        if p95 > 0 and np.max(np.abs(x)) / p95 > 10:
            flags.append("peak_gt10x_p95_review")
        features.append(
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
                "samples": n,
                "padding_removed": record["padding_removed"],
                "qa_flags": ";".join(flags),
                **summarize(x),
            }
        )
    (ROOT / "data/processed").mkdir(exist_ok=True)
    save_csv(ROOT / "data/processed/semg_amplitude_features.csv", features)
    paired = []
    for cohort in ["healthy", "patient"]:
        for condition in ["iso90", "iso180"]:
            ids = sorted(
                {r["participant_id"] for r in features if r["cohort"] == cohort},
                key=lambda s: int(s[len(cohort) :]),
            )
            for participant in ids:
                inv = next(
                    r
                    for r in features
                    if r["participant_id"] == participant
                    and r["condition"] == condition
                    and r["limb_label"] == "inv"
                )
                uninv = next(
                    r
                    for r in features
                    if r["participant_id"] == participant
                    and r["condition"] == condition
                    and r["limb_label"] == "uninv"
                )
                entry = {
                    "participant_id": participant,
                    "cohort": cohort,
                    "condition": condition,
                    "qa_flags": ";".join(
                        sorted(
                            set(
                                filter(
                                    None,
                                    (inv["qa_flags"] + ";" + uninv["qa_flags"]).split(
                                        ";"
                                    ),
                                )
                            )
                        )
                    ),
                }
                for metric in ["rms_V", "mav_V", "rms_cap995_V_sensitivity"]:
                    a, b = inv[metric], uninv[metric]
                    entry.update(
                        {
                            f"{metric}_inv": a,
                            f"{metric}_uninv": b,
                            f"{metric}_inv_uninv_ratio": ratio(a, b),
                            f"{metric}_min_max_pct": 100 * ratio(min(a, b), max(a, b)),
                        }
                    )
                paired.append(entry)
    save_csv(ROOT / "data/processed/semg_paired_amplitude.csv", paired)
    rng = np.random.default_rng(20261004)
    summaries = []
    for sensitivity in ["all_records", "without_rule_flagged_short_pairs"]:
        for cohort in ["healthy", "patient"]:
            for condition in ["iso90", "iso180"]:
                subset = [
                    r
                    for r in paired
                    if r["cohort"] == cohort
                    and r["condition"] == condition
                    and not (
                        sensitivity != "all_records"
                        and "short_record_review" in r["qa_flags"]
                    )
                ]
                for metric in ["rms_V", "mav_V"]:
                    x = [r[f"{metric}_inv_uninv_ratio"] for r in subset]
                    lo, hi = boot_median(x, rng)
                    summaries.append(
                        {
                            "sensitivity": sensitivity,
                            "cohort": cohort,
                            "condition": condition,
                            "metric": metric,
                            "participants": len(x),
                            "median_inv_uninv_ratio": float(np.median(x)),
                            "q25": float(np.quantile(x, 0.25)),
                            "q75": float(np.quantile(x, 0.75)),
                            "median_bootstrap95_low": lo,
                            "median_bootstrap95_high": hi,
                        }
                    )
    save_csv(ROOT / "reports/amplitude_group_summary.csv", summaries)
    output = ROOT / "reports/figures"
    output.mkdir(exist_ok=True)
    plt.rcParams.update(
        {"font.size": 10, "axes.spines.top": False, "axes.spines.right": False}
    )
    for metric, title in [
        ("rms_V", "Whole-record RMS"),
        ("mav_V", "Whole-record mean absolute amplitude"),
    ]:
        fig, axes = plt.subplots(2, 2, figsize=(13, 9))
        for i, cohort in enumerate(["healthy", "patient"]):
            for j, condition in enumerate(["iso90", "iso180"]):
                ax = axes[i, j]
                subset = [
                    r
                    for r in paired
                    if r["cohort"] == cohort and r["condition"] == condition
                ]
                for r in subset:
                    flagged = bool(r["qa_flags"])
                    color = "#be573c" if flagged else "#236a8d"
                    ax.plot(
                        [0, 1],
                        [r[f"{metric}_inv"] * 1e6, r[f"{metric}_uninv"] * 1e6],
                        ".-",
                        color=color,
                        alpha=0.65,
                    )
                ax.set_xticks([0, 1], ["inv (source label)", "uninv (source label)"])
                ax.set_xlim(-0.15, 1.5)
                ax.set_yscale("log")
                ax.set_ylabel("Amplitude (microvolts; log scale)")
                ax.set_title(f"{cohort} / {condition} / n={len(subset)}")
                ax.grid(alpha=0.2)
        fig.suptitle(
            title
            + " — each line is one individual; orange = QA review flag\nIndependent vertical scales; exported tasks include rest; not strength",
            fontsize=12,
        )
        fig.tight_layout(rect=[0, 0, 1, 0.93])
        fig.savefig(output / f"{metric}_paired_amplitude.png", dpi=160)
        plt.close(fig)
    fig, axes = plt.subplots(1, 2, figsize=(13, 6))
    for ax, cohort in zip(axes, ["healthy", "patient"]):
        ids = sorted(
            {r["participant_id"] for r in paired if r["cohort"] == cohort},
            key=lambda s: int(s[len(cohort) :]),
        )
        for y, participant in enumerate(ids):
            for condition, offset, color in [
                ("iso90", -0.12, "#236a8d"),
                ("iso180", 0.12, "#be573c"),
            ]:
                r = next(
                    r
                    for r in paired
                    if r["participant_id"] == participant
                    and r["condition"] == condition
                )
                ax.scatter(
                    r["rms_V_inv_uninv_ratio"],
                    y + offset,
                    color=color,
                    marker="x" if "short_record_review" in r["qa_flags"] else "o",
                    label=condition if y == 0 else None,
                )
        ax.axvline(1, color="gray", linestyle="--")
        ax.set_xscale("log")
        ax.set_yticks(range(len(ids)), ids)
        ax.invert_yaxis()
        ax.set_title(cohort)
        ax.legend()
        ax.grid(alpha=0.2)
        ax.set_xlabel("inv / uninv RMS ratio (log scale); 1 = equal amplitude")
    fig.suptitle(
        "Individual sEMG amplitude ratios — independent horizontal scales; no RTS threshold\nCross = short recording review; control limb orientation unresolved"
    )
    fig.tight_layout(rect=[0, 0, 1, 0.90])
    fig.savefig(output / "individual_rms_ratios.png", dpi=160)
    plt.close(fig)
    fig, axes = plt.subplots(1, 2, figsize=(12, 5), sharey=True)
    for ax, condition in zip(axes, ["iso90", "iso180"]):
        for position, (cohort, limb) in enumerate(
            [
                ("healthy", "inv"),
                ("healthy", "uninv"),
                ("patient", "inv"),
                ("patient", "uninv"),
            ]
        ):
            subset = [
                r
                for r in features
                if r["cohort"] == cohort
                and r["condition"] == condition
                and r["limb_label"] == limb
            ]
            values = np.array([r["rms_V"] * 1e6 for r in subset])
            ax.scatter(
                position + np.linspace(-0.12, 0.12, len(values)),
                values,
                color="#236a8d" if cohort == "healthy" else "#be573c",
                alpha=0.8,
                s=25,
            )
            ax.plot(
                [position - 0.2, position + 0.2],
                [np.median(values)] * 2,
                color="black",
                linewidth=2,
            )
        ax.set_xticks(
            range(4),
            ["healthy\ninv", "healthy\nuninv", "patient\ninv", "patient\nuninv"],
        )
        ax.set_yscale("log")
        ax.set_title(condition)
        ax.grid(axis="y", alpha=0.2)
    axes[0].set_ylabel("Whole-record RMS (microvolts; log scale)")
    fig.suptitle(
        "Exported amplitude distributions: individual values and medians\nShared vertical scale; unnormalized; limb labels do not establish comparable dominance"
    )
    fig.tight_layout(rect=[0, 0, 1, 0.88])
    fig.savefig(output / "rms_cohort_distributions.png", dpi=160)
    plt.close(fig)
    report = {
        "recordings": len(features),
        "paired_records": len(paired),
        "independent_participants": 22,
        "primary_exclusions": 0,
        "bootstrap_replicates": 5000,
        "seed": 20261004,
        "qa_flagged_recordings": sum(bool(r["qa_flags"]) for r in features),
        "group_summaries": summaries,
    }
    (ROOT / "reports/amplitude_eda_summary.json").write_text(
        json.dumps(report, indent=2), encoding="utf-8"
    )
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
