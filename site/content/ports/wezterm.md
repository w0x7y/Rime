---
title: wezterm
description: rime for the wezterm terminal.
---

# wezterm

{{downloads}}

## install

```sh
mkdir -p ~/.config/wezterm/colors
curl -fsSL https://raw.githubusercontent.com/w0x7y/rime/main/general/wezterm/{{slug}}.toml -o ~/.config/wezterm/colors/{{slug}}.toml
```

then pick the scheme by name:

```lua
-- wezterm.lua
config.color_scheme = "{{name}}"
```
