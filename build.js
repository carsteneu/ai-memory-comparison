// Static pre-render: agent-readable HTML + comparison.md
// Reads data.js → writes <thead>/<tbody> into index.html and rewrites comparison.md.
// Usage: node build.js

const fs = require('fs');
const path = require('path');
const vm = require('vm');

const ROOT = __dirname;
const DATA = path.join(ROOT, 'data.js');
const HTML = path.join(ROOT, 'index.html');
const MD   = path.join(ROOT, 'comparison.md');

const ctx = { window: {}, document: {} };
vm.createContext(ctx);
const src = fs.readFileSync(DATA, 'utf8') + '\nthis.SYSTEMS=SYSTEMS;this.FEATURE_GROUPS=FEATURE_GROUPS;';
vm.runInContext(src, ctx);
const SYSTEMS = ctx.SYSTEMS;
const FEATURE_GROUPS = ctx.FEATURE_GROUPS;

function escapeHtml(s) {
  return String(s == null ? '' : s)
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;').replace(/'/g, '&#39;');
}

function fmt(val, type, id) {
  if (type === 'bool') return val === true ? '✅' : '—';
  if (type === 'number') return String(val) + (id === 'coverage' ? '%' : '');
  return val || '—';
}
function cls(val, type) {
  if (type === 'bool') return val === true ? 'yes' : 'no';
  if (type === 'number') return 'num';
  return 'txt';
}
function fmtStars(n) {
  if (!n && n !== 0) return '?';
  if (n >= 1000) return (n / 1000).toFixed(1).replace(/\.0$/, '') + 'k';
  return String(n);
}

const features = [];
const groups = [];
for (const g of FEATURE_GROUPS) {
  for (const f of g.features) features.push({ f, glabel: g.label });
  groups.push({ label: g.label, span: g.features.length });
}

const allBool = features
  .map(x => x.f)
  .filter(f => f.type === 'bool' && f.id !== 'coverage')
  .map(f => f.id);

for (const s of SYSTEMS) {
  let hits = 0;
  for (const id of allBool) if (s[id] === true) hits++;
  s.coverage = Math.round(hits / allBool.length * 100);
}

const filtered = SYSTEMS.slice().sort((a, b) => (a.stars || 0) - (b.stars || 0));

const bestVals = {};
for (const x of features) {
  if (x.f.type !== 'number') continue;
  let max = -1;
  for (const s of filtered) if (typeof s[x.f.id] === 'number' && s[x.f.id] > max) max = s[x.f.id];
  bestVals[x.f.id] = max;
}

const theadParts = [];
let secRow = '<tr><th class="sys-h sortable" data-key="name">System</th><th class="desc-h" rowspan="2">Description</th>';
for (const g of groups) secRow += `<th class="sec" colspan="${g.span}">${escapeHtml(g.label)}</th>`;
secRow += '</tr>';
theadParts.push(secRow);

let featRow = `<tr><th class="sys-h sortable" data-key="stars">${filtered.length} systems</th>`;
for (const x of features) featRow += `<th class="feat sortable" data-key="${x.f.id}">${escapeHtml(x.f.label)}</th>`;
featRow += '</tr>';
theadParts.push(featRow);

const tbodyParts = [];
for (const sys of filtered) {
  let row = '<tr>';
  const href = sys.evidence || sys.docs || sys.url;
  row += `<td class="sys-c"><a href="${escapeHtml(href)}" class="src" title="Evidence &amp; sources">📋</a> <a href="${escapeHtml(sys.url)}" target="_blank">${escapeHtml(sys.name)}</a>${sys.authorPick ? '<span class="pick" title="Author&#39;s Pick">★ Pick</span>' : ''}<span class="stars">⭐${fmtStars(sys.stars)} · ${escapeHtml(sys.created || '')}</span></td>`;
  row += `<td class="desc">${escapeHtml(sys.description || '')}</td>`;
  for (const x of features) {
    const f = x.f, val = sys[f.id];
    let cclass = cls(val, f.type);
    if (f.type === 'number' && val === bestVals[f.id] && val > 0 && filtered.length > 1) cclass += ' best';
    row += `<td class="${cclass}">${escapeHtml(fmt(val, f.type, f.id))}</td>`;
  }
  row += '</tr>';
  tbodyParts.push(row);
}

const theadHtml = theadParts.join('\n      ');
const tbodyHtml = tbodyParts.join('\n      ');

let html = fs.readFileSync(HTML, 'utf8');
html = html.replace(
  /<thead id="thead">[\s\S]*?<\/thead>/,
  `<thead id="thead">\n      ${theadHtml}\n    </thead>`
);
html = html.replace(
  /<tbody id="tbody">[\s\S]*?<\/tbody>/,
  `<tbody id="tbody">\n      ${tbodyHtml}\n    </tbody>`
);
fs.writeFileSync(HTML, html);

const today = new Date().toISOString().split('T')[0];
const mdParts = [];
mdParts.push('# AI Memory Systems — Feature-Level Comparison');
mdParts.push('');
mdParts.push('> **Open-source fact table.** Every claim links to public README, docs, or source.');
mdParts.push('> Corrections via PR welcome. No affiliation with any listed project.');
mdParts.push('');
mdParts.push(`**Last updated:** ${today}  `);
mdParts.push(`**Systems:** ${filtered.length}  `);
mdParts.push(`**Live:** [carsteneu.github.io/ai-memory-comparison](https://carsteneu.github.io/ai-memory-comparison/)`);
mdParts.push('');
mdParts.push('---');
mdParts.push('');
mdParts.push('## Systems Overview');
mdParts.push('');
mdParts.push('| System | Stars | Lang | License | Created | Description |');
mdParts.push('|---|---:|---|---|---|---|');
for (const s of filtered) {
  mdParts.push(`| [${s.name}](${s.url}) | ${s.stars || '?'} | ${s.language || '?'} | ${s.license || '?'} | ${s.created || '?'} | ${(s.description || '').replace(/\|/g, '\\|')} |`);
}
mdParts.push('');
for (const g of FEATURE_GROUPS) {
  mdParts.push('---');
  mdParts.push('');
  mdParts.push(`## ${g.label}`);
  mdParts.push('');
  const header = ['System', ...g.features.map(f => f.label)];
  const sep = header.map(() => '---');
  mdParts.push('| ' + header.join(' | ') + ' |');
  mdParts.push('| ' + sep.join(' | ') + ' |');
  for (const s of filtered) {
    const cells = [s.name];
    for (const f of g.features) {
      const v = s[f.id];
      if (f.type === 'bool') cells.push(v === true ? '✅' : '—');
      else if (f.type === 'number') cells.push(String(v) + (f.id === 'coverage' ? '%' : ''));
      else cells.push(String(v || '—').replace(/\|/g, '\\|'));
    }
    mdParts.push('| ' + cells.join(' | ') + ' |');
  }
  mdParts.push('');
}
mdParts.push('---');
mdParts.push('');
mdParts.push('*Auto-generated from `data.js` via `build.js`. Do not edit this file directly.*');
mdParts.push('');

fs.writeFileSync(MD, mdParts.join('\n'));

console.log(`Built ${filtered.length} systems × ${features.length} features.`);
console.log(`Updated: ${path.relative(ROOT, HTML)}, ${path.relative(ROOT, MD)}`);
