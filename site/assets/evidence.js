// Figures for the evidence page. Values are quoted from the cited papers
// (Ardern 2014; Wellsandt 2017) and from this project's dataset audit.
window.aclFigures = window.aclFigures || [];
window.aclFigures.push(({el, text, T, fmt, onLang}) => {
  const bars = (host, rows, label) => onLang(() => {
    host.querySelector('svg')?.remove();
    const s = el('svg', {viewBox: `0 0 560 ${rows.length * 46 + 34}`, role: 'img', 'aria-label': label()});
    host.prepend(s);
    const X = v => 230 + v / 100 * 300;
    [0, 25, 50, 75, 100].forEach(v => { el('line', {x1: X(v), x2: X(v), y1: 8, y2: rows.length * 46 + 8, class: 'ax'}, s); text(s, X(v), rows.length * 46 + 26, v + '%', 'ax-text', 'middle'); });
    rows.forEach(([lab, v, cls], i) => {
      const y = 16 + i * 46;
      text(s, 220, y + 15, lab(), 'lbl', 'end');
      el('path', {d: `M${X(0)},${y}H${X(v) - 4}Q${X(v)},${y} ${X(v)},${y + 4}V${y + 18}Q${X(v)},${y + 22} ${X(v) - 4},${y + 22}H${X(0)}Z`, class: cls + ' growx', style: `transition-delay:${i * 180}ms`}, s);
      text(s, X(v) + 8, y + 16, fmt(v, v % 1 ? 1 : 0) + '%', 'lbl fade');
    });
  });
  const rts = document.querySelector('[data-fig="rts"]');
  if(rts) bars(rts, [
    [() => T('Any sport', 'Cualquier deporte'), 81, 'm-cyan'],
    [() => T('Pre-injury level', 'Nivel previo a la lesión'), 65, 'm-cyan'],
    [() => T('Competitive sport', 'Deporte competitivo'), 55, 'm-cyan'],
  ], () => T('Return to sport after ACL reconstruction: 81% any sport, 65% pre-injury level, 55% competitive.', 'Retorno al deporte tras reconstrucción de LCA: 81% cualquier deporte, 65% nivel previo, 55% competitivo.'));
  const lsi = document.querySelector('[data-fig="lsi"]');
  if(lsi) bars(lsi, [
    [() => T('Met 90% limb symmetry', 'Alcanzó 90% de simetría'), 57.1, 'm-cyan'],
    [() => T('Met 90% of pre-injury capacity', 'Alcanzó 90% de la capacidad previa'), 28.6, 'm-coral'],
    [() => T('Passed symmetry, failed pre-injury', 'Pasó simetría, falló capacidad previa'), 34.3, 'm-soft'],
  ], () => T('At 6 months, 57.1% met 90% limb symmetry but only 28.6% met 90% of estimated pre-injury capacity.', 'A los 6 meses, el 57,1% alcanzó 90% de simetría pero solo el 28,6% alcanzó 90% de la capacidad previa estimada.'));
});
