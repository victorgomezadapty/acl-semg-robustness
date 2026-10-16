"""Generate an auditable descriptive cohort report, with matched subsets."""

import json
import os
from pathlib import Path

import numpy as np


def main():
    data = json.loads(
        Path("reports/enabl3s_cohort_results_v1.json").read_text(encoding="utf-8")
    )
    people = data["participants"]
    summary = data["summary"]
    lines = [
        "# ENABL3S: ejecución de los nueve participantes restantes",
        "",
        "2026-10-09 · Análisis secundario de métodos en personas sanas. AB191 se mantiene como piloto separado. No es validación clínica de reconstrucción de LCA ni demostración de novedad científica.",
        "",
        "[Protocolo v1](enabl3s_cohort_protocol_v1.md) · [integridad de los nueve ZIP](../reports/enabl3s_cohort_download_manifest.json) · [resultados y auditoría completos](../reports/enabl3s_cohort_results_v1.json) · [tabla principal](../reports/enabl3s_cohort_primary_v1.csv).",
        "",
        "Fuente: Hu, Rouse y Hargrove, [ENABL3S v2](https://doi.org/10.6084/m9.figshare.5362627.v2), CC BY 4.0. Se conservaron los originales; se usó Processed sin filtrado adicional ni conversión de unidades. Las notas vacías no certifican ausencia de artefactos. La configuración y los archivos congelados se verificaron por SHA-256 antes del cálculo.",
        "",
        "## Flujo de participantes",
        "",
        f"De nueve participantes: {summary['eligible']} tienen un tramo elegible, {summary['excluded']} están excluidos y {summary['not_calculable']} presentan un error que impide el cálculo. De los elegibles, {summary['complete_primary']} tienen las once razones positivas y finitas del principal.",
        "",
        "| Participante | Estado principal | Duración útil (s) | Rango de log-razones | Cruce de 1 |",
        "|---|---|---:|---:|---|",
    ]
    primary = {}
    for person in people:
        if person["status"] == "eligible":
            analysis = next(a for a in person["analyses"] if a["primary"])
            primary[person["participant"]] = analysis
            value = (
                f"{analysis['log_ratio_range']:.4f}"
                if analysis["log_ratio_range"] is not None
                else "No completo"
            )
            lines.append(
                f"| {person['participant']} | {analysis['status']} | {analysis['samples'] / 1000:.3f} | {value} | {analysis['crosses_one']} |"
            )
        else:
            lines.append(
                f"| {person['participant']} | {person['status']}: {person.get('reason', '')} | — | — | — |"
            )
    if summary["complete_primary"]:
        lines += [
            "",
            f"Entre los {summary['complete_primary']} principales completos, mediana del rango de log-razones: **{summary['primary_log_range_median']:.4f}** (mínimo {summary['primary_log_range_minimum']:.4f}; máximo {summary['primary_log_range_maximum']:.4f}). {summary['primary_crossings_of_one']} cruzan 1 entre métodos. El rango no es un intervalo de confianza y un cruce pequeño no establece importancia clínica.",
        ]
    lines += [
        "",
        "## Sensibilidades y casos no calculables",
        "",
        "Cada margen alternativo se aplicó al mismo tramo original, sin buscar otro para aumentar la muestra. La tabla distingue resultados completos, parciales y segmentos demasiado cortos. La diferencia emparejada de rango se calcula solo en participantes con ambos rangos completos; no compara medianas de muestras distintas.",
        "",
        "| Margen (ms) | Familia | Selección | Completos | Parciales | No disponibles | Diferencia mediana vs principal (n emparejado) |",
        "|---:|---|---|---:|---:|---:|---|",
    ]
    groups = sorted(
        {
            (a["guard_samples"], a["family"], a["selection"])
            for p in people
            for a in p["analyses"]
        }
    )
    sensitivity_summary = []
    for guard, family, selection in groups:
        counts = {"complete": 0, "partial": 0, "unavailable": 0}
        differences = []
        matched = []
        undefined = 0
        for person in people:
            for analysis in person["analyses"]:
                if (
                    analysis["guard_samples"],
                    analysis["family"],
                    analysis["selection"],
                ) != (guard, family, selection):
                    continue
                counts[analysis["status"]] += 1
                undefined += sum(
                    row["undefined_reason"] is not None
                    for row in analysis.get("specifications", [])
                )
                reference = primary[person["participant"]]
                if analysis["status"] == reference["status"] == "complete":
                    differences.append(
                        analysis["log_ratio_range"] - reference["log_ratio_range"]
                    )
                    matched.append(person["participant"])
        delta = float(np.median(differences)) if differences else None
        text = (
            f"{delta:+.4f} (n={len(matched)})" if delta is not None else "No calculable"
        )
        lines.append(
            f"| {guard} | {family} | {selection} | {counts['complete']} | {counts['partial']} | {counts['unavailable']} | {text} |"
        )
        sensitivity_summary.append(
            {
                "guard": guard,
                "family": family,
                "selection": selection,
                "counts": counts,
                "undefined_specifications": undefined,
                "matched_participants": matched,
                "median_paired_log_range_difference": delta,
            }
        )
    lines += ["", "## Registro de exclusiones", ""]
    for person in people:
        screened = person.get("trial_audit", [])
        counts = {}
        for trial in screened:
            counts[trial["reason"]] = counts.get(trial["reason"], 0) + 1
        lines.append(
            f"- **{person['participant']}**: {json.dumps(counts, ensure_ascii=False)}; {len(person.get('unassessed_later_trials', []))} ensayos posteriores no evaluados porque la selección determinista ya terminó. Textos de notas, archivos e índices constan en el JSON completo."
        )
    lines += [
        "",
        "## Interpretación y reproducción",
        "",
        "Las diferencias describen dependencia del algoritmo y la ventana elegida. No identifican qué método es fisiológicamente correcto. La selección compartida puede privilegiar coactivación; las ventanas de duración equivalente no igualan tarea, fase de marcha, sensores o procesamiento con Dryad. No se combinan sujetos, bloques o ensayos como unidades independientes ni se infieren fuerza o retorno al deporte.",
        "",
        "El análisis conserva amplitudes de numerador/denominador, colas descartadas e índices de selección. Variantes sin intersección, con denominador no positivo o con rango incompleto se mantienen con motivo explícito. Las razones se interpretan como cocientes de unidades de exportación; no eliminan posibles diferencias de ganancia o normalización bilateral.",
        "",
        "```powershell",
        ".\\.venv\\Scripts\\python.exe scripts/fetch_enabl3s_cohort.py",
        ".\\.venv\\Scripts\\python.exe scripts/analyze_enabl3s_cohort.py",
        ".\\.venv\\Scripts\\python.exe scripts/report_enabl3s_cohort.py",
        "```",
        "",
        "La descarga requiere Internet; el análisis es local una vez verificados los originales. Esta extensión no actualiza automáticamente Kaggle.",
    ]
    Path("reports/enabl3s_cohort_sensitivity_summary_v1.json").write_text(
        json.dumps(sensitivity_summary, indent=2, allow_nan=False), encoding="utf-8"
    )
    if primary:
        os.environ.setdefault("MPLCONFIGDIR", str(Path(".mpl-cache").resolve()))
        import matplotlib.pyplot as plt

        figure, axis = plt.subplots(figsize=(8, 4.5))
        for index, (participant, analysis) in enumerate(primary.items()):
            ratios = [
                r["ratio"]
                for r in analysis["specifications"]
                if r["ratio"] is not None and r["ratio"] > 0
            ]
            axis.scatter(ratios, [index] * len(ratios), s=24, alpha=0.7)
        axis.set_yticks(range(len(primary)), list(primary))
        axis.set_xscale("log")
        axis.axvline(1, color="gray", linestyle="--")
        axis.set_xlabel("Right/left VL amplitude ratio (log scale)")
        axis.set_title(
            "ENABL3S: 11 RMS specifications per participant\nFrozen primary rules; healthy population; no clinical inference"
        )
        axis.grid(axis="x", alpha=0.2)
        figure.tight_layout()
        figure.savefig("reports/figures/enabl3s_cohort_primary_v1.png", dpi=180)
        plt.close(figure)
        lines += [
            "",
            "![Razones por participante y método](../reports/figures/enabl3s_cohort_primary_v1.png)",
        ]
    Path("docs/enabl3s_cohort_results_v1.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
