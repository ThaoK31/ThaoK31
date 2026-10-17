"""The header of the GitHub profile, set on the page of GitHub itself, without a card: the name, one line of role, and an
effort curve that draws itself once, slowly, ending on the only yellow point. One file per theme of GitHub, in its own
colors. Fonts embedded (Barlow, OFL), no request to a third party. Usage: python header.py <fonts dir> <out dir>"""
import base64
import math
import sys
from pathlib import Path

FONTS, OUT = Path(sys.argv[1]), Path(sys.argv[2])
font = lambda name: base64.b64encode((FONTS / name).read_bytes()).decode()
THEMES = {"dark": {"text": "#E6EDF3", "muted": "#9198A1", "grid": "#262C36", "dot": "#F0CF4C"},
          "light": {"text": "#1F2328", "muted": "#59636E", "grid": "#D8DEE4", "dot": "#BF8700"}}
X, Y, W, H = 56, 84, 1168, 188  # the view, cut around the name and the curve

# An effort: a warm-up, three efforts with their recoveries, a cool-down. Deterministic jitter, as a watch would draw it.
levels = [(0.00, 250), (0.10, 175), (0.18, 165), (0.24, 118), (0.33, 121), (0.36, 168), (0.42, 166), (0.45, 112),
          (0.54, 116), (0.57, 166), (0.63, 163), (0.66, 106), (0.76, 110), (0.80, 170), (0.90, 196), (1.00, 214)]
x0, x1 = 700, 1196
points = []
for step in range(0, 241):
    t = step / 240
    for (ta, ya), (tb, yb) in zip(levels, levels[1:]):
        if ta <= t <= tb:
            k = (t - ta) / (tb - ta)
            k = k * k * (3 - 2 * k)
            y = ya + (yb - ya) * k
            break
    y += 2.2 * math.sin(step * 1.7) + 1.4 * math.sin(step * 0.53 + 1)
    points.append((x0 + (x1 - x0) * t, y))
trace = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in points)
end_x, end_y = points[-1]
faces = (f'@font-face {{ font-family: "Barlow Semi Condensed"; font-weight: 600; src: url(data:font/woff2;base64,'
         f'{font("barlow-semi-condensed-600.woff2")}) format("woff2"); }}\n'
         f'@font-face {{ font-family: "Barlow"; font-weight: 400; src: url(data:font/woff2;base64,{font("barlow-400.woff2")}) '
         f'format("woff2"); }}')

for theme, c in THEMES.items():
    grid = "".join(f'<line x1="{x0}" x2="{x1}" y1="{y}" y2="{y}" stroke="{c["grid"]}" stroke-width="1"/>' for y in (110, 170, 230))
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="{X} {Y} {W} {H}" role="img">
<title>Lucas Remery, full-stack developer</title>
<style>
{faces}
.name {{ font: 600 92px "Barlow Semi Condensed", "Arial Narrow", sans-serif; fill: {c["text"]}; }}
.role {{ font: 400 28px "Barlow", Arial, sans-serif; fill: {c["muted"]}; }}
.trace {{ fill: none; stroke: {c["text"]}; stroke-width: 3; stroke-linejoin: round; stroke-linecap: round;
  stroke-dasharray: 1; stroke-dashoffset: 1; animation: draw 4.5s cubic-bezier(.45, 0, .2, 1) .4s forwards; }}
.dot {{ fill: {c["dot"]}; opacity: 0; animation: appear .6s ease-out 4.9s forwards, breathe 3.2s ease-in-out 5.5s infinite; }}
@keyframes draw {{ to {{ stroke-dashoffset: 0; }} }}
@keyframes appear {{ to {{ opacity: 1; }} }}
@keyframes breathe {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: .35; }} }}
@media (prefers-reduced-motion: reduce) {{ .trace {{ animation: none; stroke-dashoffset: 0; }} .dot {{ animation: none; opacity: 1; }} }}
</style>
<text class="name" x="80" y="196">Lucas Remery</text>
<text class="role" x="84" y="246">Full-stack developer</text>
{grid}
<path class="trace" pathLength="1" d="{trace}"/>
<circle class="dot" cx="{end_x:.1f}" cy="{end_y:.1f}" r="7"/>
</svg>'''
    (OUT / f"header-{theme}.svg").write_text(svg, encoding="utf-8")
    print(f"header-{theme}.svg", len(svg) // 1024, "KB")
