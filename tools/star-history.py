#!/usr/bin/env python3
"""Generate star-history.svg from GitHub API stargazer data."""
import subprocess, os
from datetime import datetime

result = subprocess.run(
    ['gh', 'api', '-H', 'Accept: application/vnd.github.v3.star+json',
     '/repos/carsteneu/ai-memory-comparison/stargazers', '--paginate',
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

w, h = 800, 360
pad_l, pad_r, pad_t, pad_b = 60, 20, 30, 50
plot_w, plot_h = w - pad_l - pad_r, h - pad_t - pad_b

max_stars = cum_data[-1][1]
first_date = datetime.fromisoformat(cum_data[0][0])
last_date = datetime.fromisoformat(cum_data[-1][0])
date_range = (last_date - first_date).days or 1

points = []
for day, count in cum_data:
    dt = datetime.fromisoformat(day)
    x = pad_l + ((dt - first_date).days / date_range) * plot_w
    y = pad_t + plot_h - (count / max_stars) * plot_h
    points.append((x, y))

# Paths
path_d = f"M {points[0][0]},{points[0][1]}"
for x, y in points[1:]:
    path_d += f" L {x},{y}"
area_d = path_d + f" L {points[-1][0]},{pad_t + plot_h} L {points[0][0]},{pad_t + plot_h} Z"

# Y-axis
y_lines = []
for i in range(25, max_stars + 1, 25):
    y = pad_t + plot_h - (i / max_stars) * plot_h
    y_lines.append(f'<line x1="{pad_l - 5}" y1="{y:.1f}" x2="{pad_l}" y2="{y:.1f}" stroke="#30363d"/>')
    y_lines.append(f'<text x="{pad_l - 8}" y="{y + 4:.1f}" text-anchor="end" fill="#8b949e" font-size="11">{i}</text>')
    y_lines.append(f'<line x1="{pad_l}" y1="{y:.1f}" x2="{w - pad_r}" y2="{y:.1f}" stroke="#30363d" stroke-dasharray="2,4" opacity="0.15"/>')

# X-axis
x_labels = []
for day, count in cum_data:
    dt = datetime.fromisoformat(day)
    x = pad_l + ((dt - first_date).days / date_range) * plot_w
    if dt.day in (1, 15) or count == max_stars:
        x_labels.append(f'<text x="{x:.1f}" y="{pad_t + plot_h + 18}" text-anchor="middle" fill="#8b949e" font-size="10">{dt.strftime("%b %d")}</text>')

last_x, last_y = points[-1]

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" height="auto">
  <rect width="{w}" height="{h}" fill="#0d1117"/>
  {"".join(y_lines)}
  {"".join(x_labels)}
  <line x1="{pad_l}" y1="{pad_t + plot_h}" x2="{w - pad_r}" y2="{pad_t + plot_h}" stroke="#30363d"/>
  <path d="{area_d}" fill="#e3b341" opacity="0.15"/>
  <path d="{path_d}" fill="none" stroke="#e3b341" stroke-width="2.5"/>
  <circle cx="{last_x:.1f}" cy="{last_y:.1f}" r="4" fill="#e3b341"/>
  <text x="{last_x + 10:.1f}" y="{last_y - 8:.1f}" fill="#e3b341" font-size="13" font-weight="bold">{max_stars}</text>
</svg>'''

out = 'star-history.svg'
with open(out, 'w') as f:
    f.write(svg)
print(f'Generated {out}: {max_stars} stars, {first_date.strftime("%b %d")} – {last_date.strftime("%b %d")}')
