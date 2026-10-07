"""Verify pinned Dryad originals; inspect ZIP members without extraction.

Run from any directory: python scripts/inspect_dataset.py
Uses only the standard library. No clinical labels or units are inferred.
"""

import csv
import hashlib
import io
import json
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
REPORTS = ROOT / "reports"
EXPECTED = {
    "ACL_data.zip": (
        11214589,
        "7bac99ea5425cc356f261a641b2123bceeae323039c5a201d0f6cd0f5a1f2a24",
    ),
    "README_acl.txt": (
        3110,
        "de59715a6707972f45ba59e628b7dc85b6f23084eae2e3eb7d6eec89bfbefece",
    ),
}


def verify_originals():
    problems = []
    for name, (size, digest) in EXPECTED.items():
        path = RAW / name
        if not path.is_file():
            problems.append(f"{name}: missing; obtain it from the Dryad dataset page.")
            continue
        contents = path.read_bytes()
        if len(contents) != size or hashlib.sha256(contents).hexdigest() != digest:
            problems.append(f"{name}: size/hash mismatch; do not use as source data.")
    if problems:
        raise ValueError("\n".join(problems))


def describe_text(name, content):
    try:
        text = content.decode("utf-8-sig")
    except UnicodeDecodeError:
        return {"status": "encoding_unresolved"}
    suffix = Path(name).suffix.lower()
    if suffix == ".json":
        try:
            value = json.loads(text)
            return {
                "status": "json",
                "root_type": type(value).__name__,
                "keys": list(value) if isinstance(value, dict) else None,
            }
        except json.JSONDecodeError as exc:
            return {"status": "parse_error", "error": str(exc)}
    if suffix not in {".csv", ".tsv"}:
        return {
            "status": "text_review_required",
            "line_count": len(text.splitlines()),
            "preview": text[:1500],
        }
    reader = csv.reader(io.StringIO(text), delimiter="\t" if suffix == ".tsv" else ",")
    header = next(reader, [])
    counts = [0] * len(header)
    rows = anomalies = blank_rows = 0
    for row in reader:
        if not row:
            blank_rows += 1
            continue
        rows += 1
        anomalies += len(row) != len(header)
        for index, cell in enumerate(row[: len(header)]):
            counts[index] += not cell.strip()
    return {
        "status": "table_structure_only",
        "header": header,
        "rows": rows,
        "blank_rows": blank_rows,
        "row_width_anomalies": anomalies,
        "empty_cells_by_column_position": counts,
        "note": "Units, labels and sentinel missing values require source documentation.",
    }


def main():
    verify_originals()
    inventory, schemas = [], {}
    with zipfile.ZipFile(RAW / "ACL_data.zip") as archive:
        for member in archive.infolist():
            if member.is_dir():
                continue
            contents = archive.read(member)
            inventory.append(
                {
                    "path": member.filename,
                    "bytes": len(contents),
                    "sha256": hashlib.sha256(contents).hexdigest(),
                    "extension": Path(member.filename).suffix.lower(),
                }
            )
            if Path(member.filename).suffix.lower() in {
                ".csv",
                ".tsv",
                ".txt",
                ".md",
                ".json",
            }:
                schemas[member.filename] = describe_text(member.filename, contents)
            else:
                schemas[member.filename] = {"status": "format_specific_reader_required"}
    REPORTS.mkdir(exist_ok=True)
    with (REPORTS / "file_inventory.csv").open(
        "w", encoding="utf-8", newline=""
    ) as out:
        writer = csv.DictWriter(
            out, fieldnames=["path", "bytes", "sha256", "extension"]
        )
        writer.writeheader()
        writer.writerows(inventory)
    (REPORTS / "schema_inventory.json").write_text(
        json.dumps(schemas, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(f"Verified both originals. Inventoried {len(inventory)} archive files.")
    print("Review schema_inventory.json and source README before analytical use.")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, zipfile.BadZipFile, csv.Error) as error:
        print(f"Inspection stopped:\n{error}", file=sys.stderr)
        sys.exit(1)
