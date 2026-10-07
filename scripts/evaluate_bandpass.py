"""Clock-derived sampling rate, 20-450 Hz band-pass sensitivity and in-band QA."""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import os

import numpy as np

from src.data.semg import recordings
from src.data.tables import write_csv
from src.features.quality import (
    EMG_BAND_HZ,
    bandpass,
    excluded_pairs,
    rms_retention_ratio,
    sampling_rate_from_clock,
    short_records,
)
from src.features.specifications import specifications

os.environ.setdefault("MPLCONFIGDIR", str(ROOT / ".mpl-cache"))
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Review heuristic, chosen after inspecting the spectra; not an exclusion rule.
LOW_RMS_RETENTION = 0.8
# All clocks must agree within this relative spread before one rate is used.
MAX_RATE_SPREAD = 0.002


def crosses_one(ratios):
    logs = np.log([r for r in ratios if np.isfinite(r) and r > 0])
    return bool(np.any(logs < 0) and np.any(logs > 0))


def main():
    records = list(recordings())
    rates = [sampling_rate_from_clock(r["time_exported_s"]) for r in records]
    fs = float(np.median(rates))
    spread = (max(rates) - min(rates)) / fs
    assert spread < MAX_RATE_SPREAD, f"Clock rates disagree ({spread:.4f})"
    short = short_records({**r, "samples": len(r["semg_V"])} for r in records)
    excluded = excluded_pairs({**r, "samples": len(r["semg_V"])} for r in records)

    audit, grouped = [], {}
    for record, rate in zip(records, rates):
        x = record["semg_V"]
        key = (record["participant_id"], record["condition"], record["limb_label"])
        share = rms_retention_ratio(x, fs)
        flags = []
        if key in short:
            flags.append("short_record")
        if share < LOW_RMS_RETENTION:
            flags.append("low_rms_retention_ratio")
        audit.append(
            {
                "participant_id": record["participant_id"],
                "cohort": record["cohort"],
                "condition": record["condition"],
                "limb_label": record["limb_label"],
                "samples": len(x),
                "duration_s": len(x) / fs,
                "clock_rate_hz": rate,
                "duplicate_timestamp_fraction": float(
                    np.mean(np.diff(record["time_exported_s"]) == 0)
                ),
                "rms_retention_ratio": share,
                "filtered_mean_square_ratio": share**2,
                "qa_flags": ";".join(flags),
            }
        )
        pair = (record["participant_id"], record["cohort"], record["condition"])
        grouped.setdefault(pair, {})[record["limb_label"]] = {
            "exported": specifications(x),
            "bandpass": specifications(bandpass(x, fs)),
        }

    rows, pairs = [], []
    for (person, cohort, condition), limbs in sorted(grouped.items()):
        summary = {
            "participant_id": person,
            "cohort": cohort,
            "condition": condition,
            "primary_pair": (person, condition) not in excluded,
        }
        for processing in ("exported", "bandpass"):
            ratios = {}
            for method, a in limbs["inv"][processing].items():
                b = limbs["uninv"][processing][method]
                ratios[method] = a / b if b > 0 else np.nan
                rows.append(
                    {
                        "participant_id": person,
                        "cohort": cohort,
                        "condition": condition,
                        "processing": processing,
                        "method": method,
                        "ratio": ratios[method],
                    }
                )
            summary[f"{processing}_whole_rms_ratio"] = ratios["whole_RMS"]
            summary[f"{processing}_rms_crosses_one"] = crosses_one(
                v for m, v in ratios.items() if m.endswith("RMS")
            )
        summary["whole_rms_direction_changes"] = bool(
            (summary["exported_whole_rms_ratio"] - 1)
            * (summary["bandpass_whole_rms_ratio"] - 1)
            < 0
        )
        pairs.append(summary)
    write_csv(ROOT / "reports/bandpass_signal_audit.csv", audit)
    write_csv(ROOT / "reports/bandpass_specifications.csv", rows)
    write_csv(ROOT / "reports/bandpass_paired_summary.csv", pairs)

    primary = [p for p in pairs if p["primary_pair"]]
    flips = [p for p in primary if p["whole_rms_direction_changes"]]
    changes = sorted(
        (
            {
                "pair": f"{p['participant_id']}/{p['condition']}",
                "exported_ratio": p["exported_whole_rms_ratio"],
                "filtered_ratio": p["bandpass_whole_rms_ratio"],
                "relative_change_pct": 100
                * (p["bandpass_whole_rms_ratio"] / p["exported_whole_rms_ratio"] - 1),
                "absolute_log_change": abs(
                    np.log(
                        p["bandpass_whole_rms_ratio"] / p["exported_whole_rms_ratio"]
                    )
                ),
            }
            for p in primary
        ),
        key=lambda item: item["absolute_log_change"],
        reverse=True,
    )
    medians = {}
    for cohort in ("healthy", "patient"):
        for condition in ("iso90", "iso180"):
            subset = [
                p
                for p in primary
                if p["cohort"] == cohort and p["condition"] == condition
            ]
            medians[f"{cohort}/{condition}"] = {
                "pairs": len(subset),
                "exported": float(
                    np.median([p["exported_whole_rms_ratio"] for p in subset])
                ),
                "bandpass": float(
                    np.median([p["bandpass_whole_rms_ratio"] for p in subset])
                ),
            }
    low = sorted(
        (r for r in audit if "low_rms_retention_ratio" in r["qa_flags"]),
        key=lambda r: r["rms_retention_ratio"],
    )
    shares = np.array([r["rms_retention_ratio"] for r in audit])
    h = next(
        p
        for p in pairs
        if p["participant_id"] == "healthy8" and p["condition"] == "iso90"
    )
    h_uninv = next(
        r
        for r in audit
        if r["participant_id"] == "healthy8"
        and r["condition"] == "iso90"
        and r["limb_label"] == "uninv"
    )
    durations = sorted(r["duration_s"] for r in audit)

    fig, axes = plt.subplots(1, 2, figsize=(13, 5.5))
    ax = axes[0]
    for cohort, color in (("healthy", "tab:blue"), ("patient", "tab:orange")):
        for is_primary, marker in ((True, "o"), (False, "x")):
            subset = [
                p
                for p in pairs
                if p["cohort"] == cohort and p["primary_pair"] == is_primary
            ]
            if subset:
                ax.scatter(
                    [p["exported_whole_rms_ratio"] for p in subset],
                    [p["bandpass_whole_rms_ratio"] for p in subset],
                    color=color,
                    marker=marker,
                    s=60 if marker == "x" else 30,
                    label=cohort + ("" if is_primary else " (excluded pair)"),
                )
    ax.plot([0.1, 100], [0.1, 100], color="gray", linestyle="--")
    ax.axhline(1, color="gray", linewidth=0.6)
    ax.axvline(1, color="gray", linewidth=0.6)
    ax.set(
        xscale="log",
        yscale="log",
        xlabel="Exported whole-record RMS ratio (inv/uninv)",
        ylabel=f"{EMG_BAND_HZ[0]:.0f}-{EMG_BAND_HZ[1]:.0f} Hz band-passed RMS ratio",
        title="A. Band-pass sensitivity: 44 participant-condition pairs",
    )
    ax.legend(fontsize=8)
    ax = axes[1]
    order = np.argsort(shares)
    colors = ["tab:red" if shares[i] < LOW_RMS_RETENTION else "tab:gray" for i in order]
    ax.scatter(range(len(shares)), shares[order], color=colors, s=18)
    ax.axhline(LOW_RMS_RETENTION, color="tab:red", linestyle="--", linewidth=0.8)
    for rank, i in enumerate(order[: len(low)]):
        r = audit[i]
        ax.annotate(
            f"{r['participant_id']} {r['condition']} {r['limb_label']}",
            (rank, shares[i]),
            xytext=(12, 0.3 + 0.07 * rank),
            fontsize=8,
            arrowprops={"arrowstyle": "-", "color": "tab:red", "linewidth": 0.6},
        )
    ax.set(
        ylim=(0, 1.05),
        xlabel="Recordings sorted by RMS retention",
        ylabel="Band-passed RMS / mean-centered RMS",
        title=f"B. RMS retained after this filter (fs = {fs:.1f} Hz from clocks)",
    )
    fig.tight_layout()
    fig.savefig(ROOT / "reports/figures/bandpass_sensitivity.png", dpi=150)
    plt.close(fig)

    checks = {
        "recordings": len(audit),
        "pairs": len(pairs),
        "primary_pairs": len(primary),
        "excluded_pairs": sorted("/".join(k) for k in excluded),
        "sampling_rate_hz": fs,
        "clock_rate_min_hz": min(rates),
        "clock_rate_max_hz": max(rates),
        "band_hz": list(EMG_BAND_HZ),
        "filter_design": {
            "prototype_N": 4,
            "bandpass_order_per_pass": 8,
            "forward_backward_effective_order": 16,
            "method": "butter SOS + sosfiltfilt",
        },
        "largest_primary_individual_changes": changes[:5],
        "specification_rows": len(rows),
        "primary_whole_rms_direction_changes": len(flips),
        "primary_whole_rms_direction_change_pairs": [
            f"{p['participant_id']}/{p['condition']}" for p in flips
        ],
        "primary_rms_crossings_exported": sum(
            p["exported_rms_crosses_one"] for p in primary
        ),
        "primary_rms_crossings_bandpass": sum(
            p["bandpass_rms_crosses_one"] for p in primary
        ),
        "median_whole_rms_ratio_primary": medians,
        "median_rms_retention_ratio": float(np.median(shares)),
        "low_rms_retention_ratio_records": [
            {
                "record": f"{r['participant_id']}/{r['condition']}/{r['limb_label']}",
                "rms_retention_ratio": r["rms_retention_ratio"],
            }
            for r in low
        ],
        "healthy8_iso90": {
            "exported_ratio": h["exported_whole_rms_ratio"],
            "bandpass_ratio": h["bandpass_whole_rms_ratio"],
            "uninv_duration_s": h_uninv["duration_s"],
            "uninv_rms_retention_ratio": h_uninv["rms_retention_ratio"],
            "uninv_filtered_mean_square_ratio": h_uninv["filtered_mean_square_ratio"],
            "next_shortest_duration_s": durations[1],
        },
    }
    (ROOT / "reports/bandpass_checks.json").write_text(
        json.dumps(checks, indent=2), encoding="utf-8"
    )

    median_lines = "\n".join(
        f"| {k} | {v['pairs']} | {v['exported']:.3f} | {v['bandpass']:.3f} |"
        for k, v in medians.items()
    )
    low_lines = ", ".join(
        f"{r['participant_id']}/{r['condition']}/{r['limb_label']} ({r['rms_retention_ratio']:.2f})"
        for r in low
    )
    flip_text = (
        ", ".join(
            f"{p['participant_id']}/{p['condition']} "
            f"({p['exported_whole_rms_ratio']:.3f} â†’ {p['bandpass_whole_rms_ratio']:.3f})"
            for p in flips
        )
        or "none"
    )
    (ROOT / "docs/history/bandpass_results.md").write_text(
        f"""# Band-pass sensitivity and signal-validity audit

Generated by `scripts/evaluate_bandpass.py`. Retrospective analysis added on 2026-10-07 after review; not preregistered.

## Sampling rate

The authors do not state the EMG sampling rate for this export. Every one of the {len(audit)} exported clocks gives (samples âˆ’ 1) / elapsed time between {min(rates):.2f} and {max(rates):.2f} Hz (median {fs:.2f} Hz). The agreement supports using the median as an average-rate estimate for sensitivity analysis. Nondecreasing clocks are required, while duplicates are retained. Uniform acquisition is an explicit assumption: endpoint agreement cannot establish the cause of duplicated times or rule out missing samples. Rounding is a possible explanation, not a demonstrated cause. Original device preprocessing remains undocumented.

## Band-pass specification

A Butterworth prototype N=4 band-pass (order 8 per direction, effective order 16 after forward/backward filtering) of {EMG_BAND_HZ[0]:.0f}â€“{EMG_BAND_HZ[1]:.0f} Hz (a common surface-EMG band) was applied to each record and all 21 amplitude specifications were recomputed ({len(rows)} evaluations). It is an additional specification, not a replacement for the exported baseline.

Across the {len(primary)} primary pairs, whole-record RMS direction changes after band-pass: {len(flips)} â€” {flip_text}. RMS-specification crossings of ratio 1: {checks["primary_rms_crossings_exported"]} exported versus {checks["primary_rms_crossings_bandpass"]} band-passed.

| Cohort/condition | Pairs | Median exported ratio | Median band-passed ratio |
|---|---|---|---|
{median_lines}

## Group summaries and individual changes

Small shifts in group medians do not imply stability for every recording. The largest primary individual change is {changes[0]["pair"]}: {changes[0]["exported_ratio"]:.3f} â†’ {changes[0]["filtered_ratio"]:.3f} ({changes[0]["relative_change_pct"]:+.1f}%). RMS-specification crossings change from 10 to 8. These are descriptive sensitivity results, not clinical equivalence or evidence of practical clinical importance.

## RMS retention as a review indicator

RMS retention is band-passed RMS divided by mean-centered RMS. Its square is the ratio of filtered to centered mean square. The filter has transition attenuation and edge effects, so neither is a direct partition of spectral energy. Its median across recordings is {np.median(shares):.3f}. Records below {LOW_RMS_RETENTION}: {low_lines or "none"}. Low values indicate RMS attenuation under this specific filter, without identifying its physiological or acquisition cause. The {LOW_RMS_RETENTION} cut-off is a retrospective review heuristic; this flag does not cause exclusion. Eligibility is determined separately by the record-length rule; all records remain in sensitivity outputs.

## healthy8 / iso90 pair validity

The healthy8 iso90 uninv record lasts {h_uninv["duration_s"]:.2f} s; the next shortest of all {len(audit)} records lasts {durations[1]:.1f} s. It meets the existing short-record rule (below 25% of the cohort-condition median length), and its RMS retention is {h_uninv["rms_retention_ratio"]:.3f}: RMS decreases by {100 * (1 - h_uninv["rms_retention_ratio"]):.1f}% and mean square decreases by {100 * (1 - h_uninv["filtered_mean_square_ratio"]):.1f}% under this filter. These are not percentages of energy proven to lie outside the band. A whole-record ratio between a ~25 s task and a ~2 s fragment does not compare like with like, so this pair is excluded from the primary presentation and retained as a sensitivity analysis. Its ratio is {h["exported_whole_rms_ratio"]:.1f} exported and {h["bandpass_whole_rms_ratio"]:.1f} band-passed. The rule and its promotion to an exclusion were decided retrospectively; the cause (truncated export, failed trial or acquisition issue) cannot be determined from the files.

Filter implementation: [SciPy butter](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.butter.html), [sosfiltfilt](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.sosfiltfilt.html). The band and review threshold are sensitivity choices, not validated clinical cut-offs.

![Band-pass sensitivity](../../reports/figures/bandpass_sensitivity.png)
""",
        encoding="utf-8",
    )
    print(json.dumps(checks))


if __name__ == "__main__":
    main()
