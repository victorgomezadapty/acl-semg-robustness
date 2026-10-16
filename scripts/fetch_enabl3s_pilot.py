"""Fetch a fixed external pilot and inventory it without opening signal values."""

import hashlib
import json
import urllib.request
import zipfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path


def main():
    root = Path("data/external/enabl3s")
    root.mkdir(parents=True, exist_ok=True)
    metadata_path = root / "metadata.json"
    if not metadata_path.exists():
        with urllib.request.urlopen(
            "https://api.figshare.com/v2/articles/5362627/versions/2", timeout=45
        ) as response:
            metadata_path.write_bytes(response.read())
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    if metadata["version"] != 2:
        raise ValueError("This protocol requires ENABL3S version 2.")
    entry = next(f for f in metadata["files"] if f["name"] == "AB191.zip")
    target = root / entry["name"]
    if not target.exists():
        partial = target.with_suffix(".zip.part")
        offset = partial.stat().st_size if partial.exists() else 0
        chunk_size = 20 * 1024 * 1024
        ranges = [
            (start, min(start + chunk_size, entry["size"]) - 1)
            for start in range(offset, entry["size"], chunk_size)
        ]

        def fetch(bounds):
            start, stop = bounds
            chunk_path = root / f"AB191.range-{start}-{stop}"
            if chunk_path.exists() and chunk_path.stat().st_size == stop - start + 1:
                return chunk_path
            request = urllib.request.Request(
                entry["download_url"], headers={"Range": f"bytes={start}-{stop}"}
            )
            with urllib.request.urlopen(request, timeout=120) as response:
                if (
                    response.status != 206
                    or response.headers.get("Content-Range")
                    != f"bytes {start}-{stop}/{entry['size']}"
                ):
                    raise ValueError("Server did not honor the requested byte range.")
                with chunk_path.open("wb") as output:
                    while chunk := response.read(1024 * 1024):
                        output.write(chunk)
            if chunk_path.stat().st_size != stop - start + 1:
                raise ValueError("Incomplete range; rerun to retry.")
            print(f"Downloaded bytes {start}-{stop}", flush=True)
            return chunk_path

        with ThreadPoolExecutor(max_workers=8) as pool:
            chunks = list(pool.map(fetch, ranges))
        with partial.open("ab") as output:
            for chunk_path in chunks:
                with chunk_path.open("rb") as source:
                    while chunk := source.read(1024 * 1024):
                        output.write(chunk)
        partial.rename(target)
    md5 = hashlib.md5()
    sha = hashlib.sha256()
    with target.open("rb") as source:
        while chunk := source.read(1024 * 1024):
            md5.update(chunk)
            sha.update(chunk)
    if (
        target.stat().st_size != entry["size"]
        or md5.hexdigest() != entry["computed_md5"]
    ):
        raise ValueError("Source size or MD5 mismatch; do not analyze this archive.")
    with zipfile.ZipFile(target) as archive:
        members = [
            {"name": m.filename, "bytes": m.file_size} for m in archive.infolist()
        ]
    report = {
        "source_doi": metadata["doi"],
        "license": metadata["license"],
        "pilot_selection": "Smallest participant ZIP by metadata, before signal inspection",
        "participant": "AB191",
        "bytes": target.stat().st_size,
        "md5_verified": True,
        "sha256": sha.hexdigest(),
        "members": members,
    }
    destination = Path("reports/enabl3s_pilot_inventory.json")
    destination.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps({k: v for k, v in report.items() if k != "members"}, indent=2))
    print(f"Inventory: {len(members)} members; {destination}")


if __name__ == "__main__":
    main()
