#!/usr/bin/env bash
# Regenerate assets/screenshot-*.png from real Neovim highlighting.
# Needs: nvim 0.10+ with the typescript treesitter parser, chromium, python3 with Pillow.
# Usage: tools/screenshots/render.sh [nvim-treesitter dir, containing parser/typescript.so and runtime/queries]
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
repo="$(cd "$here/../.." && pwd)"
parsers="${1:-$HOME/.local/share/nvim/lazy/nvim-treesitter}"
work="$(mktemp -d)"
trap 'rm -rf "$work"' EXIT
variants=(rime rime-glacier rime-aurora rime-abyss)

for v in "${variants[@]}"; do
  nvim --headless -u NONE --cmd "set rtp^=$parsers rtp^=$parsers/runtime rtp+=$repo/nvim" \
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

# crop the transparent margin
python3 - "$repo"/assets/screenshot-*.png <<'PY'
import sys
from PIL import Image
for f in sys.argv[1:]:
    im = Image.open(f).convert("RGBA")
    im.crop(im.getchannel("A").getbbox()).save(f, optimize=True)
PY
echo "screenshots written to $repo/assets"
