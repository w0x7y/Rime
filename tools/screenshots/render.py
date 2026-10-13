#!/usr/bin/env python3
"""Regenerate the README screenshots from real Neovim highlighting, and the VS Code icon.

Needs: nvim 0.10+ with the typescript and rust treesitter parsers, chromium, Pillow,
and the Maple Mono NF font installed. Run tools/build.py first so the colorschemes are current.

Usage: python3 tools/screenshots/render.py [dir containing parser/typescript.so and queries]
"""

import math
import pathlib
import re
import subprocess
import sys
import tempfile

from PIL import Image

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import build  # noqa: E402

# Each shot renders `sample` in every variant listed, as rows of panes: `rows` gives the number of
# panes in each row, and each row splits the width evenly. `size` is the browser window; the
# transparent margin around the panes is cropped away.
SHOTS = [
    {
        "out": "assets/screenshot-all.png",
        "variants": build.ORDER,
        "sample": "sample.ts",
        "rows": [2, 3],
        "size": (2200, 1500),
    },
    # the default variant on its own, for the Neovim README
    {
        "out": "assets/screenshot-rime.png",
        "variants": build.ORDER[:1],
        "sample": "sample.ts",
        "rows": [1],
        "size": (760, 760),
    },
    # a small Rust demo for the top of the README
    {
        "out": "assets/demo.png",
        "variants": build.ORDER[:1],
        "sample": "demo.rs",
        "rows": [1],
        "size": (600, 600),
    },
]
LANGUAGES = {".ts": "typescript", ".rs": "rust"}


def export(variant, sample, parsers, out):
    """Write Neovim's :TOhtml export of `sample` highlighted by the `variant` colorscheme."""
    lang = LANGUAGES[pathlib.Path(sample).suffix]
    subprocess.run(
        [
            "nvim",
            "--headless",
            "-u",
            "NONE",
            "--cmd",
            f"set rtp^={parsers} rtp^={parsers}/runtime rtp+={ROOT}",
            "-l",
            HERE / "export_html.lua",
            variant,
            HERE / sample,
            out,
            lang,
        ],
        check=True,
    )


def compose(exports, rows):
    """One page with each variant's export in a rounded code pane. `exports` maps slug to :TOhtml output."""
    palettes = {spec["slug"]: spec["palette"] for spec in build.load()[0]}
    # the grid has enough columns for every row to split evenly; a pane in a row of n spans width/n
    width = math.lcm(*rows)
    spans = [width // n for n in rows for _ in range(n)]
    css, panes = [], []
    for (slug, html), span in zip(exports.items(), spans, strict=True):
        style = re.search(r"<style>(.*?)</style>", html, re.S)[1]
        for line in style.strip().splitlines():
            m = re.match(r"^(\S.*?)\s*\{(.*)\}\s*$", line)
            if not m or m[1] == "*":
                continue
            sel, decl = m[1], m[2]
            css.append(
                f".v-{slug} {{{decl}}}"
                if sel == "body"
                else f".v-{slug} {sel} {{{decl}}}"
            )
        # drop the trailing newline so the pane ends right after the last line
        pre = re.search(r"<pre>(.*?)</pre>", html, re.S)[1].rstrip()
        panes.append(
            f'<div class="win v-{slug}" style="border-color:{palettes[slug]["base02"]};grid-column:span {span}"><pre>{pre}</pre></div>'
        )
    # a single pane hugs its code; a grid splits the width evenly
    columns = "max-content" if rows == [1] else f"repeat({width},1fr)"
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
body{{margin:0;background:transparent}}
.grid{{display:grid;grid-template-columns:{columns};gap:18px;padding:0}}
.win{{border-radius:12px;overflow:hidden;border:1px solid}}
pre{{margin:0;padding:16px 18px 16px 6px;font:13px/1.6 "Maple Mono NF",monospace;tab-size:4;overflow:hidden;white-space:pre}}
{chr(10).join(css)}
</style></head><body><div class="grid">{''.join(panes)}</div></body></html>"""


def shoot(page, size, png, scale=2):
    """Screenshot a local page with a transparent background."""
    subprocess.run(
        [
            "chromium",
            "--headless=new",
            "--disable-gpu",
            "--hide-scrollbars",
            f"--force-device-scale-factor={scale}",
            "--default-background-color=00000000",
            f"--window-size={size[0]},{size[1]}",
            f"--screenshot={png}",
            f"file://{page}",
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def crop(png):
    im = Image.open(png).convert("RGBA")
    im.crop(im.getchannel("A").getbbox()).save(png, optimize=True)


def main(args):
    parsers = (
        args[0]
        if args
        else str(pathlib.Path.home() / ".local/share/nvim/lazy/nvim-treesitter")
    )
    with tempfile.TemporaryDirectory() as work:
        work = pathlib.Path(work)
        exported = {}  # (variant, sample) -> html, so each pair is exported once
        for shot in SHOTS:
            for variant in shot["variants"]:
                key = (variant, shot["sample"])
                if key not in exported:
                    out = work / f"{variant}-{shot['sample']}.html"
                    export(variant, shot["sample"], parsers, out)
                    exported[key] = out.read_text()
            page = work / f"{pathlib.Path(shot['out']).stem}.html"
            page.write_text(
                compose(
                    {v: exported[(v, shot["sample"])] for v in shot["variants"]},
                    shot["rows"],
                )
            )
            shoot(page, shot["size"], ROOT / shot["out"])
            crop(ROOT / shot["out"])
    # assets/icon.svg is generated by tools/build.py; the Marketplace wants a PNG
    shoot(ROOT / "assets/icon.svg", (256, 256), ROOT / "vscode/icon.png", scale=1)
    Image.open(ROOT / "vscode/icon.png").save(ROOT / "vscode/icon.png", optimize=True)
    print(f"wrote {', '.join(s['out'] for s in SHOTS)} and vscode/icon.png")


if __name__ == "__main__":
    main(sys.argv[1:])
