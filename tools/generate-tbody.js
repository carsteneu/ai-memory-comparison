// Generate static HTML tbody from data.js
const fs = require('fs');
const src = fs.readFileSync('data.js', 'utf8');

// Wrap in IIFE to capture const variables
const wrapped = '(function() { ' + src + '; return { FEATURE_GROUPS, SYSTEMS }; })()';
const data = eval(wrapped);
const { FEATURE_GROUPS, SYSTEMS } = data;

// Build flat feature list
const features = [];
for (const g of FEATURE_GROUPS) {
  for (const f of g.features) {
    features.push(f);
  }
}

// Best numeric values
const bestVals = {};
for (const f of features) {
  if (f.type !== 'number') continue;
  let max = -1;
  for (const s of SYSTEMS) {
    const v = s[f.id];
    if (typeof v === 'number' && v > max) max = v;
  }
  bestVals[f.id] = max;
}

// Compute coverage for each system
const allBool = [];
for (const f of features) {
  if (f.type === 'bool' && f.id !== 'coverage') allBool.push(f.id);
}
for (const s of SYSTEMS) {
  let hits = 0;
  for (const b of allBool) {
    if (s[b] === true) hits++;
  }
  s.coverage = Math.round(hits / allBool.length * 100);
  if (s.coverage > (bestVals.coverage || 0)) bestVals.coverage = s.coverage;
}

function fmtStars(n) {
  if (!n) return '0';
  if (n >= 1000) return (n / 1000).toFixed(n >= 10000 ? 1 : 1) + 'k';
  return String(n);
}

function fmt(val, type) {
  if (type === 'bool') return val === true ? '✅' : '—';
  if (type === 'number') return String(val ?? '—');
  return val || '—';
}

function cls(val, type, fid) {
  if (val === true) return 'yes';
  if (val === false) return 'no';
  if (type === 'number') {
    let c = 'num';
    if (val === bestVals[fid] && val > 0 && SYSTEMS.length > 1) c += ' best';
    return c;
  }
  return 'txt';
}

// Sort by stars ascending (default)
const sorted = [...SYSTEMS].sort((a, b) => (a.stars || 0) - (b.stars || 0));

let html = '';
for (const sys of sorted) {
  html += '      <tr data-id="' + sys.id + '">';
  html += '<td class="sys-c"><input type="checkbox" class="cmp-cb" data-id="' + sys.id + '"> <a href="' + (sys.evidence || sys.docs || sys.url) + '" class="src" title="Evidence &amp; sources">📋</a> <a href="' + sys.url + '" target="_blank">' + sys.name + '</a><span class="stars">⭐' + fmtStars(sys.stars) + ' · ' + (sys.created || '') + '</span></td>';
  html += '<td class="desc">' + (sys.description || '') + '</td>';
  for (const f of features) {
    const val = sys[f.id];
    html += '<td class="' + cls(val, f.type, f.id) + '">' + fmt(val, f.type) + '</td>';
  }
  html += '</tr>\n';
}

// Replace tbody content
let idx = fs.readFileSync('index.html', 'utf8');
idx = idx.replace(/<tbody id="tbody">[\s\S]*?<\/tbody>/, '<tbody id="tbody">\n' + html + '    </tbody>');
fs.writeFileSync('index.html', idx);

console.log('Generated ' + sorted.length + ' system rows');
console.log('Features per row: ' + features.length);
console.log('Total lines: ' + idx.split('\n').length);
