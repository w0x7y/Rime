---
title: noctalia
description: rime for the noctalia desktop shell, version 5 and later.
---

# noctalia

for the [noctalia](https://github.com/noctalia-dev/noctalia) desktop shell, version 5 and later.

{{downloads}}

## install

```sh
mkdir -p ~/.config/noctalia/palettes
curl -fsSL https://raw.githubusercontent.com/w0x7y/rime/main/general/noctalia/{{slug}}.json -o ~/.config/noctalia/palettes/{{slug}}.json
```

```toml
# ~/.config/noctalia/config.toml, or any .toml file in that folder
[theme]
mode           = "{{appearance}}"
source         = "custom"
custom_palette = "{{slug}}"
```

you can also pick the palette in noctalia's settings after choosing the custom source, or run:

```sh
noctalia msg color-scheme-set custom {{slug}}
```

## notes

- the shell takes its colors from rime's zed and vs code themes. the bar and panels use the editors' background, cards their popup background, and hovered items the gray of their list selection. blue is the primary accent, violet the secondary and cyan the tertiary.
- its terminal colors are the [16 terminal colors](/docs/colors#terminal-colors), and noctalia's terminal templates (kitty, foot, ghostty, alacritty and others) pass them on.
- each palette holds one variant, so noctalia uses the same colors in light and dark mode. keep `mode = "dark"` with a dark variant so the apps noctalia themes stay dark too, and set `mode = "light"` with rime frost.
- noctalia 4 called these color schemes, and read the same file from `~/.config/noctalia/colorschemes/rime/rime.json`.
