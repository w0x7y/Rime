---
title: customizing
description: change a color in neovim, or edit a palette and rebuild every rime port from it.
---

# customizing

## in neovim

the plugin's `setup()` takes `on_colors`, to change colors before anything is built from them, and `on_highlights`, to change any highlight group:

```lua
require("rime").setup({
  on_colors = function(c, variant)
    c.bg = "#0b0e13" -- derived shades such as bg_dark and border follow
  end,
  on_highlights = function(hl, c)
    hl.CursorLine = { bg = c.bg_sel }
  end,
})
```

the other options (transparency, styles, dimming) are on the [neovim page](/ports/neovim#configuration).

## change a variant

every color in every port comes from the palettes in `palettes/`. this is the default variant, `palettes/rime.json`:

```json
{
  "name": "Rime",
  "slug": "rime",
  "description": "Soft and muted pastels for long sessions.",
  "appearance": "dark",
  "palette": {
    "base00": "#23272e",
    "base01": "#2b3038",
    "base02": "#3a404b",
    "base03": "#6b768c",
    "base04": "#9aa4b6",
    "base05": "#c3ccd9",
    "base06": "#dce2eb",
    "base07": "#f0f3f8",
    "base08": "#d98a9c",
    "base09": "#e8a8cc",
    "base0A": "#e4d098",
    "base0B": "#9ad8ac",
    "base0C": "#7cc4d0",
    "base0D": "#7aa4e4",
    "base0E": "#bb98d6",
    "base0F": "#7987a1"
  }
}
```

edit it, then run the build. it rewrites the neovim, zed, vs code and terminal files and this site's data, using only the python standard library:

```sh
git clone https://github.com/w0x7y/Rime && cd Rime
python3 tools/build.py
```

which slot is which color name is on [colors](/docs/colors).

## your own variant

1. copy a palette to `palettes/<slug>.json` and give it a new `name`, `slug` and `description`. set `appearance` to `dark` or `light`.
2. add the slug to `ORDER` at the top of `tools/build.py`. the first variant in `ORDER` is the default.
3. run `python3 tools/build.py`.

every port, from neovim to fzf, now has your variant.

## which color code gets

`SYNTAX` in `tools/build.py` maps each [syntax role](/docs/syntax) to a color name and a style, and neovim, zed and vs code all read it. change a role there and run the build.

## checks

```sh
python3 tools/build.py --check        # lists generated files that are out of date or no longer generated
python3 -m unittest discover -s tools  # the tests; one needs nvim on the path
```

the screenshots and the vs code icon come from `python3 tools/screenshots/render.py`.
