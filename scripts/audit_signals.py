"""Read every numeric cell; report availability and temporal structure, no cleaning."""

import csv
import io
import json
import math
import statistics
import zipfile

from inspect_dataset import RAW, REPORTS, verify_originals


def main():
    verify_originals()
    records, clocks = [], {}
    with zipfile.ZipFile(RAW / "ACL_data.zip") as archive:
        for name in sorted(archive.namelist()):
            if name.endswith("_time.csv"):
                rows = list(
                    csv.reader(io.StringIO(archive.read(name).decode("utf-8-sig")))
                )
                times = [float(row[0]) for row in rows[1:]]
                differences = [b - a for a, b in zip(times, times[1:])]
                median = statistics.median(differences)
                clocks[name] = {
                    "samples": len(times),
                    "start_s": times[0],
                    "end_s": times[-1],
                    "median_dt_s": median,
                    "min_dt_s": min(differences),
                    "max_dt_s": max(differences),
                    "nonpositive_steps": sum(d <= 0 for d in differences),
                    "nonfinite_times": sum(not math.isfinite(t) for t in times),
                    "implied_sample_rate_hz": 1 / median if median > 0 else None,
                    "average_sample_rate_hz": (len(times) - 1) / (times[-1] - times[0]),
                    "duplicate_steps": sum(d == 0 for d in differences),
                    "negative_steps": sum(d < 0 for d in differences),
                    "distinct_dt_s_rounded": sorted({round(d, 8) for d in differences}),
                }
        for name in sorted(archive.namelist()):
            if not name.endswith(".csv") or name.endswith("_time.csv"):
                continue
            rows = list(csv.reader(io.StringIO(archive.read(name).decode("utf-8-sig"))))
            cohort, condition, limb = name.removesuffix(".csv").split("_")
            time_name = name.removesuffix(".csv") + "_time.csv"
            times = [
                float(row[0])
                for row in list(
                    csv.reader(io.StringIO(archive.read(time_name).decode("utf-8-sig")))
                )[1:]
            ]
            for index, participant in enumerate(rows[0]):
                values, positions, invalid = [], [], 0
                for position, row in enumerate(rows[1:]):
                    if not row[index].strip():
                        continue
                    try:
                        value = float(row[index])
                    except ValueError:
                        invalid += 1
                        continue
                    values.append(value)
                    positions.append(position)
                first, last = positions[0], positions[-1]
                records.append(
                    {
                        "file": name,
                        "participant_id": participant,
                        "cohort": cohort,
                        "condition": condition,
                        "limb_label": limb,
                        "samples": len(values),
                        "empty_cells": len(rows) - 1 - len(values) - invalid,
                        "internal_empty_cells": last
                        - first
                        + 1
                        - len(values)
                        - invalid,
                        "leading_empty_cells": first,
                        "trailing_empty_cells": len(rows) - 2 - last,
                        "invalid_numeric_cells": invalid,
                        "nonfinite_values": sum(not math.isfinite(v) for v in values),
                        "start_s": times[first],
                        "end_s": times[last],
                        "elapsed_s": times[last] - times[first],
                        "min_V": min(values),
                        "max_V": max(values),
                        "zero_values": sum(v == 0 for v in values),
                        "time_rows_match": len(times) == len(rows) - 1,
                    }
                )
    with (REPORTS / "signal_availability.csv").open(
        "w", encoding="utf-8", newline=""
    ) as out:
        writer = csv.DictWriter(out, fieldnames=list(records[0]))
        writer.writeheader()
        writer.writerows(records)
    (REPORTS / "time_audit.json").write_text(
        json.dumps(clocks, indent=2), encoding="utf-8"
    )
    summary = {
        "recordings": len(records),
        "participants": len({r["participant_id"] for r in records}),
        "sample_range": [
            min(r["samples"] for r in records),
            max(r["samples"] for r in records),
        ],
        "elapsed_s_range": [
            min(r["elapsed_s"] for r in records),
            max(r["elapsed_s"] for r in records),
        ],
        "internal_empty_cells": sum(r["internal_empty_cells"] for r in records),
        "leading_empty_cells": sum(r["leading_empty_cells"] for r in records),
        "invalid_numeric_cells": sum(r["invalid_numeric_cells"] for r in records),
        "nonfinite_values": sum(r["nonfinite_values"] for r in records),
        "all_time_rows_match": all(r["time_rows_match"] for r in records),
    }
    (REPORTS / "audit_summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )
    print(json.dumps(summary, indent=2))
    print(json.dumps(clocks, indent=2))


if __name__ == "__main__":
    main()
