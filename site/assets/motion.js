// Visual layer for the ACL sEMG site. Every number in the charts comes from
// window.ACL (scripts/build_site_data.py, derived from saved results). The hero
// waveform and the signal lab are synthetic illustrations and say so on the page.
(function(){
  'use strict';
  const D = window.ACL;
  const NS = 'http://www.w3.org/2000/svg';
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const lang = () => document.documentElement.lang === 'es' ? 'es' : 'en';
  const T = (en, es) => lang() === 'es' ? es : en;
  const fmt = (x, d = 2) => { const s = (+x).toFixed(d); return lang() === 'es' ? s.replace('.', ',') : s; };
  const el = (tag, attrs = {}, parent) => { const n = document.createElementNS(NS, tag); for(const [k, v] of Object.entries(attrs)) n.setAttribute(k, v); if(parent) parent.appendChild(n); return n; };
  const text = (p, x, y, s, cls, anchor = 'start') => { const t = el('text', {x, y, class: cls, 'text-anchor': anchor}, p); t.textContent = s; return t; };
  const renderers = [];
  const onLang = fn => { renderers.push(fn); fn(); };
  document.addEventListener('acl:lang', () => renderers.forEach(f => f()));
  const methodName = m => m === 'whole_RMS' ? T('whole RMS', 'RMS completo') : m === 'whole_MAV' ? T('whole MAV', 'MAV completo') : m === 'cap995_RMS' ? T('capped RMS 99.5%', 'RMS limitado 99,5%')
    : m.replace(/^block(\d+)_f0\.(\d)_(RMS|MAV)$/, (_, s, f, k) => `${T('blocks', 'bloques')} ${s} · 0.${f} ${k}`);
  const shortName = m => m === 'whole_RMS' ? 'wRMS' : m === 'whole_MAV' ? 'wMAV' : m === 'cap995_RMS' ? 'cap' : m.replace(/^block(\d+)_f0\.(\d)_(RMS|MAV)$/, (_, s, f, k) => `${s}.${f}${k[0]}`);

  /* ---------- progress, reveal, count-up ---------- */
  const bar = document.querySelector('.progress');
  if(bar){ const u = () => { const h = document.documentElement; bar.style.transform = `scaleX(${h.scrollTop / Math.max(1, h.scrollHeight - h.clientHeight)})`; }; addEventListener('scroll', u, {passive: true}); u(); }
  const numOut = n => { const to = parseFloat(n.dataset.count), suf = n.dataset.suf || ''; return v => { n.textContent = Math.round(v).toLocaleString(lang() === 'es' ? 'es-ES' : 'en-US') + suf; }; };
  const countUp = n => { const out = numOut(n), to = parseFloat(n.dataset.count); if(reduce){ out(to); return; } const t0 = performance.now(); const st = t => { const k = Math.min(1, (t - t0) / 1400); out(to * (1 - Math.pow(1 - k, 3))); if(k < 1) requestAnimationFrame(st); }; requestAnimationFrame(st); };
  const io = new IntersectionObserver(es => es.forEach(e => { if(!e.isIntersecting) return; e.target.classList.add('in'); if(e.target.dataset.count) countUp(e.target); io.unobserve(e.target); }), {threshold: 0.2, rootMargin: '0px 0px -40px 0px'});
  document.addEventListener('acl:lang', () => document.querySelectorAll('[data-count].in').forEach(n => numOut(n)(parseFloat(n.dataset.count))));

  /* ---------- tooltip ---------- */
  function tooltip(host){ const t = document.createElement('div'); t.className = 'tip'; host.appendChild(t); return {show(h, x, y){ t.innerHTML = h; t.style.left = x + 'px'; t.style.top = y + 'px'; t.classList.add('on'); }, hide(){ t.classList.remove('on'); }}; }
  function bindTip(target, host, tip, html, anchor){
    const place = () => { const r = (anchor ? anchor() : target).getBoundingClientRect(), h = host.getBoundingClientRect(); tip.show(html(), r.left + r.width / 2 - h.left, r.top - h.top); };
    target.addEventListener('mouseenter', place); target.addEventListener('focus', place); target.addEventListener('mouseleave', tip.hide); target.addEventListener('blur', tip.hide); target.addEventListener('touchstart', place, {passive: true});
  }
  const logX = (lo, hi, x0, x1) => r => x0 + (Math.log(r) - Math.log(lo)) / (Math.log(hi) - Math.log(lo)) * (x1 - x0);

  /* ---------- hero oscilloscope ---------- */
  const canvas = document.getElementById('scope');
  if(canvas && D){
    const ctx = canvas.getContext('2d'), W = canvas.width, H = canvas.height;
    const ab = D.people.find(p => p.id === 'AB156');
    const specs = ab.specs.filter(s => s[1] > 0);
    const name = document.getElementById('method-name'), ratio = document.getElementById('ratio'), needle = document.getElementById('needle');
    let k = 0, phase = 0, last = 0, timer = 0;
    const seedNoise = (() => { let s = 7; return () => { s = (s * 16807) % 2147483647; return s / 2147483647 - 0.5; }; })();
    const L = Array.from({length: 1800}, () => seedNoise()), R = Array.from({length: 1800}, () => seedNoise());
    const show = () => {
      const [m, r] = specs[k];
      name.textContent = methodName(m);
      ratio.textContent = fmt(r, 3);
      ratio.className = 'ratio ' + (r >= 1 ? 'up' : 'down');
      needle.style.left = Math.max(2, Math.min(98, 50 + Math.log(r) / Math.log(1.6) * 50)) + '%';
    };
    const draw = t => {
      const dt = Math.min(50, t - last); last = t; phase += dt * 0.12;
      ctx.clearRect(0, 0, W, H);
      ctx.strokeStyle = 'rgba(133,146,170,.12)'; ctx.lineWidth = 1;
      for(let x = 0; x < W; x += 60){ ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, H); ctx.stroke(); }
      for(let y = 0; y < H; y += 55){ ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(W, y); ctx.stroke(); }
      const r = specs[k][1];
      const trace = (arr, y0, gain, color, label) => {
        ctx.beginPath(); ctx.lineWidth = 1.6; ctx.strokeStyle = color; ctx.shadowColor = color; ctx.shadowBlur = 8;
        for(let x = 0; x < W; x += 2){
          const i = Math.floor(x / 2 + phase) % arr.length, tt = (x + phase * 2) / 180;
          const env = 0.15 + 0.85 * Math.pow(Math.max(0, Math.sin(tt)), 3);
          const y = y0 + arr[i] * env * 150 * gain;
          x ? ctx.lineTo(x, y) : ctx.moveTo(x, y);
        }
        ctx.stroke(); ctx.shadowBlur = 0;
        ctx.fillStyle = color; ctx.font = '600 22px JetBrains Mono, monospace'; ctx.fillText(label, 14, y0 - 70);
      };
      trace(L, H * 0.3, 1, '#5fd4f5', 'L');
      trace(R, H * 0.74, r, '#ff8a65', 'R');
      if(!reduce) requestAnimationFrame(draw);
    };
    show();
    requestAnimationFrame(draw);
    if(!reduce) timer = setInterval(() => { k = (k + 1) % specs.length; show(); }, 2200);
    document.addEventListener('acl:lang', show);
  }

  /* ---------- charts ---------- */
  function ratioDemo(host){
    const ab = D.people.find(p => p.id === 'AB156'), get = m => ab.specs.find(s => s[0] === m)[1];
    const rows = [['whole_RMS', get('whole_RMS')], ['cap995_RMS', get('cap995_RMS')], ['block256_f0.1_RMS', get('block256_f0.1_RMS')]];
    onLang(() => {
      host.querySelector('svg')?.remove();
      const s = el('svg', {viewBox: '0 0 380 190', role: 'img', 'aria-label': T('Three summaries of the same recordings give ratios of 1.05, 0.96 and 1.22.', 'Tres resúmenes de los mismos registros dan cocientes de 1,05, 0,96 y 1,22.')});
      host.prepend(s);
      const X = logX(0.8, 1.35, 140, 360);
      [0.8, 0.9, 1, 1.1, 1.2, 1.3].forEach(v => text(s, X(v), 178, fmt(v, 1), 'ax-text', 'middle'));
      el('line', {x1: X(1), x2: X(1), y1: 14, y2: 160, class: 'one'}, s);
      text(s, X(1) + 4, 12, T('equal legs', 'piernas iguales'), 'ax-text');
      rows.forEach(([m, r], i) => {
        const y = 42 + i * 46;
        text(s, 130, y + 4, methodName(m), 'lbl', 'end');
        el('line', {x1: X(1), x2: X(r), y1: y, y2: y, class: (r >= 1 ? 's-coral' : 's-cyan') + ' growx', 'stroke-width': 3, 'stroke-linecap': 'round', style: `transition-delay:${i * 200}ms`}, s);
        el('circle', {cx: X(r), cy: y, r: 7, class: (r >= 1 ? 'm-coral' : 'm-cyan') + ' ring pop', style: `transition-delay:${300 + i * 200}ms`}, s);
        text(s, X(r) + (r >= 1 ? 12 : -12), y - 10, fmt(r, 3), 'lbl fade', r >= 1 ? 'start' : 'end');
      });
    });
  }

  function ribbons(host){
    const rows = D.pairs.filter(p => p.primary);
    const tip = tooltip(host);
    let sortKey = 'range', groups = [];
    const rowH = 13, top = 24, H = top + rows.length * rowH + 30;
    const order = () => [...rows].sort((a, b) => sortKey === 'range' ? Math.log(b.max / b.min) - Math.log(a.max / a.min) : b.whole - a.whole);
    const place = () => order().forEach((p, i) => { const g = groups.find(x => x.p === p).g; g.style.transform = `translate(0px, ${top + i * rowH}px)`; });
    onLang(() => {
      host.querySelector('svg')?.remove();
      const s = el('svg', {viewBox: `0 0 1100 ${H}`, role: 'img', 'aria-label': T('Range of ratios across 21 methods for 43 participant-condition pairs; 13 cross 1.', 'Rango de cocientes entre 21 métodos para 43 pares; 13 cruzan 1.')});
      host.prepend(s);
      const X = logX(0.15, 2, 170, 1080);
      [0.2, 0.3, 0.5, 0.7, 1, 1.5, 2].forEach(v => { el('line', {x1: X(v), x2: X(v), y1: top - 8, y2: H - 26, class: 'ax'}, s); text(s, X(v), H - 10, fmt(v, v < 1 && v !== 0.5 ? 1 : v === 0.5 ? 1 : 1), 'ax-text', 'middle'); });
      el('line', {x1: X(1), x2: X(1), y1: top - 14, y2: H - 26, class: 'one'}, s);
      text(s, X(1) + 4, top - 14, T('ratio = 1', 'cociente = 1'), 'ax-text');
      text(s, X(0.16), top - 14, T('← right leg larger', '← pierna derecha mayor'), 'ax-text');
      groups = rows.map((p, i) => {
        const g = el('g', {class: 'row', tabindex: 0, role: 'img', 'aria-label': `${p.id}: ${fmt(p.min)}–${fmt(p.max)}`}, s);
        g.style.transition = reduce ? 'none' : 'transform .8s cubic-bezier(.2,.8,.2,1)';
        text(g, 160, 4, p.id, 'ax-text', 'end');
        el('line', {x1: X(p.min), x2: X(p.max), y1: 0, y2: 0, class: (p.crosses ? 's-coral' : 's-cyan') + ' growx', 'stroke-width': 5, 'stroke-linecap': 'round', style: `transition-delay:${i * 18}ms`}, g);
        el('circle', {cx: X(p.whole), cy: 0, r: 3.2, fill: 'var(--ink)', class: 'fade'}, g);
        el('rect', {x: 0, y: -6, width: 1100, height: 12, class: 'hit'}, g);
        bindTip(g, host, tip, () => `<b>${p.id}</b> · ${p.cohort === 'patient' ? T('ACLR', 'LCA') : T('control', 'control')}<br>${T('range', 'rango')} ${fmt(p.min)}–${fmt(p.max)} · whole RMS ${fmt(p.whole)}${p.crosses ? '<br>' + T('crosses 1', 'cruza 1') : ''}`, () => g.querySelector('circle'));
        return {p, g};
      });
      place();
    });
    host.closest('.card').querySelectorAll('[data-sort]').forEach(b => b.addEventListener('click', () => {
      sortKey = b.dataset.sort;
      host.closest('.card').querySelectorAll('[data-sort]').forEach(x => x.setAttribute('aria-pressed', String(x === b)));
      place();
    }));
  }

  function bandpass(host){
    const pts = D.bandpass, tip = tooltip(host);
    onLang(() => {
      host.querySelector('svg')?.remove();
      const s = el('svg', {viewBox: '0 0 360 300', role: 'img', 'aria-label': T('Exported versus band-passed whole-RMS ratio for 43 pairs; points sit near the identity line.', 'Cociente RMS exportado frente a filtrado para 43 pares; los puntos quedan cerca de la diagonal.')});
      host.prepend(s);
      const X = logX(0.15, 2, 44, 344), Y = r => 260 - (X(r) - 44) / 300 * 240;
      [0.2, 0.5, 1, 2].forEach(v => { el('line', {x1: X(v), x2: X(v), y1: 20, y2: 260, class: 'ax'}, s); el('line', {x1: 44, x2: 344, y1: Y(v), y2: Y(v), class: 'ax'}, s); text(s, X(v), 276, fmt(v, 1), 'ax-text', 'middle'); text(s, 38, Y(v) + 4, fmt(v, 1), 'ax-text', 'end'); });
      text(s, 194, 296, T('exported ratio', 'cociente exportado'), 'ax-text', 'middle');
      text(s, 12, 140, T('band-passed', 'filtrado'), 'ax-text', 'middle').setAttribute('transform', 'rotate(-90 12 140)');
      el('line', {x1: X(0.15), y1: Y(0.15), x2: X(2), y2: Y(2), class: 'one'}, s);
      pts.forEach((p, i) => {
        const g = el('g', {tabindex: 0, role: 'img', 'aria-label': `${p.id}: ${fmt(p.exported, 3)} → ${fmt(p.filtered, 3)}`}, s);
        el('circle', {cx: X(p.exported), cy: Y(p.filtered), r: p.changes ? 7 : 5, class: (p.changes ? 'm-coral' : 'm-cyan') + ' ring pop', style: `transition-delay:${i * 20}ms`}, g);
        el('circle', {cx: X(p.exported), cy: Y(p.filtered), r: 12, class: 'hit'}, g);
        bindTip(g, host, tip, () => `<b>${p.id}</b><br>${fmt(p.exported, 3)} → ${fmt(p.filtered, 3)}${p.changes ? '<br>' + T('crosses 1', 'cruza 1') : ''}`);
        if(p.changes) text(s, X(p.exported) - 10, Y(p.filtered) - 12, 'patient7/iso180', 'lbl fade', 'end');
      });
    });
  }

  const SCEN = {
    exact_symmetry: ['Exact symmetry', 'Simetría exacta'], near_symmetry: ['Near symmetry', 'Casi simétrica'],
    clean_shared_carrier: ['Clean, shared carrier', 'Limpia, portadora común'], clean_independent_carrier: ['Clean, independent carrier', 'Limpia, portadora independiente'],
    common_gain: ['Common gain', 'Ganancia común'], asymmetric_noise: ['Asymmetric noise', 'Ruido asimétrico'],
    denominator_attenuation: ['Weak denominator', 'Denominador atenuado'], unequal_pause: ['Unequal pause', 'Pausa desigual'],
    single_spike_artifact: ['Single spike artefact', 'Artefacto de pico aislado'], sustained_true_event: ['Sustained true event', 'Evento real sostenido'],
    unequal_sensor_gain: ['Unequal sensor gain', 'Ganancia desigual del sensor'],
  };
  function heatmap(host){
    const {scenarios, methods, error} = D.synthetic, tip = tooltip(host);
    const lo = [27, 37, 55], mid = [232, 96, 60], hi = [255, 214, 196];
    const color = v => { const t = Math.min(1, Math.sqrt(v / 1.2)); const [a, b, u] = t < 0.6 ? [lo, mid, t / 0.6] : [mid, hi, (t - 0.6) / 0.4]; return `rgb(${a.map((c, i) => Math.round(c + (b[i] - c) * u)).join(',')})`; };
    onLang(() => {
      host.querySelector('svg')?.remove();
      const cw = 13, ch = 17, x0 = 150, y0 = 52;
      const s = el('svg', {viewBox: `0 0 ${x0 + methods.length * cw + 10} ${y0 + scenarios.length * ch + 30}`, role: 'img', 'aria-label': T('Heatmap of median error by scenario and method.', 'Mapa de calor del error mediano por escenario y método.')});
      host.prepend(s);
      methods.forEach((m, j) => { const t = text(s, x0 + j * cw + cw / 2, y0 - 6, shortName(m), 'ax-text', 'start'); t.setAttribute('transform', `rotate(-60 ${x0 + j * cw + cw / 2} ${y0 - 6})`); t.style.fontSize = '8.5px'; });
      scenarios.forEach((sc, i) => {
        text(s, x0 - 8, y0 + i * ch + ch / 2 + 4, T(...SCEN[sc]), 'lbl-m', 'end').style.fontSize = '11px';
        methods.forEach((m, j) => {
          const [e, mis] = error[`${sc}|${m}`];
          const r = el('rect', {x: x0 + j * cw, y: y0 + i * ch, width: cw - 2, height: ch - 2, rx: 2, fill: color(e), class: 'cell', tabindex: -1, style: `transition-delay:${(i + j) * 25}ms`}, s);
          bindTip(r, host, tip, () => `<b>${T(...SCEN[sc])}</b><br>${methodName(m)}<br>${T('median error', 'error mediano')} ${fmt(e, 3)} · ${T('direction flips', 'inversiones')} ${Math.round(mis * 100)}%`);
        });
      });
      const ly = y0 + scenarios.length * ch + 14;
      text(s, x0, ly + 10, T('low error', 'error bajo'), 'ax-text');
      for(let q = 0; q < 10; q++) el('rect', {x: x0 + 62 + q * 10, y: ly, width: 10, height: 10, fill: color(q / 9 * 1.2)}, s);
      text(s, x0 + 170, ly + 10, T('high error', 'error alto'), 'ax-text');
    });
  }

  function peopleChart(host){
    const chips = document.getElementById('people'), tip = tooltip(host);
    let current = D.people[0].id, dots = [];
    const all = D.people.flatMap(p => p.specs.map(s => s[1])).filter(v => v > 0);
    const lo = Math.min(...all) * 0.95, hi = Math.max(...all) * 1.05;
    const methods = D.people[0].specs.map(s => s[0]);
    const X = logX(lo, hi, 200, 980);
    const update = () => {
      const p = D.people.find(x => x.id === current);
      dots.forEach(({c, m}) => { const r = p.specs.find(s => s[0] === m)[1]; c.style.cx = X(r) + 'px'; c.setAttribute('class', (r >= 1 ? 'm-coral' : 'm-cyan') + ' ring'); c.dataset.r = r; });
      chips.querySelectorAll('button').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.id === current)));
      const sum = host.querySelector('.p-sum'); if(sum) sum.textContent = p.crosses ? T('Crosses 1: direction depends on the method', 'Cruza 1: la dirección depende del método') : T('Stays on one side of 1', 'Se mantiene de un lado del 1');
    };
    D.people.forEach(p => { const b = document.createElement('button'); b.type = 'button'; b.dataset.id = p.id; b.innerHTML = p.id + (p.crosses ? ' <span class="x">●</span>' : ''); b.addEventListener('click', () => { current = p.id; update(); }); chips.appendChild(b); });
    onLang(() => {
      host.querySelector('svg')?.remove(); host.querySelector('.p-sum')?.remove();
      const s = el('svg', {viewBox: `0 0 1000 ${methods.length * 22 + 50}`, role: 'img', 'aria-label': T('Ratios for the selected participant across 11 RMS methods.', 'Cocientes del participante seleccionado en 11 métodos RMS.')});
      host.prepend(s);
      const H = methods.length * 22 + 20;
      [0.8, 0.9, 1, 1.1, 1.2, 1.4].filter(v => v > lo && v < hi).forEach(v => { el('line', {x1: X(v), x2: X(v), y1: 6, y2: H, class: 'ax'}, s); text(s, X(v), H + 16, fmt(v, 1), 'ax-text', 'middle'); });
      el('line', {x1: X(1), x2: X(1), y1: 0, y2: H, class: 'one'}, s);
      dots = methods.map((m, i) => {
        const y = 18 + i * 22;
        text(s, 188, y + 4, methodName(m), 'ax-text', 'end');
        el('line', {x1: 200, x2: 980, y1: y, y2: y, class: 'ax', opacity: .5}, s);
        const c = el('circle', {cx: X(1), cy: y, r: 6.5, class: 'm-cyan ring', tabindex: 0}, s);
        c.style.transition = reduce ? 'none' : 'cx .7s cubic-bezier(.2,.8,.2,1), fill .4s';
        bindTip(c, host, tip, () => `<b>${current}</b> · ${methodName(m)}<br>${T('right / left', 'derecha / izquierda')} ${fmt(+c.dataset.r, 3)}`);
        return {c, m};
      });
      const p = document.createElement('p'); p.className = 'p-sum small'; p.style.cssText = 'margin:6px 0 0;font-weight:600'; host.appendChild(p);
      update();
    });
  }

  /* ---------- signal lab (synthetic, computed live) ---------- */
  function signalLab(root){
    const N = 4096, cv = root.querySelector('canvas'), ctx = cv.getContext('2d');
    const sp = root.querySelector('#sl-spike'), pa = root.querySelector('#sl-pause'), ga = root.querySelector('#sl-gain');
    const rng = seed => () => { seed |= 0; seed = seed + 0x6D2B79F5 | 0; let t = Math.imul(seed ^ seed >>> 15, 1 | seed); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; };
    const gauss = r => () => Math.sqrt(-2 * Math.log(1 - r())) * Math.cos(2 * Math.PI * r());
    const env = i => 0.6 + 0.4 * Math.pow(Math.sin(i / N * Math.PI * 8), 2);
    const gl = gauss(rng(11)), gr = gauss(rng(29));
    const baseL = Float64Array.from({length: N}, (_, i) => gl() * env(i) * 1.10);
    const baseR = Float64Array.from({length: N}, (_, i) => gr() * env(i));
    const rms = a => Math.sqrt(a.reduce((s, v) => s + v * v, 0) / a.length);
    const quantile = (a, q) => { const b = Float64Array.from(a).sort(); const pos = (b.length - 1) * q, i = Math.floor(pos); return b[i] + (b[Math.min(i + 1, b.length - 1)] - b[i]) * (pos - i); };
    const capped = a => { const c = quantile(a.map(Math.abs), 0.995); return rms(a.map(v => Math.max(-c, Math.min(c, v)))); };
    const blocks = a => {
      const size = 256, br = [];
      for(let i = 0; i + size <= a.length; i += size) br.push(rms(a.subarray(i, i + size)));
      const lo = quantile(br, 0.2), hi = quantile(br, 0.9), thr = lo + 0.1 * (hi - lo), sel = [];
      br.forEach((v, k) => { if(v > thr) for(let i = k * size; i < (k + 1) * size; i++) sel.push(a[i]); });
      return sel.length ? rms(sel) : NaN;
    };
    const pin = (id, r) => { const p = root.querySelector('#p-' + id), v = Math.max(-1, Math.min(1, Math.log(r) / Math.log(2))); p.style.left = (50 + v * 50) + '%'; p.style.background = r >= 1 ? 'var(--coral)' : 'var(--cyan)'; root.querySelector('#r-' + id).textContent = isFinite(r) ? fmt(r) : '—'; };
    function run(){
      const spike = +sp.value, pause = +pa.value / 100, gain = +ga.value / 100;
      const L = Float64Array.from(baseL), R = Float64Array.from(baseR);
      if(spike) for(let i = 2000; i < 2012; i++) L[i] += spike * 0.2 * (i % 2 ? 1 : -1);
      const p0 = Math.floor(N * (0.5 - pause / 2)), p1 = Math.floor(N * (0.5 + pause / 2));
      for(let i = p0; i < p1; i++) R[i] *= 0.02;
      for(let i = 0; i < N; i++) R[i] *= gain;
      root.querySelector('#o-spike').textContent = fmt(spike * 0.2, 1) + '×';
      root.querySelector('#o-pause').textContent = Math.round(pause * 100) + '%';
      root.querySelector('#o-gain').textContent = fmt(gain) + '×';
      pin('whole', rms(L) / rms(R)); pin('cap', capped(L) / capped(R)); pin('block', blocks(L) / blocks(R));
      const W = cv.width, H = cv.height;
      ctx.clearRect(0, 0, W, H);
      const draw = (a, y0, color, label) => {
        ctx.beginPath(); ctx.strokeStyle = color; ctx.lineWidth = 1.2;
        const step = a.length / W;
        for(let x = 0; x < W; x++){ let mx = 0; for(let i = Math.floor(x * step); i < Math.floor((x + 1) * step); i++) if(Math.abs(a[i]) > Math.abs(mx)) mx = a[i]; const y = y0 - Math.max(-90, Math.min(90, mx * 26)); x ? ctx.lineTo(x, y) : ctx.moveTo(x, y); }
        ctx.stroke(); ctx.fillStyle = color; ctx.font = '600 20px JetBrains Mono, monospace'; ctx.fillText(label, 10, y0 - 66);
      };
      draw(L, H * 0.27, '#5fd4f5', 'L'); draw(R, H * 0.75, '#ff8a65', 'R');
    }
    [sp, pa, ga].forEach(i => i.addEventListener('input', run));
    root.querySelector('#lab-reset').addEventListener('click', () => { sp.value = 0; pa.value = 0; ga.value = 100; run(); });
    onLang(run);
  }

  const charts = {ratioDemo, ribbons, bandpass, heatmap, people: peopleChart};
  if(D) document.querySelectorAll('[data-chart]').forEach(h => charts[h.dataset.chart]?.(h));
  const lab = document.getElementById('signal-lab'); if(lab) signalLab(lab);
  window.aclFigures?.forEach(fn => fn({el, text, T, fmt, onLang, tooltip, bindTip}));
  document.querySelectorAll('.reveal,.viz,[data-count]').forEach(n => io.observe(n));
})();
