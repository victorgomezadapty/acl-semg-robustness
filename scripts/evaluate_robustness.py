"""Retrospective specification sensitivity, not a clinical reliability score."""

import csv
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
os.environ.setdefault("MPLCONFIGDIR", str(ROOT / ".mpl-cache"))
import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from src.features.quality import excluded_pairs
from src.features.specifications import specifications


def read(path):
    with (ROOT / path).open(encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def write(path, rows):
    with (ROOT / path).open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


def synthetic():
    rng = np.random.default_rng(20261006)
    base = rng.normal(size=32768)
    inv = 0.8 * base
    uninv = base.copy()
    cases = {
        "clean": (inv, uninv),
        "common_gain": (inv * 7, uninv * 7),
        "unequal_pause": (np.r_[inv, np.zeros(98304)], uninv),
        "transient": (inv.copy(), uninv.copy()),
        "small_denominator": (inv, uninv * 0.01),
    }
    cases["transient"][0][100] = 200
    rows = []
    for name, (a, b) in cases.items():
        va, vb = specifications(a), specifications(b)
        for spec in va:
            ratio = va[spec] / vb[spec] if vb[spec] > 0 else np.nan
            rows.append(
                {
                    "scenario": name,
                    "specification": spec,
                    "exported_ratio": ratio,
                    "underlying_active_ratio_before_perturbation": 0.8,
                }
            )
    lookup = {(r["scenario"], r["specification"]): r["exported_ratio"] for r in rows}
    for spec in specifications(base):
        assert np.isclose(lookup["clean", spec], 0.8)
        assert np.isclose(lookup["common_gain", spec], lookup["clean", spec])
    assert np.isclose(lookup["unequal_pause", "whole_RMS"], 0.4)
    assert lookup["transient", "whole_RMS"] > 1
    assert lookup["transient", "cap995_RMS"] < 1
    assert np.isclose(lookup["small_denominator", "whole_RMS"], 80)
    return rows


def main():
    features = read("data/processed/semg_extended_features.csv")
    blocks = read("reports/block_selection_sensitivity.csv")
    excluded = excluded_pairs(features)
    grouped = {}
    for r in features:
        key = (r["participant_id"], r["cohort"], r["condition"])
        grouped.setdefault(key, {})[r["limb_label"]] = {
            "whole_RMS": float(r["rms_V"]),
            "whole_MAV": float(r["mav_V"]),
            "cap995_RMS": float(r["rms_cap995_V_sensitivity"]),
        }
    for r in blocks:
        key = (r["participant_id"], r["cohort"], r["condition"])
        for metric in ("RMS", "MAV"):
            spec = (
                f"block{r['block_samples']}_f{float(r['threshold_fraction'])}_{metric}"
            )
            grouped[key][r["limb_label"]][spec] = float(
                r[f"selected_{metric.lower()}_V"]
            )
    rows = []
    summaries = []
    matrix = []
    labels = []
    names = list(next(iter(grouped.values()))["inv"])
    for key, limbs in sorted(grouped.items()):
        person, cohort, condition = key
        logs = []
        for spec in names:
            a, b = limbs["inv"][spec], limbs["uninv"][spec]
            value = np.log(a / b) if a > 0 and b > 0 else np.nan
            logs.append(value)
            rows.append(
                {
                    "participant_id": person,
                    "cohort": cohort,
                    "condition": condition,
                    "specification": spec,
                    "inv_V": a,
                    "uninv_V": b,
                    "log_ratio": value,
                    "ratio_pct": float(np.exp(value) * 100),
                }
            )
        logs = np.array(logs)
        valid = logs[np.isfinite(logs)]
        reference = logs[0]
        crosses = bool(np.any(valid < 0) and np.any(valid > 0))
        summaries.append(
            {
                "participant_id": person,
                "cohort": cohort,
                "condition": condition,
                "valid_specifications": len(valid),
                "whole_rms_ratio_pct": np.exp(reference) * 100,
                "min_ratio_pct": np.exp(valid.min()) * 100,
                "max_ratio_pct": np.exp(valid.max()) * 100,
                "min_log_ratio": float(valid.min()),
                "max_log_ratio": float(valid.max()),
                "log_ratio_range": float(valid.max() - valid.min()),
                "direction_changes_across_specifications": crosses,
                "max_absolute_log_change_from_whole_rms": max(abs(valid - reference)),
                "primary_pair": (person, condition) not in excluded,
            }
        )
        matrix.append(logs)
        labels.append(
            f"{person} / {condition}"
            + (" (excluded: short record)" if (person, condition) in excluded else "")
        )
    assert len(rows) == 924 and len(summaries) == 44
    write("reports/robustness_specifications.csv", rows)
    write("reports/robustness_participant_summary.csv", summaries)
    synthetic_rows = synthetic()
    write("reports/robustness_synthetic_checks.csv", synthetic_rows)
    changed = sum(r["direction_changes_across_specifications"] for r in summaries)
    people = len(
        {
            r["participant_id"]
            for r in summaries
            if r["direction_changes_across_specifications"]
        }
    )
    rms_columns = [i for i, n in enumerate(names) if n.endswith("RMS")]
    rms_changed = sum(
        np.any(np.array(v)[rms_columns] < 0) and np.any(np.array(v)[rms_columns] > 0)
        for v in matrix
    )
    primary = [r for r in summaries if r["primary_pair"]]
    primary_changed = sum(r["direction_changes_across_specifications"] for r in primary)
    primary_rms_changed = sum(
        np.any(np.array(v)[rms_columns] < 0) and np.any(np.array(v)[rms_columns] > 0)
        for v, r in zip(matrix, summaries)
        if r["primary_pair"]
    )
    fig, ax = plt.subplots(figsize=(14, 13))
    im = ax.imshow(matrix, aspect="auto", cmap="RdBu_r", vmin=-1.5, vmax=1.5)
    ax.set_yticks(range(44), labels, fontsize=8)
    ax.set_xticks(range(len(names)), names, rotation=65, ha="right", fontsize=8)
    ax.set_title(
        "Specification sensitivity of exported sEMG asymmetry\n"
        "Red: inv > uninv; blue: inv < uninv. Not a clinical score."
    )
    fig.colorbar(im, ax=ax, label="log(inv/uninv); display clipped at ±1.5")
    fig.tight_layout()
    fig.savefig(ROOT / "reports/figures/robustness_matrix.png", dpi=150)
    plt.close(fig)
    content = f"""# Aportación evaluada: sensibilidad de la interpretación

Evaluación retrospectiva · 2026-10-06. No es un descubrimiento clínico ni se afirma prioridad científica.

## Resultado principal

De 44 pares participante-condición, **{changed} ({changed / 44:.1%}) cambian de dirección** entre las 21 especificaciones de amplitud. Corresponden a {people} de 22 personas; cada persona puede aportar dos condiciones. Cambiar de dirección significa que unas especificaciones dan inv/uninv <1 y otras >1. Diferencias muy pequeñas también cuentan: no implica un cambio clínicamente relevante.

Esto demuestra información adicional al RMS único: identifica interpretaciones dependientes de cómo se resume la señal. No demuestra cuál especificación es fisiológicamente correcta. Las 21 variantes no son réplicas independientes ni votos con probabilidad clínica. RMS y MAV son estimandos diferentes; se agrupan aquí para mostrar dependencia de la interpretación, no para estimar error de medición del mismo estimando.

Clasificación de validez (2026-10-07): {44 - len(primary)} par(es) quedan fuera de la presentación principal porque un miembro dura menos del 25% de la mediana de su cohorte-condición; con los {len(primary)} pares válidos, {primary_changed} cambian de dirección (21 variantes) y {primary_rms_changed} con las 11 variantes RMS. Los 44 se conservan como sensibilidad.

Si se restringe la comparación a las 11 variantes RMS (registro completo, límite de picos y nueve selecciones de bloques), {rms_changed} pares cambian de dirección. Los bloques seleccionados siguen midiendo subconjuntos diferentes del registro.

Ejemplos auditables: healthy1/iso180 abarca aproximadamente 79,5–107,7% entre especificaciones; patient2/iso180, 83,6–106,0%. En cambio, patient6/iso90 abarca 99,6–108,7%: cruzar 100% por sí solo no indica una diferencia sustancial. Los valores no describen fuerza muscular recuperada.

![Matriz de especificaciones](../../reports/figures/robustness_matrix.png)

## Evaluación con perturbaciones conocidas

Se generó una señal aleatoria con semilla fija y una copia de amplitud 0,8. Las 21 especificaciones recuperan 0,8 y conservan el cociente bajo ganancia común ×7. Añadir reposo exclusivamente a inv cambia el RMS total a 0,4 sin cambiar la amplitud activa subyacente. Un transitorio artificial invierte la dirección del RMS; la sensibilidad al límite p99,5 mantiene la dirección original. Reducir el denominador ×0,01 produce cociente 80: el análisis lo expone, pero no lo corrige automáticamente ni diagnostica su causa.

Estas comprobaciones pasaron por assertions y prueban propiedades matemáticas de casos construidos. No validan segmentación, artefactos reales, fuerza ni recuperación. Los bloques se seleccionan por separado en cada miembro, sin sincronización fisiológica.

## Protocolo y utilidad demostrada

La formalización PICOTT posterior fija el rango logarítmico entre las 11 variantes RMS como resultado principal de la evaluación externa propuesta. El rango de las 21 variantes aquí exportado corresponde al desarrollo retrospectivo; no se presenta como análisis preregistrado. Los cambios de signo quedan como resultado secundario y no establecen importancia clínica.

Tres resúmenes completos (RMS, MAV, RMS limitado p99,5) más 18 variantes de bloque (3 tamaños ×3 umbrales ×2 métricas). Se conservan los 88 registros y todas las variantes. La utilidad demostrada es **auditar la estabilidad de la dirección y magnitud de una interpretación descriptiva**, con tabla por persona y señal consultable. No se usa umbral 90%, p-value ni criterio de retorno deportivo.

La auditoría amplía el análisis estándar del dataset; para afirmar novedad bibliográfica hace falta una búsqueda específica de estudios multiverse/specification-curve y robustez sEMG. Para afirmar utilidad clínica hace falta validación independiente y desenlaces observados. No se añaden inferencias de grupo seleccionando la especificación más favorable.

La revisión dirigida localizó [Simonsohn, Simmons y Nelson (2020)](https://doi.org/10.1038/s41562-020-0912-z), antecedente de specification curve analysis. La idea de evaluar decisiones alternativas ya existe. Este proyecto adapta una auditoría descriptiva a estos registros y no ejecuta el procedimiento inferencial completo de ese artículo.

## Entregables y reproducción

- [924 resultados de especificación](../../reports/robustness_specifications.csv).
- [44 resúmenes por participante-condición](../../reports/robustness_participant_summary.csv).
- [105 resultados sintéticos](../../reports/robustness_synthetic_checks.csv).
- Código: scripts/evaluate_robustness.py, después de comprehensive_semg.py.

No hay validación independiente ni ejecución confirmada en Kaggle todavía. El paquete preparado contiene datos originales atribuidos, código y notebook que regenera los análisis.
"""
    (ROOT / "docs/history/robustness_results.md").write_text(content, encoding="utf-8")
    result = {
        "pairs": 44,
        "specifications_per_pair": 21,
        "rows": 924,
        "direction_changes": changed,
        "participants_with_direction_changes": people,
        "rms_only_direction_changes": int(rms_changed),
        "excluded_pairs": sorted("/".join(k) for k in excluded),
        "primary_pairs": len(primary),
        "primary_direction_changes": int(primary_changed),
        "primary_rms_only_direction_changes": int(primary_rms_changed),
        "synthetic_assertions_passed": True,
    }
    (ROOT / "reports/robustness_summary.json").write_text(
        json.dumps(result, indent=2), encoding="utf-8"
    )
    print(json.dumps(result))


if __name__ == "__main__":
    main()
