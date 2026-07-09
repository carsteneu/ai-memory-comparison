#!/usr/bin/env python3
"""Generate star-history.svg from GitHub API stargazer data.

Uses Handlee font (OFL, public domain) embedded as WOFF2.
Style mimics star-history.com: xkcd-like sketch filter, red line, bold labels.

Requirements: Python 3 + gh CLI (authenticated).
Note: GitHub's stargazers API now requires repo admin/collaborator access
since 2026 API changes. Run as the repo owner.
"""
import subprocess, math, base64
from datetime import datetime

# --- Configuration ---
REPO = "carsteneu/ai-memory-comparison"
LINE_COLOR = "#dd4528"
FONT_FILE = "tools/handlee-subset.woff2"
OUTPUT = "star-history.svg"

# --- Fetch star data ---
result = subprocess.run(
    ['gh', 'api', '-H', 'Accept: application/vnd.github.v3.star+json',
     f'/repos/{REPO}/stargazers', '--paginate',
     '--jq', '.[].starred_at'],
    capture_output=True, text=True, timeout=30
)
dates = sorted([line.strip() for line in result.stdout.strip().split('\n') if line.strip()])

daily = {}
for d in dates:
    day = d[:10]
    daily[day] = daily.get(day, 0) + 1

cum_data = []
total = 0
for day in sorted(daily.keys()):
    total += daily[day]
    cum_data.append((day, total))

# --- Dimensions ---
w, h = 800, 533
pad_l, pad_r, pad_t, pad_b = 60, 35, 80, 70
plot_w, plot_h = w - pad_l - pad_r, h - pad_t - pad_b

max_stars = cum_data[-1][1]
y_max = math.ceil(max_stars / 25) * 25

first_date = datetime.fromisoformat(cum_data[0][0])
last_date = datetime.fromisoformat(cum_data[-1][0])
date_range = (last_date - first_date).days or 1

# --- Compute points ---
points = []
for day, count in cum_data:
    dt = datetime.fromisoformat(day)
    x = pad_l + ((dt - first_date).days / date_range) * plot_w
    y = pad_t + plot_h - (count / y_max) * plot_h
    points.append((x, y))

# --- Smooth Catmull-Rom curve ---
def smooth_path(pts):
    if len(pts) < 2:
        return ""
    p = f"M {pts[0][0]:.1f},{pts[0][1]:.1f}"
    for i in range(len(pts) - 1):
        p0 = pts[max(0, i-1)]
        p1 = pts[i]
        p2 = pts[i+1]
        p3 = pts[min(len(pts)-1, i+2)]
        cp1x = p1[0] + (p2[0] - p0[0]) / 6
        cp1y = p1[1] + (p2[1] - p0[1]) / 6
        cp2x = p2[0] - (p3[0] - p1[0]) / 6
        cp2y = p2[1] - (p3[1] - p1[1]) / 6
        p += f" C {cp1x:.1f},{cp1y:.1f} {cp2x:.1f},{cp2y:.1f} {p2[0]:.1f},{p2[1]:.1f}"
    return p

line_path = smooth_path(points)
area_path = line_path + f" L {points[-1][0]:.1f},{pad_t + plot_h:.1f} L {points[0][0]:.1f},{pad_t + plot_h:.1f} Z"

# --- Load embedded font ---
import os
if not os.path.exists(FONT_FILE):
    print(f"ERROR: font file {FONT_FILE} not found")
    print("Generate it with:")
    print("  curl -sL 'https://github.com/google/fonts/raw/main/ofl/handlee/Handlee-Regular.ttf' -o /tmp/handlee.ttf")
    print(f"  pyftsubset /tmp/handlee.ttf --text='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789 /.:-' --output-file={FONT_FILE} --flavor=woff2 --no-hinting --desubroutinize")
    exit(1)

with open(FONT_FILE, 'rb') as f:
    font_b64 = base64.b64encode(f.read()).decode()

# --- Helpers ---
FF = "Handlee, cursive"
XKCD = ' filter="url(#xkcdify)"'
AXIS_COLOR = "#222"

def fmt(n):
    """Format numbers: 1000 -> 1K, 2500 -> 2.5K."""
    if n >= 1000:
        v = n / 1000
        return f"{v:g}K" if v != int(v) else f"{int(v)}K"
    return str(n)

def text_el(x, y, content, size=16, weight='bold', fill='#000', anchor=None, transform=None):
    attrs = [f'x="{x}"', f'y="{y}"', f'fill="{fill}"', f'font-size="{size}"', f'font-family="{FF}"', f'font-weight="{weight}"']
    if anchor:
        attrs.append(f'text-anchor="{anchor}"')
    if transform:
        attrs.append(f'transform="{transform}"')
    return f'<text {" ".join(attrs)}>{content}</text>'

# --- Legend ---
char_w = 7.5
text_w = len(REPO) * char_w
legend_h = 32
legend_pad = 10
swatch = 8
swatch_gap = 8
legend_w = text_w + swatch + swatch_gap + legend_pad * 2 + 7
legend_x = pad_l + 15
legend_y = pad_t + 10

legend = (
    f'<rect width="{legend_w:.0f}" height="{legend_h}" x="{legend_x}" y="{legend_y}" '
    f'fill="#fff" fill-opacity="0.9" stroke="#000" stroke-width="1.5" rx="4" ry="4"{XKCD}/>'
    f'<rect width="{swatch}" height="{swatch}" x="{legend_x + legend_pad}" y="{legend_y + 12}" '
    f'rx="2" ry="2" fill="{LINE_COLOR}"{XKCD}/>'
    + text_el(legend_x + legend_pad + swatch + swatch_gap, legend_y + 20, REPO, size=15)
)

# --- Y-axis ---
y_elements = []
for i in range(0, y_max + 1, 25):
    y_val = pad_t + plot_h - (i / y_max) * plot_h
    if i > 0:
        y_elements.append(
            f'<line x1="{pad_l}" y1="{y_val:.1f}" x2="{w - pad_r}" y2="{y_val:.1f}" '
            f'stroke="#eee" stroke-width="1"{XKCD}/>'
        )
    y_elements.append(text_el(pad_l - 29, y_val + 5, fmt(i)))

y_elements.append(text_el(6, pad_t + plot_h/2, 'GitHub Stars', size=17,
                          transform=f'rotate(-90, 6, {pad_t + plot_h/2:.1f})'))

# --- X-axis ---
prev_month = None
month_positions = []
for day, count in cum_data:
    dt = datetime.fromisoformat(day)
    x = pad_l + ((dt - first_date).days / date_range) * plot_w
    month_key = dt.strftime("%Y-%m")
    if month_key != prev_month:
        month_positions.append((x, dt))
        prev_month = month_key

x_labels = []
for i, (x, dt) in enumerate(month_positions):
    cx = (x + month_positions[i+1][0]) / 2 if i < len(month_positions) - 1 else (x + (w - pad_r)) / 2
    x_labels.append(text_el(f'{cx:.1f}', pad_t + plot_h + 25, dt.strftime('%b %Y')))
x_labels.append(text_el('50%', h - 8, 'Date', size=17))

# --- End label ---
last_x, last_y = points[-1]
label_x = min(last_x + 12, w - pad_r - 30)
label_y = max(last_y - 8, pad_t + 20)

# --- Assemble SVG ---
svg_parts = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" height="auto">',
    '  <defs>',
    f'    <style>@font-face{{font-family:"Handlee";src:url(data:font/woff2;charset=utf-8;base64,{font_b64}) format("woff2")}}</style>',
    '    <filter id="xkcdify" width="100%" height="100%" x="-5" y="-5" filterUnits="userSpaceOnUse">',
    '      <feTurbulence baseFrequency=".05" result="noise" type="fractalNoise"/>',
    '      <feDisplacementMap in="SourceGraphic" in2="noise" scale="3" xChannelSelector="R" yChannelSelector="G"/>',
    '    </filter>',
    f'    <linearGradient id="g" x1="0" y1="0" x2="0" y2="1">',
    f'      <stop offset="0%" stop-color="{LINE_COLOR}" stop-opacity="0.22"/>',
    f'      <stop offset="100%" stop-color="{LINE_COLOR}" stop-opacity="0.02"/>',
    '    </linearGradient>',
    '  </defs>',
    f'  <rect width="{w}" height="{h}" fill="#fff"/>',
    text_el('50%', 30, 'Star History', size=20, anchor='middle'),
    '  ' + legend,
] + ['  ' + el for el in y_elements] + ['  ' + el for el in x_labels] + [
    f'  <line x1="{pad_l}" y1="{pad_t}" x2="{pad_l}" y2="{pad_t + plot_h}" stroke="{AXIS_COLOR}" stroke-width="2.5"{XKCD}/>',
    f'  <line x1="{pad_l}" y1="{pad_t + plot_h}" x2="{w - pad_r}" y2="{pad_t + plot_h}" stroke="{AXIS_COLOR}" stroke-width="2.5"{XKCD}/>',
    f'  <path d="{area_path}" fill="url(#g)"/>',
    f'  <path d="{line_path}" fill="none" stroke="{LINE_COLOR}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"{XKCD}/>',
    f'  <circle cx="{last_x:.1f}" cy="{last_y:.1f}" r="5" fill="{LINE_COLOR}" stroke="#fff" stroke-width="2"{XKCD}/>',
    text_el(f'{label_x:.1f}', f'{label_y:.1f}', max_stars, size=18, fill=LINE_COLOR),
    '</svg>'
]

svg = '\n'.join(svg_parts)
with open(OUTPUT, 'w') as f:
    f.write(svg)

# --- Validate ---
import xml.etree.ElementTree as ET
try:
    ET.fromstring(svg)
    print(f'OK: {len(svg)} chars ({len(svg)/1024:.0f}KB), {max_stars} stars, y_max={y_max}')
except ET.ParseError as e:
    print(f'XML ERROR: {e}')
    exit(1)
