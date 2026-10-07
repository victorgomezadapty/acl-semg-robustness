"""Save public Figshare metadata for independent-cohort eligibility inspection."""

import json
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
article_id = sys.argv[1] if len(sys.argv) > 1 else "30928694"
if article_id not in ("30928694", "22139915"):
    raise ValueError("Unapproved research candidate")
out = ROOT / f"data/external/figshare_{article_id}"
out.mkdir(parents=True, exist_ok=True)
req = urllib.request.Request(
    "https://api.figshare.com/v2/articles/" + article_id,
    headers={"User-Agent": "ACL-Research-Portfolio/1.0"},
)
with urllib.request.urlopen(req, timeout=45) as r:
    data = json.load(r)
(out / "metadata.json").write_text(
    json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8"
)
print(
    json.dumps(
        {
            k: data.get(k)
            for k in (
                "id",
                "title",
                "doi",
                "published_date",
                "license",
                "authors",
                "files",
            )
        },
        ensure_ascii=True,
    )
)
