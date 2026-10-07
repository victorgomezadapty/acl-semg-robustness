"""Persist explicit title/abstract relevance decisions from a single reviewer."""

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
folder = ROOT / "data/literature/pubmed_methods_20261006"
with (folder / "records.csv").open(encoding="utf-8") as f:
    records = list(csv.DictReader(f))
core = {
    "14654208": (
        "antecedente_directo",
        "Lesion LCA; normalizacion modifica interpretacion; resumen leido, texto completo no evaluado",
    ),
    "27810649": (
        "antecedente_metodologico",
        "Decisiones de procesamiento sEMG; resumen y secciones editoriales accesibles",
    ),
    "38773029": (
        "antecedente_multiverse",
        "72 pipelines EMG facial; metodos y disponibilidad de datos consultados",
    ),
    "28634449": (
        "antecedente_metodologico",
        "Procesamiento afecta sinergias en marcha; resumen leido",
    ),
    "32569878": (
        "guia_metodologica",
        "CEDE normalizacion; resumen y extractos del manuscrito de autores",
    ),
    "38547715": (
        "guia_metodologica",
        "CEDE reporting; resumen leido; no checklist puntuado",
    ),
    "39069427": (
        "guia_metodologica",
        "CEDE fuerza; resumen/metadatos, no evidencia de equivalencia sEMG-fuerza",
    ),
}
acl = {
    "42817281",
    "42225679",
    "41696949",
    "41843500",
    "37759573",
    "37508839",
    "27532454",
    "24067994",
}
excluded = {
    "42141439": "Deportistas sin cohorte ACLR establecida en resumen",
    "37510918": "Lesion aguda, no reconstruccion",
    "34235227": "Modelo de carga de LCA en atletas, no validacion de asimetria sEMG ACLR",
    "7658940": "Disfuncion LCA sin reconstruccion especificada",
}
rows = []
for r in records:
    pmid = r["pmid"]
    category, reason = core.get(
        pmid,
        (
            "fuera_pregunta",
            "Titulo fuera de poblacion/resultado principal; no revision de eficacia",
        ),
    )
    level = "titulo"
    if pmid in core:
        level = "resumen_y_acceso_indicado_en_motivo"
    elif pmid in acl:
        category, reason, level = (
            "contexto_ACLR",
            "Resumen leido; no compara el protocolo completo de 11 especificaciones RMS",
            "resumen",
        )
    elif pmid in excluded:
        reason = excluded[pmid]
        level = "resumen"
    rows.append(
        {
            **r,
            "relevance": category,
            "decision_reason": reason,
            "reading_level": level,
            "reviewers": 1,
            "independent_duplicate_screening": False,
        }
    )
with (ROOT / "reports/novelty_screening.csv").open(
    "w", encoding="utf-8", newline=""
) as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]))
    w.writeheader()
    w.writerows(rows)
logs = []
for p in folder.glob("*_search.json"):
    d = json.loads(p.read_text())["esearchresult"]
    logs.append(
        {
            "search": p.stem,
            "total_hits": int(d["count"]),
            "warnings": d.get("warninglist", {}),
            "query_translation": d.get("querytranslation"),
        }
    )
(ROOT / "reports/pubmed_search_audit.json").write_text(
    json.dumps(logs, indent=2), encoding="utf-8"
)
print(
    json.dumps(
        {
            "unique_records": len(rows),
            "core_evidence": len(core),
            "ACLR_context": len(acl),
            "title_abstract_only_not_systematic_review": True,
        }
    )
)
