"""Complete currently supported sEMG analyses and publication comparison."""

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
from scipy import stats

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from src.analysis.statistics import compare, holm
from src.data.semg import recordings
from src.features.amplitude import summarize

METRICS = ["rms_V", "mav_V", "peak_abs_V", "peak_positive_V"]


def csvwrite(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as stream:
        w = csv.DictWriter(stream, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


def main():
    records = list(recordings())
    by = {(r["participant_id"], r["condition"], r["limb_label"]): r for r in records}
    ids = sorted(
        {r["participant_id"] for r in records},
        key=lambda p: (p.startswith("patient"), int("".join(filter(str.isdigit, p)))),
    )
    features = []
    blocks = []
    for r in records:
        x = r["semg_V"]
        f = {
            k: r[k]
            for k in [
                "participant_id",
                "cohort",
                "condition",
                "limb_label",
                "source_file",
            ]
        }
        f.update(summarize(x))
        f.update(
            {
                "samples": len(x),
                "peak_positive_V": float(x.max()),
                "mean_signed_V": float(x.mean()),
                "std_V": float(x.std(ddof=1)),
                "crest_factor": float(np.max(np.abs(x)) / np.sqrt(np.mean(x * x))),
            }
        )
        features.append(f)
        for size in [256, 512, 1024]:
            n = len(x) // size
            vals = np.sqrt(np.mean(x[: n * size].reshape(n, size) ** 2, axis=1))
            floor, top = np.quantile(vals, [0.2, 0.9])
            for fraction in [0.1, 0.2, 0.3]:
                threshold = floor + fraction * (top - floor)
                mask = vals > threshold
                selected = x[: n * size].reshape(n, size)[mask]
                blocks.append(
                    {
                        **{
                            k: r[k]
                            for k in [
                                "participant_id",
                                "cohort",
                                "condition",
                                "limb_label",
                            ]
                        },
                        "block_samples": size,
                        "threshold_fraction": fraction,
                        "threshold_rms_V": float(threshold),
                        "selected_blocks": int(mask.sum()),
                        "total_blocks": n,
                        "selected_fraction": float(mask.mean()),
                        "selected_rms_V": float(np.sqrt(np.mean(selected**2)))
                        if selected.size
                        else None,
                        "selected_mav_V": float(np.mean(np.abs(selected)))
                        if selected.size
                        else None,
                        "remainder_samples": len(x) % size,
                    }
                )
    csvwrite(ROOT / "data/processed/semg_extended_features.csv", features)
    csvwrite(ROOT / "reports/block_selection_sensitivity.csv", blocks)
    lookup = {
        (r["participant_id"], r["condition"], r["limb_label"]): r for r in features
    }
    pairs = []
    for p in ids:
        for condition in ["iso90", "iso180"]:
            a, b = lookup[p, condition, "inv"], lookup[p, condition, "uninv"]
            row = {"participant_id": p, "cohort": a["cohort"], "condition": condition}
            for metric in METRICS:
                row.update(
                    {
                        f"{metric}_inv": a[metric],
                        f"{metric}_uninv": b[metric],
                        f"{metric}_ratio_pct": 100 * a[metric] / b[metric],
                        f"{metric}_log_ratio": float(np.log(a[metric] / b[metric])),
                        f"{metric}_balance_pct": 100
                        * min(a[metric], b[metric])
                        / max(a[metric], b[metric]),
                    }
                )
            pairs.append(row)
    csvwrite(ROOT / "data/processed/semg_extended_pairs.csv", pairs)
    rng = np.random.default_rng(20261004)
    tests = []
    descriptives = []

    def add(family, name, endpoint, a, b, paired):
        tests.append(
            {
                "family": family,
                "comparison": name,
                "endpoint": endpoint,
                **compare(a, b, paired, rng),
            }
        )

    for metric in METRICS[:3]:
        for cohort in ["healthy", "patient"]:
            group = [p for p in ids if p.startswith(cohort)]
            for condition in ["iso90", "iso180"]:
                for limb in ["inv", "uninv"]:
                    x = np.array([lookup[p, condition, limb][metric] for p in group])
                    descriptives.append(
                        {
                            "cohort": cohort,
                            "condition": condition,
                            "limb_label": limb,
                            "metric": metric,
                            "n": len(x),
                            "mean_V": float(x.mean()),
                            "sd_V": float(x.std(ddof=1)),
                            "median_V": float(np.median(x)),
                            "q25_V": float(np.quantile(x, 0.25)),
                            "q75_V": float(np.quantile(x, 0.75)),
                        }
                    )
                a = [lookup[p, condition, "inv"][metric] for p in group]
                b = [lookup[p, condition, "uninv"][metric] for p in group]
                add(
                    "within_limb",
                    f"{cohort}/{condition}: inv minus uninv",
                    metric,
                    a,
                    b,
                    True,
                )
            for limb in ["inv", "uninv"]:
                add(
                    "within_condition",
                    f"{cohort}/{limb}: iso180 minus iso90",
                    metric,
                    [lookup[p, "iso180", limb][metric] for p in group],
                    [lookup[p, "iso90", limb][metric] for p in group],
                    True,
                )
            for endpoint in ["log_ratio", "balance_pct"]:
                a = [
                    next(
                        r
                        for r in pairs
                        if r["participant_id"] == p and r["condition"] == "iso180"
                    )[f"{metric}_{endpoint}"]
                    for p in group
                ]
                b = [
                    next(
                        r
                        for r in pairs
                        if r["participant_id"] == p and r["condition"] == "iso90"
                    )[f"{metric}_{endpoint}"]
                    for p in group
                ]
                add(
                    "within_condition",
                    f"{cohort}: iso180 minus iso90",
                    f"{metric}_{endpoint}",
                    a,
                    b,
                    True,
                )
        for condition in ["iso90", "iso180"]:
            for limb in ["inv", "uninv"]:
                add(
                    "between_cohort",
                    f"{condition}/{limb}: patient minus healthy",
                    metric,
                    [
                        r[metric]
                        for r in features
                        if r["cohort"] == "patient"
                        and r["condition"] == condition
                        and r["limb_label"] == limb
                    ],
                    [
                        r[metric]
                        for r in features
                        if r["cohort"] == "healthy"
                        and r["condition"] == condition
                        and r["limb_label"] == limb
                    ],
                    False,
                )
            for endpoint in ["log_ratio", "balance_pct"]:
                add(
                    "between_cohort",
                    f"{condition}: patient minus healthy",
                    f"{metric}_{endpoint}",
                    [
                        r[f"{metric}_{endpoint}"]
                        for r in pairs
                        if r["cohort"] == "patient" and r["condition"] == condition
                    ],
                    [
                        r[f"{metric}_{endpoint}"]
                        for r in pairs
                        if r["cohort"] == "healthy" and r["condition"] == condition
                    ],
                    False,
                )
    for family in sorted({r["family"] for r in tests}):
        subset = [r for r in tests if r["family"] == family]
        for r, p, q in zip(
            subset,
            holm([r["p_raw"] for r in subset]),
            holm([r["rank_p_raw"] for r in subset]),
        ):
            r["p_holm_family"] = float(p)
            r["rank_p_holm_family"] = float(q)
            r["family_tests"] = len(subset)
    csvwrite(ROOT / "reports/exploratory_tests.csv", tests)
    csvwrite(ROOT / "reports/amplitude_descriptives.csv", descriptives)
    correlations = []
    for cohort in ["healthy", "patient"]:
        for condition in ["iso90", "iso180"]:
            for limb in ["inv", "uninv"]:
                sub = [
                    r
                    for r in features
                    if r["cohort"] == cohort
                    and r["condition"] == condition
                    and r["limb_label"] == limb
                ]
                for a, b in [
                    ("rms_V", "mav_V"),
                    ("rms_V", "peak_abs_V"),
                    ("samples", "rms_V"),
                ]:
                    res = stats.spearmanr([r[a] for r in sub], [r[b] for r in sub])
                    correlations.append(
                        {
                            "cohort": cohort,
                            "condition": condition,
                            "limb_label": limb,
                            "a": a,
                            "b": b,
                            "n": len(sub),
                            "spearman_rho": float(res.statistic),
                            "p_raw": float(res.pvalue),
                        }
                    )
    for r, p in zip(correlations, holm([r["p_raw"] for r in correlations])):
        r["p_holm_all"] = float(p)
    csvwrite(ROOT / "reports/exploratory_correlations.csv", correlations)
    published = {
        ("patient", "iso90"): (90.2, 7.9, 91.4, 8.6),
        ("patient", "iso180"): (87.5, 9.8, 88.3, 10.4),
        ("healthy", "iso90"): (96.8, 3.5, 97.6, 3.1),
        ("healthy", "iso180"): (96.1, 4.2, 96.9, 3.8),
    }
    comparison = []
    for (cohort, condition), reported in published.items():
        for metric, offset in [("rms_V", 0), ("peak_abs_V", 2), ("peak_positive_V", 2)]:
            x = np.array(
                [
                    r[f"{metric}_ratio_pct"]
                    for r in pairs
                    if r["cohort"] == cohort and r["condition"] == condition
                ]
            )
            comparison.append(
                {
                    "cohort": cohort,
                    "condition": condition,
                    "metric": metric,
                    "n": len(x),
                    "our_whole_record_mean_pct": float(x.mean()),
                    "our_whole_record_sd_pct": float(x.std(ddof=1)),
                    "published_mean_pct": reported[offset],
                    "published_sd_pct": reported[offset + 1],
                    "mean_difference_pp": float(x.mean() - reported[offset]),
                    "status": "not_exact_replication_unknown_processing_and_cycle_boundaries",
                }
            )
    csvwrite(ROOT / "reports/publication_comparison.csv", comparison)
    figures = ROOT / "reports/figures"
    figures.mkdir(exist_ok=True)
    profiles = figures / "profiles"
    profiles.mkdir(exist_ok=True)
    plt.rcParams.update(
        {"axes.spines.top": False, "axes.spines.right": False, "font.size": 9}
    )
    fig, axes = plt.subplots(2, 3, figsize=(15, 9))
    for j, metric in enumerate(METRICS[:3]):
        for i, condition in enumerate(["iso90", "iso180"]):
            ax = axes[i, j]
            for position, cohort in enumerate(["healthy", "patient"]):
                x = [
                    r[f"{metric}_balance_pct"]
                    for r in pairs
                    if r["cohort"] == cohort and r["condition"] == condition
                ]
                ax.boxplot(x, positions=[position], widths=0.4, showfliers=False)
                ax.scatter(
                    position + np.linspace(-0.12, 0.12, len(x)),
                    x,
                    s=25,
                    color="#236a8d" if cohort == "healthy" else "#be573c",
                )
            ax.set_xticks([0, 1], ["healthy", "patient"])
            ax.set_ylim(0, 105)
            ax.set_title(f"{condition} / {metric}")
            ax.set_ylabel("min / max amplitude (%)")
            ax.grid(axis="y", alpha=0.2)
    fig.suptitle(
        "Orientation-independent sEMG balance — individuals and distributions\nWhole exported records; not strength LSI or RTS classification"
    )
    fig.tight_layout(rect=[0, 0, 1, 0.93])
    fig.savefig(figures / "extended_balance_distributions.png", dpi=150)
    plt.close(fig)
    for p in ids:
        fig, axes = plt.subplots(2, 3, figsize=(14, 7))
        cohort = "patient" if p.startswith("patient") else "healthy"
        for i, condition in enumerate(["iso90", "iso180"]):
            ax = axes[i, 0]
            for limb, color in [("inv", "#236a8d"), ("uninv", "#be573c")]:
                r = by[p, condition, limb]
                x = r["semg_V"]
                edges = np.linspace(0, len(x), 401, dtype=int)
                ax.fill_between(
                    [(a + b) / 2 for a, b in zip(edges[:-1], edges[1:])],
                    [x[a:b].min() * 1e6 for a, b in zip(edges[:-1], edges[1:])],
                    [x[a:b].max() * 1e6 for a, b in zip(edges[:-1], edges[1:])],
                    alpha=0.45,
                    label=limb,
                    color=color,
                )
            ax.set_title(condition + " / exported signals")
            ax.set_xlabel("Sample index (not time)")
            ax.set_ylabel("microvolts")
            ax.legend()
            for j, metric in enumerate(["rms_V", "peak_abs_V"], start=1):
                ax = axes[i, j]
                for position, limb in enumerate(["inv", "uninv"]):
                    controls = [
                        r[metric] * 1e6
                        for r in features
                        if r["cohort"] == "healthy"
                        and r["condition"] == condition
                        and r["limb_label"] == limb
                    ]
                    ax.boxplot(
                        controls, positions=[position], widths=0.4, showfliers=False
                    )
                    ax.scatter(
                        position,
                        lookup[p, condition, limb][metric] * 1e6,
                        s=60,
                        color="#be573c",
                        zorder=4,
                    )
                ax.set_xticks([0, 1], ["inv", "uninv"])
                ax.set_yscale("log")
                ax.set_ylabel("microvolts (log)")
                ax.set_title(metric + " / dot = selected; box = controls")
        pair_text = " | ".join(
            f"{c}: RMS ratio {next(r for r in pairs if r['participant_id'] == p and r['condition'] == c)['rms_V_ratio_pct']:.1f}%"
            for c in ["iso90", "iso180"]
        )
        fig.suptitle(
            f"{p} / {cohort} — exploratory exported-signal profile\n{pair_text}\nReference is descriptive; controls include self for control profiles; not physiological normalization",
            fontsize=11,
        )
        fig.tight_layout(rect=[0, 0, 1, 0.88])
        fig.savefig(profiles / f"{p}.png", dpi=140)
        plt.close(fig)
    summary = {
        "records": len(features),
        "participant_pairs": len(pairs),
        "participants": len(ids),
        "comparisons": len(tests),
        "correlations": len(correlations),
        "profiles": len(ids),
        "selection_sensitivity_rows": len(blocks),
        "seed": 20261004,
        "holm_t_below_005": sum(r["p_holm_family"] < 0.05 for r in tests),
        "holm_rank_below_005": sum(r["rank_p_holm_family"] < 0.05 for r in tests),
        "exact_publication_replication": False,
    }
    (ROOT / "reports/comprehensive_summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
