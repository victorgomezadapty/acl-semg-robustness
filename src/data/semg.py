"""Verified ZIP loader: retain exported signal and time; remove trailing padding only."""

import csv
import hashlib
import io
import zipfile
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
ARCHIVE_HASH = "7bac99ea5425cc356f261a641b2123bceeae323039c5a201d0f6cd0f5a1f2a24"


def recordings(path=None, expected_hash=ARCHIVE_HASH):
    path = Path(path) if path else ROOT / "data/raw/ACL_data.zip"
    if hashlib.sha256(path.read_bytes()).hexdigest() != expected_hash:
        raise ValueError("Archive does not match pinned Dryad version.")
    with zipfile.ZipFile(path) as archive:
        for name in sorted(archive.namelist()):
            if not name.endswith(".csv") or name.endswith("_time.csv"):
                continue
            rows = list(csv.reader(io.StringIO(archive.read(name).decode("utf-8-sig"))))
            header, body = rows[0], rows[1:]
            time_name = name[:-4] + "_time.csv"
            time_rows = list(
                csv.reader(io.StringIO(archive.read(time_name).decode("utf-8-sig")))
            )
            times = np.array([float(row[0]) for row in time_rows[1:]])
            if len(times) != len(body) or not np.isfinite(times).all():
                raise ValueError(f"{name}: invalid paired clock")
            cohort, condition, limb = name[:-4].split("_")
            for col, participant in enumerate(header):
                if any(row and len(row) != len(header) for row in body):
                    raise ValueError(f"{name}: inconsistent signal columns")
                cells = [row[col].strip() if row else "" for row in body]
                n = len(cells)
                while n and not cells[n - 1]:
                    n -= 1
                if not n or any(not cell for cell in cells[:n]):
                    raise ValueError(
                        f"{name}/{participant}: empty signal or internal gap"
                    )
                signal = np.array([float(cell) for cell in cells[:n]])
                if not np.isfinite(signal).all():
                    raise ValueError(f"{name}/{participant}: nonfinite sEMG")
                yield {
                    "source_file": name,
                    "participant_id": participant,
                    "cohort": cohort,
                    "condition": condition,
                    "limb_label": limb,
                    "sample_index": np.arange(n),
                    "time_exported_s": times[:n].copy(),
                    "semg_V": signal,
                    "padding_removed": len(cells) - n,
                }


def long_rows(path=None):
    """Stream tidy rows without duplicating multi-million-row storage."""
    for record in recordings(path):
        metadata = {
            key: record[key]
            for key in [
                "source_file",
                "participant_id",
                "cohort",
                "condition",
                "limb_label",
            ]
        }
        for index, (time, value) in enumerate(
            zip(record["time_exported_s"], record["semg_V"])
        ):
            yield {
                **metadata,
                "sample_index": index,
                "time_exported_s": float(time),
                "semg_V": float(value),
            }
