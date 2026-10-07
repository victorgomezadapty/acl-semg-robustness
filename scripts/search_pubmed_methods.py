"""Reproducible focused PubMed searches; not an exhaustive systematic review."""

import csv
import json
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
out = ROOT / "data/literature/pubmed_methods_20261006"
out.mkdir(parents=True, exist_ok=True)
queries = {
    "ACL_methods": '("anterior cruciate ligament"[Title/Abstract] OR ACLR[Title/Abstract]) AND (electromyograph*[Title/Abstract] OR EMG[Title/Abstract] OR sEMG[Title/Abstract]) AND (symmetr*[Title/Abstract] OR asymmetr*[Title/Abstract]) AND (normaliz*[Title/Abstract] OR normalis*[Title/Abstract] OR process*[Title/Abstract] OR reliab*[Title/Abstract] OR sensitiv*[Title/Abstract])',
    "EMG_multiverse": '(electromyograph*[Title/Abstract] OR EMG[Title/Abstract] OR sEMG[Title/Abstract]) AND (multiverse[Title/Abstract] OR "specification curve"[Title/Abstract] OR "processing pipeline"[Title/Abstract])',
    "EMG_processing": '(electromyograph*[Title/Abstract] OR EMG[Title/Abstract] OR sEMG[Title/Abstract]) AND (normaliz*[Title/Abstract] OR normalis*[Title/Abstract]) AND ("clinical interpretation"[Title/Abstract] OR "processing choices"[Title/Abstract] OR "data-driven approach"[Title/Abstract])',
    "EMG_CEDE": '"Consensus for experimental design in electromyography"[Title]',
    "EMG_CEDE_revised": "CEDE[Title/Abstract] AND electromyograph*[Title/Abstract]",
}


def get(endpoint, args):
    url = (
        "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
        + endpoint
        + "?"
        + urllib.parse.urlencode(args)
    )
    with urllib.request.urlopen(
        urllib.request.Request(url, headers={"User-Agent": "ACL-Methods-Review/1.0"}),
        timeout=45,
    ) as r:
        return r.read()


records = {}
logs = []
for name, query in queries.items():
    blob = get(
        "esearch.fcgi",
        {
            "db": "pubmed",
            "term": query,
            "retmode": "json",
            "retmax": 200,
            "sort": "pub_date",
        },
    )
    (out / (name + "_search.json")).write_bytes(blob)
    data = json.loads(blob)["esearchresult"]
    ids = data["idlist"]
    logs.append(
        {
            "date_utc": datetime.now(timezone.utc).isoformat(),
            "database": "PubMed",
            "search_id": name,
            "query": query,
            "total_hits": int(data["count"]),
            "retrieved": len(ids),
            "retmax": 200,
            "filters": "none",
        }
    )
    time.sleep(0.4)
    if not ids:
        continue
    xml = get("efetch.fcgi", {"db": "pubmed", "id": ",".join(ids), "retmode": "xml"})
    (out / (name + "_records.xml")).write_bytes(xml)
    for article in ET.fromstring(xml).findall("PubmedArticle"):
        pmid = article.findtext("./MedlineCitation/PMID")
        a = article.find("./MedlineCitation/Article")
        title = "".join(a.find("ArticleTitle").itertext())
        doi = next(
            (
                n.text
                for n in article.findall("./PubmedData/ArticleIdList/ArticleId")
                if n.get("IdType") == "doi"
            ),
            "",
        )
        publication_types = "; ".join(
            n.text or "" for n in a.findall("./PublicationTypeList/PublicationType")
        )
        comments = "; ".join(
            (n.get("RefType", "") + ":" + (n.findtext("PMID") or ""))
            for n in article.findall(
                "./MedlineCitation/CommentsCorrectionsList/CommentsCorrections"
            )
        )
        if pmid in records:
            records[pmid]["search_ids"] += ";" + name
        else:
            records[pmid] = {
                "pmid": pmid,
                "title": title,
                "doi": doi,
                "journal": a.findtext("./Journal/Title"),
                "publication_types": publication_types,
                "linked_notices": comments,
                "search_ids": name,
                "url": "https://pubmed.ncbi.nlm.nih.gov/" + pmid + "/",
            }
    time.sleep(0.4)
for filename, rows in [
    ("search_log.csv", logs),
    ("records.csv", list(records.values())),
]:
    if rows:
        with (out / filename).open("w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0]))
            w.writeheader()
            w.writerows(rows)
print(json.dumps({"searches": logs, "unique_records": len(records)}, ensure_ascii=True))
