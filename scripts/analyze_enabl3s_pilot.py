"""Apply the frozen RMS pilot to verified ENABL3S processed walking data."""

import csv
import hashlib
import io
import json
import os
import re
import sys
import zipfile
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.features.specifications import specifications


def first_segment(rows):
    start = None
    right, left = [], []
    for index, row in enumerate(rows):
        right_value, left_value = float(row["Right_VL"]), float(row["Left_VL"])
        eligible = (
            float(row["Mode"]) == 1 and np.isfinite([right_value, left_value]).all()
        )
        if eligible:
            if start is None:
                start = index
            right.append(right_value)
            left.append(left_value)
        else:
            if len(right) >= 2048:
                return start, index, np.asarray(right), np.asarray(left)
            start, right, left = None, [], []
    if len(right) >= 2048:
        return start, start + len(right), np.asarray(right), np.asarray(left)
    return None


def main():
    inventory = json.loads(Path("reports/enabl3s_pilot_inventory.json").read_text())
    if not inventory["md5_verified"]:
        raise ValueError("A verified source inventory is required.")
    archive_path = Path("data/external/enabl3s/AB191.zip")
    if archive_path.stat().st_size != inventory["bytes"]:
        raise ValueError("Archive size changed after verification.")
    with archive_path.open("rb") as source:
        if hashlib.file_digest(source, "sha256").hexdigest() != inventory["sha256"]:
            raise ValueError("Archive hash changed after verification.")
    with zipfile.ZipFile(archive_path) as archive:
        names = sorted(
            (
                n
                for n in archive.namelist()
                if re.search(r"/Processed/.*_post\.csv$", n)
            ),
            key=lambda n: int(re.search(r"Circuit_(\d+)", n)[1]),
        )
        excluded = []
        selected = None
        for name in names:
            with archive.open(name) as member:
                rows = csv.DictReader(io.TextIOWrapper(member, encoding="utf-8-sig"))
                if not {"Right_VL", "Left_VL", "Mode"}.issubset(rows.fieldnames):
                    raise ValueError(f"Ambiguous channels or task: {name}")
                selected = first_segment(rows)
            if selected is not None:
                break
            excluded.append(name)
        if selected is None:
            raise ValueError("No eligible segment; participant excluded.")
        notes = None
        with archive.open("AB191/AB191_Metadata.csv") as member:
            for row in csv.DictReader(io.TextIOWrapper(member, encoding="utf-8-sig")):
                if Path(row["Filename"]).stem.removesuffix("_post") == Path(
                    name
                ).stem.removesuffix("_post"):
                    notes = row["Notes"]
    start, stop, right, left = selected
    right_specs, left_specs = specifications(right), specifications(left)
    results = []
    for method, numerator in right_specs.items():
        if not method.endswith("RMS"):
            continue
        denominator = left_specs[method]
        ratio = numerator / denominator if denominator > 0 else float("nan")
        results.append(
            {
                "method": method,
                "right_export_units": numerator if np.isfinite(numerator) else None,
                "left_export_units": denominator if np.isfinite(denominator) else None,
                "right_left_ratio": ratio if np.isfinite(ratio) else None,
            }
        )
    ratios = np.asarray([r["right_left_ratio"] for r in results], dtype=float)
    finite = ratios[np.isfinite(ratios) & (ratios > 0)]
    selection_audit = []
    for size in (256, 512, 1024):
        block_count = len(right) // size
        right_rms = np.sqrt(
            np.mean(right[: block_count * size].reshape(-1, size) ** 2, axis=1)
        )
        left_rms = np.sqrt(
            np.mean(left[: block_count * size].reshape(-1, size) ** 2, axis=1)
        )
        for factor in (0.1, 0.2, 0.3):
            selections = []
            for amplitudes in (right_rms, left_rms):
                low, high = np.quantile(amplitudes, [0.2, 0.9])
                selections.append(
                    np.flatnonzero(amplitudes > low + factor * (high - low)).tolist()
                )
            selection_audit.append(
                {
                    "block_samples": size,
                    "threshold_factor": factor,
                    "complete_blocks": block_count,
                    "discarded_tail_samples": len(right) % size,
                    "right_selected_indices": selections[0],
                    "left_selected_indices": selections[1],
                    "common_selected_indices": sorted(
                        set(selections[0]) & set(selections[1])
                    ),
                }
            )
    report = {
        "protocol": "docs/history/enabl3s_transport_protocol.md",
        "source_doi": inventory["source_doi"],
        "source_sha256": inventory["sha256"],
        "population": "Healthy adults; one pilot participant; no ACL clinical validation",
        "participant": "AB191",
        "signal_file": name,
        "signal_representation": "Source postprocessed export; no additional filtering",
        "units": "Export units; no conversion to volts asserted",
        "sample_rate_Hz_from_publication": 1000,
        "segment_start_zero_based_inclusive": start,
        "segment_stop_zero_based_exclusive": stop,
        "samples": len(right),
        "duration_seconds_at_documented_rate": len(right) / 1000,
        "earlier_ineligible_files": excluded,
        "source_trial_notes": notes,
        "defined_RMS_specifications": len(finite),
        "minimum_ratio": float(finite.min()) if len(finite) else None,
        "maximum_ratio": float(finite.max()) if len(finite) else None,
        "log_ratio_range": float(np.ptp(np.log(finite))) if len(finite) else None,
        "crosses_one": bool(finite.min() < 1 < finite.max()) if len(finite) else None,
        "specifications": results,
        "block_selection_audit": selection_audit,
    }
    if len(results) != 11:
        raise ValueError("Frozen analysis must contain exactly 11 RMS specifications.")
    destination = Path("reports/enabl3s_pilot_results.json")
    destination.write_text(
        json.dumps(report, indent=2, allow_nan=False), encoding="utf-8"
    )
    os.environ.setdefault("MPLCONFIGDIR", str(Path(".mpl-cache").resolve()))
    import matplotlib.pyplot as plt

    figure, axis = plt.subplots(figsize=(9, 6))
    axis.scatter(ratios, np.arange(len(results)), color="#245b78", zorder=3)
    axis.set_yticks(np.arange(len(results)), [r["method"] for r in results])
    axis.invert_yaxis()
    axis.axvline(
        1, color="#999999", linestyle="--", label="Ratio 1 (descriptive reference)"
    )
    axis.set_xscale("log")
    axis.set_xlabel("Right/left VL amplitude ratio (log axis)")
    axis.set_title(
        "ENABL3S AB191: one 2.85 s walking segment\nPilot only; source trial has a late-transition annotation"
    )
    axis.grid(axis="x", alpha=0.2)
    axis.legend(loc="lower right", fontsize=8)
    figure.text(
        0.02,
        0.015,
        "Source: Hu, Rouse & Hargrove, ENABL3S v2 (CC BY 4.0). No clinical inference.",
        fontsize=8,
    )
    figure.tight_layout(rect=(0, 0.04, 1, 1))
    figure_directory = Path("reports/figures")
    figure_directory.mkdir(parents=True, exist_ok=True)
    figure.savefig(figure_directory / "enabl3s_pilot.png", dpi=180)
    figure.savefig(figure_directory / "enabl3s_pilot.svg")
    plt.close(figure)
    print(json.dumps(report, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
