"""Download and verify the nine fixed ENABL3S participants, without signal analysis."""

import hashlib
import json
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path("data/external/enabl3s")


def fetch_archive(entry):
    target = ROOT / entry["name"]
    stem = target.stem
    chunks = []
    if not target.exists():
        size = 20 * 1024 * 1024
        bounds = [
            (s, min(s + size, entry["size"]) - 1) for s in range(0, entry["size"], size)
        ]

        def fetch(part):
            start, stop = part
            path = ROOT / f"{stem}.cohort-range-{start}-{stop}"
            expected = stop - start + 1
            if path.exists() and path.stat().st_size == expected:
                return path
            for attempt in range(3):
                try:
                    request = urllib.request.Request(
                        entry["download_url"],
                        headers={"Range": f"bytes={start}-{stop}"},
                    )
                    with urllib.request.urlopen(request, timeout=120) as response:
                        if (
                            response.status != 206
                            or response.headers.get("Content-Range")
                            != f"bytes {start}-{stop}/{entry['size']}"
                        ):
                            raise ValueError("Unexpected byte range response")
                        with path.open("wb") as output:
                            while block := response.read(1024 * 1024):
                                output.write(block)
                    if path.stat().st_size != expected:
                        raise ValueError("Incomplete byte range")
                    return path
                except Exception:
                    if attempt == 2:
                        raise
                    time.sleep(2 * (attempt + 1))

        with ThreadPoolExecutor(max_workers=8) as pool:
            chunks = list(pool.map(fetch, bounds))
        partial = target.with_suffix(".cohort-part")
        with partial.open("wb") as output:
            for path in chunks:
                with path.open("rb") as source:
                    while block := source.read(1024 * 1024):
                        output.write(block)
        partial.rename(target)
    with target.open("rb") as source:
        md5 = hashlib.file_digest(source, "md5").hexdigest()
    if target.stat().st_size != entry["size"] or md5 != entry["computed_md5"]:
        raise ValueError(f"Integrity mismatch: {stem}")
    with target.open("rb") as source:
        sha = hashlib.file_digest(source, "sha256").hexdigest()
    for path in chunks:
        if path.resolve().parent != ROOT.resolve():
            raise ValueError("Unsafe temporary file path")
        path.unlink()
    result = {
        "participant": stem,
        "file": entry["name"],
        "bytes": entry["size"],
        "md5": md5,
        "sha256": sha,
        "verified": True,
    }
    (ROOT / f"{stem}.verified.json").write_text(
        json.dumps(result, indent=2), encoding="utf-8"
    )
    print(f"Verified {stem}: {entry['size']} bytes", flush=True)
    return result


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    metadata_path = ROOT / "metadata.json"
    if not metadata_path.exists():
        with urllib.request.urlopen(
            "https://api.figshare.com/v2/articles/5362627/versions/2", timeout=45
        ) as response:
            metadata_path.write_bytes(response.read())
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    if metadata["version"] != 2:
        raise ValueError("ENABL3S v2 is required")
    entries = sorted(
        (
            e
            for e in metadata["files"]
            if e["name"].endswith(".zip") and e["name"] != "AB191.zip"
        ),
        key=lambda e: e["name"],
    )
    if len(entries) != 9:
        raise ValueError("Expected exactly nine non-pilot participants")
    with ThreadPoolExecutor(max_workers=2) as pool:
        records = list(pool.map(fetch_archive, entries))
    report = {
        "source_doi": metadata["doi"],
        "license": metadata["license"],
        "participants": records,
    }
    Path("reports/enabl3s_cohort_download_manifest.json").write_text(
        json.dumps(report, indent=2), encoding="utf-8"
    )
    print("All nine archives verified", flush=True)


if __name__ == "__main__":
    main()
