"""Controlled measurement perturbations; synthetic signals, not patient models."""

import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import os

from src.features.specifications import specifications

os.environ.setdefault("MPLCONFIGDIR", str(ROOT / ".mpl-cache"))
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


def save(name, rows):
    with (ROOT / "reports" / name).open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main():
    rows = []
    for replicate in range(100):
        rng = np.random.default_rng(2026100600 + replicate)
        n = 16384
        envelope = np.repeat(rng.uniform(0.3, 1.7, n // 1024), 1024)
        b = rng.normal(size=n) * envelope
        a = 0.8 * b
        independent = rng.normal(size=n) * envelope
        independent *= np.sqrt(np.mean(a * a) / np.mean(independent * independent))
        spike = a.copy()
        spike[rng.integers(n)] += 150
        broad = a.copy()
        broad[4096:5120] *= 8
        # This sustained event is part of the intended signal, not an artefact.
        physiological_target = np.sqrt(np.mean(broad * broad) / np.mean(b * b))
        scenarios = {
            "clean_shared_carrier": (a, b, 0.8),
            "clean_independent_carrier": (independent, b, 0.8),
            "common_gain": (7 * a, 7 * b, 0.8),
            "unequal_pause": (np.r_[a, np.zeros(3 * n)], b, 0.8),
            "single_spike_artifact": (spike, b, 0.8),
            "asymmetric_noise": (a + rng.normal(0, 0.8, n), b, 0.8),
            "unequal_sensor_gain": (1.5 * a, b, 0.8),
            "denominator_attenuation": (a, 0.1 * b, 0.8),
            "sustained_true_event": (broad, b, physiological_target),
            "near_symmetry": (1.001 * b, b, 1.001),
            "exact_symmetry": (b.copy(), b, 1.0),
        }
        for scenario, (x, y, target) in scenarios.items():
            numerator, denominator = specifications(x), specifications(y)
            for method in numerator:
                ratio = (
                    numerator[method] / denominator[method]
                    if denominator[method] > 0
                    else np.nan
                )
                valid = bool(np.isfinite(ratio) and ratio > 0)
                rows.append(
                    dict(
                        scenario=scenario,
                        replicate=replicate,
                        seed=2026100600 + replicate,
                        method=method,
                        target_ratio=target,
                        observed_ratio=ratio,
                        valid=valid,
                        absolute_log_error=abs(np.log(ratio / target))
                        if valid
                        else np.nan,
                        direction_mismatch=bool(
                            np.sign(np.log(ratio)) != np.sign(np.log(target))
                        )
                        if valid
                        else "",
                    )
                )
    save("synthetic_scenario_results.csv", rows)
    summaries = []
    for scenario in scenarios:
        for method in numerator:
            subset = [
                r for r in rows if r["scenario"] == scenario and r["method"] == method
            ]
            valid = [r for r in subset if r["valid"]]
            errors = np.array([r["absolute_log_error"] for r in valid])
            summaries.append(
                dict(
                    scenario=scenario,
                    method=method,
                    replicates=len(subset),
                    valid_replicates=len(valid),
                    median_absolute_log_error=float(np.median(errors)),
                    p90_absolute_log_error=float(np.quantile(errors, 0.9)),
                    direction_mismatch_fraction=float(
                        np.mean([r["direction_mismatch"] for r in valid])
                    ),
                )
            )
    save("synthetic_scenario_summary.csv", summaries)
    # Independently calculable invariants for these deliberately constructed signals.
    for r in rows:
        if r["scenario"] in (
            "clean_shared_carrier",
            "common_gain",
            "near_symmetry",
            "exact_symmetry",
        ):
            assert np.isclose(r["observed_ratio"], r["target_ratio"], rtol=1e-10)
        if r["scenario"] == "unequal_pause" and r["method"] == "whole_RMS":
            assert np.isclose(r["observed_ratio"], 0.4)
        if r["scenario"] == "unequal_sensor_gain" and r["method"] == "whole_RMS":
            assert np.isclose(r["observed_ratio"], 1.2)
        if r["scenario"] == "denominator_attenuation" and r["method"] == "whole_RMS":
            assert np.isclose(r["observed_ratio"], 8.0)
        if r["scenario"] == "sustained_true_event" and r["method"] == "whole_RMS":
            assert r["absolute_log_error"] < 1e-12
    methods = list(numerator)
    names = list(scenarios)
    matrix = np.array(
        [
            [
                next(
                    r["median_absolute_log_error"]
                    for r in summaries
                    if r["scenario"] == s and r["method"] == m
                )
                for m in methods
            ]
            for s in names
        ]
    )
    fig, ax = plt.subplots(figsize=(13, 6))
    im = ax.imshow(matrix, aspect="auto", vmin=0, vmax=2.5, cmap="magma")
    ax.set_xticks(range(len(methods)), methods, rotation=65, ha="right", fontsize=8)
    ax.set_yticks(range(len(names)), names, fontsize=9)
    ax.set_title(
        "Synthetic measurement scenarios: median absolute log error\n100 replicates per scenario; constructed reference, not clinical ground truth"
    )
    fig.colorbar(
        im, ax=ax, label="|log(observed / constructed target)| (display capped at 2.5)"
    )
    fig.tight_layout()
    fig.savefig(ROOT / "reports/figures/synthetic_scenario_matrix.png", dpi=160)
    plt.close(fig)
    result = {
        "scenarios": len(names),
        "replicates_per_scenario": 100,
        "methods": len(methods),
        "evaluations": len(rows),
        "invariants_passed": True,
    }
    (ROOT / "reports/synthetic_scenario_checks.json").write_text(
        json.dumps(result, indent=2), encoding="utf-8"
    )
    print(json.dumps(result))


if __name__ == "__main__":
    main()
