# usage: compose.py <shots-dir> <out.html> <cols> <slug>...
# Wraps nvim :TOhtml exports (<shots-dir>/<slug>.html) in editor-window frames.
import sys, re, json, pathlib
shots, out, cols, slugs = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4:]
PALETTES = pathlib.Path(__file__).resolve().parents[2] / "palettes"
names = {"rime": "Rime", "rime-glacier": "Rime Glacier", "rime-aurora": "Rime Aurora", "rime-abyss": "Rime Abyss"}
def mixblack(h, t=0.18):
    return "#" + "".join(f"{round(int(h[i:i+2],16)*(1-t)):02x}" for i in (1,3,5))
css, panes = [], []
for slug in slugs:
    html = open(f"{shots}/{slug}.html").read()
    pal = json.load(open(PALETTES / f"{slug}.json"))["palette"]
    style = re.search(r"<style>(.*?)</style>", html, re.S)[1]
    for line in style.strip().splitlines():
        m = re.match(r"^(\S.*?)\s*\{(.*)\}\s*$", line)
        if not m: continue
        sel, decl = m[1], m[2]
        if sel == "*": continue
        if sel == "body": css.append(f".v-{slug} {{{decl}}}"); continue
        css.append(f".v-{slug} {sel} {{{decl}}}")
    pre = re.search(r"<pre>(.*?)</pre>", html, re.S)[1]
    panes.append(f'<div class="win v-{slug}" style="border-color:{pal["base02"]}"><div class="bar" style="background:{mixblack(pal["base00"])};color:{pal["base04"]}">'
                 f'<i style="background:{pal["base08"]}"></i><i style="background:{pal["base0A"]}"></i><i style="background:{pal["base0B"]}"></i>'
                 f'<span>{names[slug]}</span><em style="color:{pal["base03"]}">sensors.ts · nvim</em></div><pre>{pre}</pre></div>')
page = f"""<!doctype html><html><head><meta charset="utf-8"><style>
body{{margin:0;background:transparent}}
.grid{{display:grid;grid-template-columns:repeat({cols},1fr);gap:18px;padding:0}}
.win{{border-radius:12px;overflow:hidden;border:1px solid}}
.bar{{display:flex;align-items:center;gap:7px;padding:10px 14px;font:600 12.5px ui-sans-serif,system-ui,sans-serif}}
.bar i{{width:11px;height:11px;border-radius:50%;display:inline-block;opacity:.85}}
.bar span{{margin-left:8px}} .bar em{{margin-left:auto;font-style:normal;font-weight:400}}
pre{{margin:0;padding:14px 18px 18px 6px;font:13px/1.6 "JetBrains Mono","Fira Code","DejaVu Sans Mono",monospace;overflow:hidden;white-space:pre}}
{chr(10).join(css)}
</style></head><body><div class="grid">{''.join(panes)}</div></body></html>"""
open(out, "w").write(page)
print(out, len(page))
