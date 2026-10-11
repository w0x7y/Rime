#!/usr/bin/env bash
# Regenerate assets/screenshot-*.png and assets/demo.png from real Neovim highlighting.
# Needs: nvim 0.10+ with the typescript and rust treesitter parsers, chromium, python3 with Pillow,
# and the Maple Mono NF font installed.
# Usage: tools/screenshots/render.sh [nvim-treesitter dir, containing parser/typescript.so and runtime/queries]
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
repo="$(cd "$here/../.." && pwd)"
parsers="${1:-$HOME/.local/share/nvim/lazy/nvim-treesitter}"
work="$(mktemp -d)"
trap 'rm -rf "$work"' EXIT
variants=(rime rime-glacier rime-aurora rime-abyss)

for v in "${variants[@]}"; do
  nvim --headless -u NONE --cmd "set rtp^=$parsers rtp^=$parsers/runtime rtp+=$repo" \
    -l "$here/export_html.lua" "$v" "$here/sample.ts" "$work/$v.html"
done

shoot() { # html, width,height, png
  chromium --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=2 \
    --default-background-color=00000000 --window-size="$2" --screenshot="$3" "file://$1" >/dev/null 2>&1
}
python3 "$here/compose.py" "$work" "$work/all.html" 2 "${variants[@]}" >/dev/null
shoot "$work/all.html" 1500,1500 "$repo/assets/screenshot-all.png"
for v in "${variants[@]}"; do
  python3 "$here/compose.py" "$work" "$work/single-$v.html" 1 "$v" >/dev/null
  shoot "$work/single-$v.html" 760,760 "$repo/assets/screenshot-$v.png"
done

# small rust demo for the top of the README
mkdir -p "$work/demo"
nvim --headless -u NONE --cmd "set rtp^=$parsers rtp^=$parsers/runtime rtp+=$repo" \
  -l "$here/export_html.lua" rime "$here/demo.rs" "$work/demo/rime.html" rust
python3 "$here/compose.py" "$work/demo" "$work/demo.html" 1 rime >/dev/null
shoot "$work/demo.html" 600,600 "$repo/assets/demo.png"

# crop the transparent margin
python3 - "$repo"/assets/screenshot-*.png "$repo/assets/demo.png" <<'PY'
import sys
from PIL import Image
for f in sys.argv[1:]:
    im = Image.open(f).convert("RGBA")
    im.crop(im.getchannel("A").getbbox()).save(f, optimize=True)
PY
echo "screenshots written to $repo/assets"
