"""Download named files from pinned saved metadata; verify MD5 and retain SHA256."""

import hashlib
import json
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
article_id = sys.argv[1] if len(sys.argv) > 1 else "30928694"
if article_id not in ("30928694", "22139915"):
    raise ValueError("Unapproved research candidate")
out = ROOT / f"data/external/figshare_{article_id}"
data = json.loads((out / "metadata.json").read_text(encoding="utf-8"))
rows = []
for entry in data["files"]:
    name = entry["name"]
    if Path(name).name != name:
        raise ValueError("Unexpected filename")
    req = urllib.request.Request(
        entry["download_url"], headers={"User-Agent": "ACL-Research-Portfolio/1.0"}
    )
    with urllib.request.urlopen(req, timeout=45) as response:
        blob = response.read()
    digest = hashlib.md5(blob).hexdigest()
    if digest != entry["computed_md5"] or len(blob) != entry["size"]:
        raise ValueError("Source verification failed")
    (out / name).write_bytes(blob)
    rows.append(
        {
            "name": name,
            "bytes": len(blob),
            "md5": digest,
            "sha256": hashlib.sha256(blob).hexdigest(),
            "url": entry["download_url"],
            "license": "CC BY 4.0",
            "doi": data["doi"],
        }
    )
(out / "download_manifest.json").write_text(
    json.dumps(rows, indent=2), encoding="utf-8"
)
print(
    json.dumps(
        {
            "files": len(rows),
            "bytes": sum(r["bytes"] for r in rows),
            "all_md5_verified": True,
        }
    )
)
