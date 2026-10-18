'use strict';
const data = window.ACL_DATA;
const select = document.querySelector('#participant');
let logScale = false;
const number = (value, digits = 3) => value.toLocaleString('es-ES', {minimumFractionDigits: digits, maximumFractionDigits: digits});
const pretty = method => method === 'whole_RMS' ? 'RMS completo' : method === 'cap995_RMS' ? 'RMS · límite p99,5' : method.replace('block', 'Bloque ').replace('_f', ' · f = ').replace('_RMS', '');
select.replaceChildren(...data.people.map(person => {
  const option = document.createElement('option'); option.value = person.id; option.textContent = person.id; return option;
}));
document.querySelector('#metric-pairs').textContent = data.dryad.primary_pairs;
document.querySelector('#metric-crossings').textContent = `${data.dryad.primary_direction_changes} / ${data.dryad.primary_pairs}`;
function renderChart() {
  const person = data.people.find(p => p.id === select.value);
  const entries = person.specifications.map(s => ({...s, value: logScale ? Math.log(s.ratio) : s.ratio}));
  const reference = logScale ? 0 : 1;
  const min = Math.min(reference, ...entries.map(s => s.value));
  const max = Math.max(reference, ...entries.map(s => s.value));
  const padding = Math.max((max - min) * .15, logScale ? .02 : .025);
  const left = 164, right = 580, top = 38, row = 29, height = 418;
  const scale = value => left + (value - min + padding) / (max - min + padding * 2) * (right - left);
  const xRef = scale(reference);
  let svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 655 ${height}" aria-hidden="true"><text x="164" y="14" fill="#5a6c63" font-size="10">${logScale ? 'ln(RMS derecha / izquierda)' : 'RMS derecha / izquierda'}</text><line x1="${xRef}" y1="24" x2="${xRef}" y2="364" stroke="#718277" stroke-dasharray="4 4"/><text x="${xRef}" y="384" text-anchor="middle" font-size="10" fill="#5a6c63">${reference} · igualdad</text>`;
  entries.forEach((entry, index) => {
    const y = top + index * row;
    const x = scale(entry.value);
    const color = entry.ratio < 1 ? '#a35437' : '#126a57';
    svg += `<line x1="${left}" y1="${y}" x2="${right}" y2="${y}" stroke="#dfe3d8"/><text x="0" y="${y + 4}" fill="#243c31" font-size="11">${pretty(entry.method)}</text><line x1="${xRef}" y1="${y}" x2="${x}" y2="${y}" stroke="${color}" stroke-width="3" opacity=".35"/><circle cx="${x}" cy="${y}" r="5" fill="${color}"/><text x="594" y="${y + 4}" fill="#243c31" font-size="11">${number(entry.value)}</text>`;
  });
  svg += '<text x="164" y="410" fill="#5a6c63" font-size="10">Mismos datos · once decisiones · sin umbral clínico</text></svg>';
  const chart = document.querySelector('#participant-chart'); chart.innerHTML = svg;
  chart.setAttribute('aria-label', `${person.id}: once métodos. ${person.crosses ? 'Las razones cruzan uno' : 'Las razones no cruzan uno'}. Los valores exactos están en la tabla siguiente.`);
  document.querySelector('#range-value').textContent = number(person.range, 4);
  document.querySelector('#crossing-description').textContent = person.crosses ? 'Cruza 1 entre métodos: la dirección descriptiva cambia. Esto no establece importancia clínica.' : 'No cruza 1 entre estos métodos. Conservar la dirección no demuestra exactitud fisiológica.';
  document.querySelector('#duration-description').textContent = `Tramo útil: ${number(person.seconds)} s. Selección independiente y margen de 500 ms por borde.`;
  document.querySelector('#chart-subtitle').textContent = `${person.id} · principal completo`;
  document.querySelector('#data-table').replaceChildren(...entries.map(entry => {
    const rowEl = document.createElement('tr');
    [entry.method, number(entry.ratio, 6), number(Math.log(entry.ratio), 6)].forEach(text => { const td = document.createElement('td'); td.textContent = text; rowEl.append(td); });
    return rowEl;
  }));
  for (const [id, active] of [['ratio-mode', !logScale], ['log-mode', logScale]]) {
    const button = document.getElementById(id); button.classList.toggle('active', active); button.setAttribute('aria-pressed', String(active));
  }
}
select.addEventListener('change', renderChart);
document.querySelector('#ratio-mode').addEventListener('click', () => {logScale = false; renderChart();});
document.querySelector('#log-mode').addEventListener('click', () => {logScale = true; renderChart();});
const figures = {
  robustness: {image:'robustness_matrix.png', tag:'DRYAD / DATOS OBSERVADOS', title:'Una dirección puede depender del resumen.', description:'13 de 43 pares principales cruzan 1 entre 21 métodos; entre las once especificaciones RMS lo hacen 10. Las condiciones de una misma persona no son observaciones independientes.', alt:'Matriz de razones bilaterales Dryad por participante y método'},
  filter: {image:'bandpass_sensitivity.png', tag:'DRYAD / SENSIBILIDAD CONDICIONAL', title:'Una mediana estable puede ocultar cambios individuales.', description:'El filtro 20–450 Hz cambia la dirección RMS completa en 1 de 43 pares. La retención RMS señala atenuación para revisar; no diagnostica artefactos ni mide energía fuera de banda. La frecuencia media se deriva del reloj exportado.', alt:'Sensibilidad de razones al filtrado y retención de amplitud RMS'},
  synthetic: {image:'synthetic_scenario_matrix.png', tag:'SIMULACIÓN / REFERENCIA CONSTRUIDA', title:'Ayudar en un escenario no significa ganar en todos.', description:'23.100 evaluaciones: 11 escenarios × 100 realizaciones × 21 métodos. Limitar picos puede ayudar ante un artefacto construido y distorsionar un evento deseado. La ganancia desigual desconocida persiste. No son resultados clínicos.', alt:'Errores por escenario sintético y método ante una referencia construida'}
};
document.querySelectorAll('[data-figure]').forEach(button => button.addEventListener('click', () => {
  const figure = figures[button.dataset.figure]; const image = document.querySelector('#evidence-image');
  image.src = `assets/${figure.image}`; image.alt = figure.alt;
  document.querySelector('#evidence-tag').textContent = figure.tag;
  document.querySelector('#evidence-title').textContent = figure.title;
  document.querySelector('#evidence-description').textContent = figure.description;
  document.querySelectorAll('[data-figure]').forEach(b => {const active = b === button; b.classList.toggle('active', active); b.setAttribute('aria-pressed', String(active));});
}));
const references = document.querySelector('#references-list');
data.literature.forEach(source => {
  const item = document.createElement('li'); const link = document.createElement('a'); link.href = source.url;
  link.textContent = `${source.authors} (${source.year}). ${source.title}. ↗`;
  const state = document.createElement('span'); state.textContent = `${source.access_reviewed}. ${source.data_status}.`;
  item.append(link, state); references.append(item);
});
renderChart();
