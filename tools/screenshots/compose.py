# usage: compose.py <shots-dir> <out.html> <cols> <slug>...
# Wraps nvim :TOhtml exports (<shots-dir>/<slug>.html) in rounded code panes.
import sys, re, json, pathlib
shots, out, cols, slugs = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4:]
PALETTES = pathlib.Path(__file__).resolve().parents[2] / "palettes"
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
    # drop the trailing newline so the pane ends right after the last line
    pre = re.search(r"<pre>(.*?)</pre>", html, re.S)[1].rstrip()
    panes.append(f'<div class="win v-{slug}" style="border-color:{pal["base02"]}"><pre>{pre}</pre></div>')
# a single pane hugs its code; a grid splits the width evenly
columns = "max-content" if cols == 1 else f"repeat({cols},1fr)"
page = f"""<!doctype html><html><head><meta charset="utf-8"><style>
body{{margin:0;background:transparent}}
.grid{{display:grid;grid-template-columns:{columns};gap:18px;padding:0}}
.win{{border-radius:12px;overflow:hidden;border:1px solid}}
pre{{margin:0;padding:16px 18px 16px 6px;font:13px/1.6 "Maple Mono NF",monospace;tab-size:4;overflow:hidden;white-space:pre}}
{chr(10).join(css)}
</style></head><body><div class="grid">{''.join(panes)}</div></body></html>"""
open(out, "w").write(page)
print(out, len(page))
