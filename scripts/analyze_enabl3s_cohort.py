"""Execute frozen cohort v1; preserve exclusions and undefined specifications."""

import csv
import hashlib
import io
import json
import re
import sys
import zipfile
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.features.amplitude import summarize
from src.features.enabl3s_windows import (
    clean_trial,
    eligible_runs,
    selected_block_indices,
)
from src.features.specifications import specifications

ROOT = Path("data/external/enabl3s")


def canonical(name):
    return Path(name.replace("\\", "/")).stem.removesuffix("_post")


def finite_value(value):
    return float(value) if np.isfinite(value) else None


def metric_row(method, numerator, denominator, audit=None):
    ratio = numerator / denominator if denominator > 0 else np.nan
    reason = None
    if not np.isfinite(numerator) or not np.isfinite(denominator):
        reason = "empty_selection_or_nonfinite_amplitude"
    elif denominator <= 0:
        reason = "nonpositive_denominator"
    elif numerator <= 0:
        reason = "nonpositive_numerator_log_undefined"
    return {
        "method": method,
        "right_export_units": finite_value(numerator),
        "left_export_units": finite_value(denominator),
        "ratio": finite_value(ratio),
        "undefined_reason": reason,
        "selection_audit": audit,
    }


def evaluate(right, left, sizes, factors, shared=False, original=False):
    if original:
        r, left_values = specifications(right), specifications(left)
        rows = [
            metric_row(k, v, left_values[k]) for k, v in r.items() if k.endswith("RMS")
        ]
    else:
        r, left_values = (
            summarize(right, block_sizes=sizes),
            summarize(left, block_sizes=sizes),
        )
        rows = [
            metric_row("whole_RMS", r["rms_V"], left_values["rms_V"]),
            metric_row(
                "cap995_RMS",
                r["rms_cap995_V_sensitivity"],
                left_values["rms_cap995_V_sensitivity"],
            ),
        ]
    for size in sizes:
        count = len(right) // size
        for factor in factors:
            ri, li = selected_block_indices(right, left, size, factor, shared=shared)
            audit = {
                "block_samples": size,
                "complete_blocks": count,
                "tail_samples": len(right) % size,
                "tail_fraction": (len(right) % size) / len(right),
                "right_indices": ri.tolist(),
                "left_indices": li.tolist(),
                "common_indices": np.intersect1d(ri, li).tolist(),
            }
            name = f"block{size}_f{factor}_RMS"
            if original:
                next(row for row in rows if row["method"] == name)[
                    "selection_audit"
                ] = audit
            else:
                values = []
                for signal, indices in ((right, ri), (left, li)):
                    selected = (
                        signal[: count * size].reshape(count, size)[indices].ravel()
                    )
                    values.append(
                        float(np.sqrt(np.mean(selected**2)))
                        if len(selected)
                        else np.nan
                    )
                rows.append(metric_row(name, *values, audit=audit))
    positive = [
        row["ratio"] for row in rows if row["ratio"] is not None and row["ratio"] > 0
    ]
    complete = len(positive) == 11
    result = {
        "status": "complete" if complete else "partial",
        "defined_positive_ratios": len(positive),
        "specifications": rows,
        "log_ratio_range": float(np.ptp(np.log(positive))) if complete else None,
        "partial_log_ratio_range": float(np.ptp(np.log(positive)))
        if positive and not complete
        else None,
        "crosses_one": bool(min(positive) < 1 < max(positive)) if complete else None,
    }
    if len(rows) != 11:
        raise ValueError("Expected exactly eleven RMS specifications")
    return result


def analyze_participant(entry, cfg):
    participant = Path(entry["file"]).stem
    result = {
        "participant": participant,
        "status": "excluded",
        "trial_audit": [],
        "analyses": [],
    }
    path = ROOT / entry["file"]
    with path.open("rb") as source:
        if hashlib.file_digest(source, "sha256").hexdigest() != entry["sha256"]:
            raise ValueError(f"Archive changed: {participant}")
    chosen = None
    with zipfile.ZipFile(path) as archive:
        metadata_name = f"{participant}/{participant}_Metadata.csv"
        with archive.open(metadata_name) as member:
            reader = csv.DictReader(io.TextIOWrapper(member, encoding="utf-8-sig"))
            if not {"Filename", "Notes"}.issubset(reader.fieldnames or []):
                result["reason"] = "missing_metadata_columns"
                return result
            notes = {}
            for row in reader:
                notes.setdefault(canonical(row["Filename"]), []).append(
                    row.get("Notes")
                )
        names = sorted(
            (
                n
                for n in archive.namelist()
                if re.search(r"/Processed/.*Circuit_\d+_post\.csv$", n)
            ),
            key=lambda n: int(re.search(r"Circuit_(\d+)", n)[1]),
        )
        for name in names:
            audit = {"file": name}
            entries = notes.get(canonical(name), [])
            if len(entries) != 1:
                audit.update(
                    reason="missing_or_ambiguous_trial_metadata", notes=entries
                )
                result["trial_audit"].append(audit)
                continue
            audit["notes"] = entries[0]
            if not clean_trial(entries[0]):
                audit["reason"] = "nonempty_or_missing_notes"
                result["trial_audit"].append(audit)
                continue
            with archive.open(name) as member:
                rows = csv.DictReader(io.TextIOWrapper(member, encoding="utf-8-sig"))
                if not {"Mode", "Right_VL", "Left_VL"}.issubset(rows.fieldnames or []):
                    audit["reason"] = "missing_channels_or_mode"
                    result["trial_audit"].append(audit)
                    continue
                values = np.asarray(
                    [
                        (
                            float(row["Mode"]),
                            float(row["Right_VL"]),
                            float(row["Left_VL"]),
                        )
                        for row in rows
                    ],
                    dtype=float,
                )
            if values.ndim != 2 or values.shape[1] != 3:
                audit["reason"] = "empty_signal_file"
                result["trial_audit"].append(audit)
                continue
            runs = eligible_runs(
                *values.T,
                guard=cfg["primary_guard_samples_per_edge"],
                minimum=cfg["minimum_samples_after_guard"],
            )
            if not runs:
                audit["reason"] = "no_contiguous_walk_meeting_guard_and_length"
                result["trial_audit"].append(audit)
                continue
            chosen = runs[0]
            audit.update(reason="selected_first_eligible_run", bounds=chosen)
            result["trial_audit"].append(audit)
            break
        if chosen is None:
            result["reason"] = "no_eligible_trial_or_segment"
            return result
    result.update(
        status="eligible",
        selected_file=name,
        raw_bounds=chosen,
        source_sha256=entry["sha256"],
        units="export units; no physiological scaling or clinical inference asserted",
    )
    result["unassessed_later_trials"] = names[names.index(name) + 1 :]
    for guard in [
        cfg["primary_guard_samples_per_edge"],
        *cfg["sensitivity_guards_samples_per_edge"],
    ]:
        start, stop = chosen["raw_start"] + guard, chosen["raw_stop"] - guard
        for family, sizes in (
            ("original_samples", cfg["primary_block_samples"]),
            ("time_matched", cfg["time_matched_block_samples"]),
        ):
            for shared in (False, True):
                analysis = {
                    "guard_samples": guard,
                    "family": family,
                    "selection": "shared_intersection" if shared else "independent",
                    "start": start,
                    "stop": stop,
                    "samples": max(0, stop - start),
                    "primary": guard == cfg["primary_guard_samples_per_edge"]
                    and family == "original_samples"
                    and not shared,
                }
                if stop - start < cfg["minimum_samples_after_guard"]:
                    analysis.update(
                        status="unavailable",
                        reason="same_raw_run_too_short_after_guard",
                    )
                else:
                    analysis.update(
                        evaluate(
                            values[start:stop, 1],
                            values[start:stop, 2],
                            sizes,
                            cfg["threshold_factors"],
                            shared=shared,
                            original=analysis["primary"],
                        )
                    )
                result["analyses"].append(analysis)
    return result


def main():
    freeze = json.loads(
        Path("reports/enabl3s_cohort_protocol_freeze_v1.json").read_text()
    )
    for name, expected in freeze["files"].items():
        if hashlib.sha256(Path(name).read_bytes()).hexdigest() != expected:
            raise ValueError(f"Frozen protocol changed: {name}")
    cfg = json.loads(Path("config/enabl3s_cohort_v1.json").read_text())
    manifest = json.loads(
        Path("reports/enabl3s_cohort_download_manifest.json").read_text()
    )
    if len(manifest["participants"]) != 9 or any(
        e["participant"] == "AB191" for e in manifest["participants"]
    ):
        raise ValueError("Expected the nine non-pilot participants")
    results = []
    for entry in manifest["participants"]:
        try:
            result = analyze_participant(entry, cfg)
        except (ValueError, KeyError, OSError, zipfile.BadZipFile) as error:
            result = {
                "participant": entry["participant"],
                "status": "not_calculable",
                "reason": str(error),
                "analyses": [],
                "trial_audit": [],
            }
        results.append(result)
        print(f"{result['participant']}: {result['status']}", flush=True)
    primary = [
        (p["participant"], next(a for a in p["analyses"] if a["primary"]))
        for p in results
        if p["status"] == "eligible"
    ]
    complete = [(p, a) for p, a in primary if a["status"] == "complete"]
    ranges = [a["log_ratio_range"] for _, a in complete]
    summary = {
        "participants_expected": 9,
        "eligible": len(primary),
        "complete_primary": len(complete),
        "excluded": sum(p["status"] == "excluded" for p in results),
        "not_calculable": sum(p["status"] == "not_calculable" for p in results),
        "complete_primary_participants": [p for p, _ in complete],
        "primary_log_range_median": float(np.median(ranges)) if ranges else None,
        "primary_log_range_minimum": min(ranges) if ranges else None,
        "primary_log_range_maximum": max(ranges) if ranges else None,
        "primary_crossings_of_one": sum(a["crosses_one"] for _, a in complete),
    }
    report = {
        "run_date": "2026-10-09",
        "source_doi": manifest["source_doi"],
        "source_license": manifest["license"],
        "protocol_freeze": freeze,
        "analysis_script_sha256": hashlib.sha256(
            Path(__file__).read_bytes()
        ).hexdigest(),
        "summary": summary,
        "participants": results,
    }
    Path("reports/enabl3s_cohort_results_v1.json").write_text(
        json.dumps(report, indent=2, allow_nan=False), encoding="utf-8"
    )
    with Path("reports/enabl3s_cohort_primary_v1.csv").open(
        "w", newline="", encoding="utf-8"
    ) as output:
        writer = csv.DictWriter(
            output,
            fieldnames=[
                "participant",
                "status",
                "reason",
                "log_ratio_range",
                "defined_positive_ratios",
                "crosses_one",
            ],
        )
        writer.writeheader()
        for participant in results:
            row = {
                "participant": participant["participant"],
                "status": participant["status"],
                "reason": participant.get("reason", ""),
            }
            if participant["status"] == "eligible":
                analysis = next(a for a in participant["analyses"] if a["primary"])
                row.update(
                    {
                        k: analysis[k]
                        for k in (
                            "log_ratio_range",
                            "defined_positive_ratios",
                            "crosses_one",
                        )
                    }
                )
                row["status"] = analysis["status"]
            writer.writerow(row)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
