"""The stack of the GitHub profile, set on the page of GitHub itself, without a card: one row per category, its name on the
left, then monochrome icons of the Simple Icons set (CC0), drawn from react-icons on this PC or from the SVG files of Simple
Icons 16.35.0, the cup of Java from Font Awesome 6.4.2 (CC BY 4.0, credited in the file), and the mark of TypeSafe for Jev, cut out of the icon of its site. One file per theme of GitHub, in its own
colors. Barlow (OFL) embedded, no request to a third party.
Usage: python stack.py <react-icons si/index.js> <simple-icons dir> <barlow-400.woff2> <typesafe icon png> <out dir>"""
import base64
import io
import re
import sys
from pathlib import Path

from PIL import Image

SOURCE, LOCAL, FONT, JEV, OUT = (Path(arg) for arg in sys.argv[1:6])
THEMES = {"dark": {"icon": "#E6EDF3", "label": "#9198A1"}, "light": {"icon": "#1F2328", "label": "#59636E"}}
ROWS = [  # (category, [(react-icons component, Simple Icons file or "jev", label)])
    ("Languages", [("SiTypescript", "TypeScript"), ("SiJavascript", "JavaScript"), ("SiPython", "Python"), ("SiPhp", "PHP"),
                   ("SiPerl", "Perl"), ("FaJava", "Java"),
                   ("SiKotlin", "Kotlin"), ("SiCsharp", "C#"), ("SiCplusplus", "C++")]),
    ("Frontend", [("SiReact", "React"), ("SiNextdotjs", "Next.js"), ("SiVuedotjs", "Vue"), ("SiTailwindcss", "Tailwind CSS"),
                  ("shadcnui.svg", "shadcn/ui"), ("SiVite", "Vite"), ("SiThreedotjs", "Three.js"), ("SiGreensock", "GSAP"),
                  ("SiFigma", "Figma")]),
    ("Backend", [("SiNodedotjs", "Node.js"), ("SiExpress", "Express"), ("SiFastapi", "FastAPI"), ("SiDjango", "Django"),
                 ("SiPrisma", "Prisma"), ("SiSocketdotio", "Socket.io")]),
    ("Data", [("SiPostgresql", "PostgreSQL"), ("SiMysql", "MySQL"), ("SiSqlite", "SQLite"), ("SiMongodb", "MongoDB"),
              ("SiRedis", "Redis"), ("SiSupabase", "Supabase")]),
    ("Testing", [("SiVitest", "Vitest"), ("SiJest", "Jest"), ("SiPlaywright", "Playwright"), ("SiPytest", "Pytest")]),
    ("DevOps", [("SiDocker", "Docker"), ("SiGithubactions", "GitHub Actions"), ("SiGitlab", "GitLab CI"), ("SiNginx", "Nginx"),
                ("SiLinux", "Linux")]),
    ("AI", [("claude.svg", "Claude Code"), ("SiOpenai", "OpenAI (Codex, ChatGPT)"), ("googlegemini.svg", "Gemini"),
            ("ollama.svg", "Ollama"), ("modelcontextprotocol.svg", "MCP"), ("elevenlabs.svg", "ElevenLabs"), ("suno.svg", "Suno"),
            ("jev", "Jev")]),
]
ICON, GAP, ROW, LABEL, PAD = 28, 18, 46, 112, 4
text = SOURCE.read_text(encoding="utf-8")
awesome = (SOURCE.parent.parent / "fa6" / "index.js").read_text(encoding="utf-8")


def paths(name):
    if name.endswith(".svg"):
        return re.findall(r'<path[^>]* d="([^"]+)"', (LOCAL / name).read_text(encoding="utf-8"))
    match = re.search(r"module\.exports\." + name + r" = function " + name + r" \(props\) \{\s*return GenIcon\((\{.*?\})\)\(props\);",
                      awesome if name.startswith("Fa") else text, re.S)
    return re.findall(r'"d":"([^"]+)"', match.group(1)) if match else []


def box(name):
    """Width and height of the view box of an icon: 24 for Simple Icons, its own for Font Awesome."""
    if not name.startswith("Fa"):
        return 24, 24
    match = re.search(r"module\.exports\." + name + r" = function " + name
                      + r' \(props\) \{\s*return GenIcon\(\{"tag":"svg","attr":\{"viewBox":"0 0 (\d+) (\d+)"', awesome)
    return int(match.group(1)), int(match.group(2))


def jev_mark(color):
    """The dark mark of the icon of TypeSafe, without its pink disc, in the color of the theme, as a PNG of 112 px."""
    icon = Image.open(JEV).convert("RGBA")
    alpha = icon.convert("L").point(lambda value: 255 if value < 90 else 0)
    alpha = Image.composite(alpha, Image.new("L", icon.size, 0), icon.getchannel("A"))
    box = alpha.getbbox()
    alpha = alpha.crop(box)
    side = max(alpha.size)
    square = Image.new("L", (side, side), 0)
    square.paste(alpha, ((side - alpha.width) // 2, (side - alpha.height) // 2))
    square = square.resize((112, 112), Image.LANCZOS)
    mark = Image.new("RGBA", square.size, color)
    mark.putalpha(square)
    out = io.BytesIO()
    mark.save(out, "PNG", optimize=True)
    return base64.b64encode(out.getvalue()).decode()


missing = [label for _, icons in ROWS for name, label in icons if name != "jev" and not paths(name)]
if missing:
    sys.exit(f"no icon for: {', '.join(missing)}")
width = PAD + LABEL + max(len(icons) for _, icons in ROWS) * (ICON + GAP) - GAP + PAD
height = 2 * PAD + len(ROWS) * ROW - (ROW - ICON)
summary = " ".join(f"{category}: {', '.join(label for _, label in icons)}." for category, icons in ROWS)
font = base64.b64encode(FONT.read_bytes()).decode()
for theme, c in THEMES.items():
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img">',
             f"<title>My stack. {summary}</title>",
             f'<style>@font-face {{ font-family: "Barlow"; font-weight: 400; src: url(data:font/woff2;base64,{font}) format("woff2"); }}'
             f'.label {{ font: 400 15px "Barlow", Arial, sans-serif; fill: {c["label"]}; }}</style>',
             '<!-- Java icon: Font Awesome Free 6.4.2 by @fontawesome, https://fontawesome.com, CC BY 4.0 -->']
    for index, (category, icons) in enumerate(ROWS):
        y = PAD + index * ROW
        parts.append(f'<text class="label" x="{PAD}" y="{y + ICON / 2}" dominant-baseline="central">{category}</text>')
        for column, (name, _) in enumerate(icons):
            x = PAD + LABEL + column * (ICON + GAP)
            if name == "jev":
                parts.append(f'<image x="{x}" y="{y}" width="{ICON}" height="{ICON}" href="data:image/png;base64,{jev_mark(c["icon"])}"/>')
                continue
            body = "".join(f'<path d="{d}"/>' for d in paths(name))
            w, h = box(name)
            scale = ICON / max(w, h)
            dx, dy = x + (ICON - w * scale) / 2, y + (ICON - h * scale) / 2
            parts.append(f'<g transform="translate({dx:g} {dy:g}) scale({scale:.4f})" fill="{c["icon"]}">{body}</g>')
    parts.append("</svg>")
    (OUT / f"stack-{theme}.svg").write_text("".join(parts), encoding="utf-8")
print(f"{sum(len(icons) for _, icons in ROWS)} icons, {width}x{height}")
print("My stack.", summary)
