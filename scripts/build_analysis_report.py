"""Generate auditable Markdown, sensitivity plots and a local participant profile index."""

import csv
import html
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault("MPLCONFIGDIR", str(ROOT / ".mpl-cache"))
sys.path.insert(0, str(ROOT))
import matplotlib
import numpy as np
from scipy import optimize, stats

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def read(name):
    with (ROOT / name).open(encoding="utf-8-sig") as stream:
        return list(csv.DictReader(stream))


def write(name, rows):
    with (ROOT / name).open("w", newline="", encoding="utf-8") as stream:
        w = csv.DictWriter(stream, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


def main():
    summary = json.loads((ROOT / "reports/comprehensive_summary.json").read_text())
    features = read("data/processed/semg_extended_features.csv")
    pairs = read("data/processed/semg_extended_pairs.csv")
    comparison = read("reports/publication_comparison.csv")
    blocks = read("reports/block_selection_sensitivity.csv")
    qa_features = read("data/processed/semg_amplitude_features.csv")
    short_pairs = {
        (r["participant_id"], r["condition"])
        for r in qa_features
        if "short_record_review" in r["qa_flags"]
    }
    sensitivity = []
    for size in [256, 512, 1024]:
        for fraction in [0.1, 0.2, 0.3]:
            for cohort in ["healthy", "patient"]:
                for condition in ["iso90", "iso180"]:
                    subset = [
                        r
                        for r in blocks
                        if int(r["block_samples"]) == size
                        and float(r["threshold_fraction"]) == fraction
                        and r["cohort"] == cohort
                        and r["condition"] == condition
                    ]
                    ids = sorted({r["participant_id"] for r in subset})
                    ratios = []
                    for p in ids:
                        a = next(
                            r
                            for r in subset
                            if r["participant_id"] == p and r["limb_label"] == "inv"
                        )
                        b = next(
                            r
                            for r in subset
                            if r["participant_id"] == p and r["limb_label"] == "uninv"
                        )
                        if a["selected_rms_V"] and b["selected_rms_V"]:
                            ratios.append(
                                100
                                * float(a["selected_rms_V"])
                                / float(b["selected_rms_V"])
                            )
                    sensitivity.append(
                        {
                            "block_samples": size,
                            "threshold_fraction": fraction,
                            "cohort": cohort,
                            "condition": condition,
                            "n": len(ratios),
                            "mean_rms_ratio_pct": float(np.mean(ratios)),
                            "median_rms_ratio_pct": float(np.median(ratios)),
                            "sd_ratio_pct": float(np.std(ratios, ddof=1)),
                        }
                    )
    write("reports/block_ratio_sensitivity.csv", sensitivity)
    planning = []
    for effect in [0.3, 0.5, 0.62, 0.8]:

        def power(n):
            df = 2 * n - 2
            critical = stats.t.ppf(0.975, df)
            nc = effect * np.sqrt(n / 2)
            return stats.nct.sf(critical, df, nc) + stats.nct.cdf(-critical, df, nc)

        upper = 4
        while power(upper) < 0.8:
            upper *= 2
        n = int(np.ceil(optimize.brentq(lambda n: power(n) - 0.8, 3, upper)))
        planning.append(
            {
                "hypothetical_standardized_effect": effect,
                "participants_per_group": n,
                "power_at_n": float(power(n)),
                "alpha": 0.05,
                "target_power": 0.8,
                "design": "two_independent_equal_groups_two_sided_t_no_multiplicity",
            }
        )
    write("reports/hypothetical_sample_size.csv", planning)
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    for i, cohort in enumerate(["healthy", "patient"]):
        for j, condition in enumerate(["iso90", "iso180"]):
            ax = axes[i, j]
            for size, color in [(256, "#236a8d"), (512, "#be573c"), (1024, "#4a8264")]:
                rows = [
                    r
                    for r in sensitivity
                    if r["block_samples"] == size
                    and r["cohort"] == cohort
                    and r["condition"] == condition
                ]
                ax.plot(
                    [r["threshold_fraction"] for r in rows],
                    [r["median_rms_ratio_pct"] for r in rows],
                    ".-",
                    color=color,
                    label=f"{size} samples",
                )
            original = [
                float(r["rms_V_ratio_pct"])
                for r in pairs
                if r["cohort"] == cohort and r["condition"] == condition
            ]
            ax.axhline(
                np.median(original),
                linestyle="--",
                color="gray",
                label="Whole-record median",
            )
            ax.set_title(f"{cohort} / {condition}")
            ax.set_ylabel("Median inv/uninv RMS (%)")
            ax.set_xlabel("Threshold fraction (analyst-defined)")
            ax.legend(fontsize=7)
            ax.grid(alpha=0.2)
    fig.suptitle(
        "Sensitivity to higher-amplitude block selection\nNot validated contraction segmentation; no threshold was selected as best"
    )
    fig.tight_layout(rect=[0, 0, 1, 0.91])
    fig.savefig(ROOT / "reports/figures/block_ratio_sensitivity.png", dpi=150)
    plt.close(fig)
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    for ax, condition in zip(axes, ["iso90", "iso180"]):
        for cohort, color in [("healthy", "#236a8d"), ("patient", "#be573c")]:
            # Bilateral mean gives exactly one participant point per condition.
            ids = sorted(
                {r["participant_id"] for r in features if r["cohort"] == cohort}
            )
            x = []
            y = []
            for p in ids:
                records = [
                    r
                    for r in features
                    if r["participant_id"] == p and r["condition"] == condition
                ]
                x.append(np.mean([float(r["rms_V"]) * 1e6 for r in records]))
                y.append(np.mean([float(r["mav_V"]) * 1e6 for r in records]))
            ax.scatter(x, y, color=color, label=cohort)
            ax.set_title(condition)
            ax.legend()
            ax.set_xlabel("Bilateral mean RMS (microvolts)")
            ax.set_ylabel("Bilateral mean MAV (microvolts)")
            ax.grid(alpha=0.2)
    fig.suptitle(
        "RMS and MAV: one point per participant\nShared signal inputs; association is not independent physiological validation"
    )
    fig.tight_layout(rect=[0, 0, 1, 0.9])
    fig.savefig(ROOT / "reports/figures/amplitude_relationships.png", dpi=150)
    plt.close(fig)
    lines = [
        "# Análisis ampliado con el dataset disponible",
        "",
        "Fecha: 2026-10-04. Resultados exploratorios reproducibles, sin ML ni etiquetas de alta deportiva.",
        "",
        f"Se analizaron {summary['records']} registros, {summary['participant_pairs']} pares condición-miembro y {summary['participants']} personas. Se ejecutaron {summary['comparisons']} comparaciones y {summary['correlations']} correlaciones, y se generaron {summary['profiles']} perfiles.",
        "",
        "## Comparación con la publicación",
        "",
        "Estas cifras contrastan cocientes RMS de registro completo con los reportados. No se afirma reproducción exacta.",
        "",
        "| Cohorte | Condición | Nuestro promedio ± SD (%) | Publicado ± SD (%) |",
        "|---|---|---|---|",
    ]
    for r in comparison:
        if r["metric"] == "rms_V":
            lines.append(
                f"| {r['cohort']} | {r['condition']} | {float(r['our_whole_record_mean_pct']):.2f} ± {float(r['our_whole_record_sd_pct']):.2f} | {float(r['published_mean_pct']):.2f} ± {float(r['published_sd_pct']):.2f} |"
            )
    controls = [
        float(r["rms_V_ratio_pct"])
        for r in pairs
        if r["cohort"] == "healthy"
        and r["condition"] == "iso90"
        and (r["participant_id"], r["condition"]) not in short_pairs
    ]
    lines.extend(
        [
            "",
            f"En controles iso90, omitir el par corto healthy8 solo como sensibilidad cambia la media a {np.mean(controls):.2f}% y SD a {np.std(controls, ddof=1):.2f}%. El análisis principal lo conserva. Un cociente con denominador pequeño puede distorsionar la media; por eso se muestran medianas y valores absolutos.",
            "",
            "El pico positivo y el absoluto producen cocientes diferentes. Ninguna variante fue elegida para hacer coincidir resultados. Unidades de amplitud, procesamiento y ciclos publicados no permiten una reproducción numérica exacta desde el texto disponible.",
            "",
            "Referencia: [Khafagy y Hamza, 2026](https://doi.org/10.25259/JMSR_129_2026), tabla 2.",
            "",
            "## Inferencia exploratoria",
            "",
            f"Tests t con p-Holm <0,05: {summary['holm_t_below_005']}; tests de rangos con p-Holm <0,05: {summary['holm_rank_below_005']}. Esto no demuestra equivalencia ni ausencia de diferencias. El pequeño tamaño y la calidad/normalización limitan la evidencia.",
            "",
            "Todas las estimaciones, tamaños de efecto e intervalos están en [exploratory_tests.csv](../../reports/exploratory_tests.csv). Los 60 endpoints pertenecen a familias explicitadas en comprehensive_methods.md; no se selecciona un test a partir del p-value. Comparar varias familias sigue siendo exploratorio.",
            "",
            "## Sensibilidad y relaciones",
            "",
            "Se evaluaron 792 combinaciones registro/bloque/umbral, resumidas en 36 filas cohorte-condición. La selección matemática de amplitud permite estudiar cuánto cambia el cociente al reducir periodos de baja amplitud; no identifica ciclos clínicos ni elimina el problema del registro corto. Los gráficos y todas las variantes permanecen disponibles.",
            "",
            "Se incluyen correlaciones por cohorte, condición y miembro. RMS y MAV comparten los mismos datos: no interpretar su asociación como mecanismo clínico. Longitud–RMS es un diagnóstico de posible dependencia de la duración del registro.",
            "",
            "## Planificación educativa de muestra",
            "",
            "Se calculó tamaño hipotético para dos grupos independientes, alfa 0,05 y potencia 80%, usando efectos supuestos (no estimaciones fiables de este piloto). No incluye multiplicidad, pérdidas ni medidas repetidas.",
            "",
            "| Efecto supuesto | Personas por grupo |",
            "|---|---|",
        ]
    )
    for r in planning:
        lines.append(
            f"| {r['hypothetical_standardized_effect']} | {r['participants_per_group']} |"
        )
    lines.extend(
        [
            "",
            "## Perfiles y reproducibilidad",
            "",
            "El [índice local de perfiles](../../reports/analysis_index.html) permite elegir entre las 22 personas. Cada perfil contiene ambas condiciones, señal exportada, amplitud y referencia descriptiva de controles. No muestra torque, reinjury risk ni puntuación RTS.",
            "",
            "Código: scripts/comprehensive_semg.py y scripts/build_analysis_report.py. Validación: scripts/check_statistics.py y check_amplitude.py; conteos y hashes comprobados. [Métodos](comprehensive_methods.md) y [cobertura](analysis_coverage.md) documentan lo implementado y los límites.",
            "",
            "Conclusión: el dataset permite análisis completos de magnitud y simetría sEMG exportada. Nuestros resultados no justifican adoptar las conclusiones clínicas publicadas sin más; diferencias de procesamiento y tareas pueden cambiar los resultados. Los puntos pendientes ya no impiden estos análisis, y cualquier extensión posterior parte de estos entregables.",
        ]
    )
    (ROOT / "docs/history/comprehensive_results.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )
    ids = sorted(
        {r["participant_id"] for r in features},
        key=lambda p: (p.startswith("patient"), int("".join(filter(str.isdigit, p)))),
    )
    options = "".join(f'<option value="{p}">{p}</option>' for p in ids)
    rows = "".join(
        f"<tr><td>{html.escape(r['cohort'])}</td><td>{r['condition']}</td><td>{float(r['our_whole_record_mean_pct']):.2f}</td><td>{float(r['our_whole_record_sd_pct']):.2f}</td><td>{float(r['published_mean_pct']):.2f}</td></tr>"
        for r in comparison
        if r["metric"] == "rms_V"
    )
    document = """<!doctype html><html lang="es"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>ACL — informe exploratorio sEMG</title>
<style>body{font:16px/1.6 system-ui;color:#193244;background:#f4f7f8;margin:0}main{max-width:1150px;margin:auto;padding:32px}section{background:white;padding:24px;margin:24px 0;border-radius:12px}h1{font-size:32px;line-height:1.2}h2{font-size:22px}img{width:100%;height:auto}select{font:inherit;padding:10px;min-width:180px}table{border-collapse:collapse;width:100%}th,td{text-align:left;border-bottom:1px solid #ddd;padding:10px}.note{border-left:4px solid #be573c;padding-left:16px}a{color:#236a8d}</style><main>
<h1>sEMG limb symmetry after ACL reconstruction: robustness analysis</h1><p>22 participantes · 88 registros sEMG · baseline exploratorio conservado</p>
<section><h2>Current robustness review</h2><p>Within-person sensitivity is the primary interpretation. Absolute between-cohort voltages are supplemental acquisition-dependent descriptions. Clinical validity and scientific priority are unestablished.</p><p><a href="../docs/review_methods.md">Methods</a> · <a href="../docs/review_results.md">Results</a> · <a href="../docs/review_limitations.md">Limitations</a> · <a href="../docs/review_case.md">Portfolio case</a></p><img src="figures/centering_ratio_sensitivity.png" alt="Exported versus centered RMS ratios"><img src="figures/synthetic_scenario_matrix.png" alt="Controlled synthetic scenario errors"></section>
<p class="note">Amplitud de registros exportados, sin normalización MVC. Los resultados describen estas señales; no representan fuerza ni preparación para volver al deporte.</p>
<section><h2>Perfil individual</h2><label for="participant">Participante </label><select id="participant">OPTIONS</select><p>Señales por índice de muestra. Referencia de controles descriptiva; en perfiles de controles incluye al propio participante. Sin sincronización de contracciones entre miembros.</p><img id="profile" src="figures/profiles/healthy1.png" alt="Perfil exploratorio healthy1"></section>
<section><h2>Comparación con la publicación</h2><p>Cociente RMS inv/uninv ×100. Registro completo; procesamiento/ciclos publicados no reproducidos exactamente. SD = desviación estándar. El registro corto healthy8 afecta especialmente la media de controles iso90.</p><table><thead><tr><th>Cohorte</th><th>Condición</th><th>Nuestra media (%)</th><th>Nuestra SD</th><th>Media publicada (%)</th></tr></thead><tbody>ROWS</tbody></table><p><a href="publication_comparison.csv">Tabla completa</a> · <a href="https://doi.org/10.25259/JMSR_129_2026">Artículo</a></p></section>
<section><h2>Distribución individual de balance sEMG</h2><img src="figures/extended_balance_distributions.png" alt="Balance individual en cohortes y condiciones"></section>
<section><h2>Sensibilidad a la selección de bloques</h2><img src="figures/block_ratio_sensitivity.png" alt="Sensibilidad de cocientes a bloques y umbrales"></section>
<section><h2>Resultados y documentación</h2><p>60 comparaciones y 24 correlaciones exploratorias. Ninguna comparación conserva p &lt;0,05 tras Holm dentro de su familia; esto no demuestra equivalencia.</p><p><a href="exploratory_tests.csv">Comparaciones y efectos</a> · <a href="exploratory_correlations.csv">Correlaciones</a> · <a href="../docs/history/comprehensive_results.md">Informe completo</a> · <a href="../docs/history/comprehensive_methods.md">Métodos</a> · <a href="../docs/history/literature_review.md">Literatura</a></p></section></main>
<script>const select=document.getElementById('participant');select.addEventListener('change',()=>{const img=document.getElementById('profile');img.src='figures/profiles/'+select.value+'.png';img.alt='Perfil exploratorio '+select.value;});</script></html>"""
    (ROOT / "reports/analysis_index.html").write_text(
        document.replace("OPTIONS", options).replace("ROWS", rows), encoding="utf-8"
    )
    print(
        "Report, local 22-participant index, sensitivity plots and sample-size planning generated."
    )


if __name__ == "__main__":
    main()
