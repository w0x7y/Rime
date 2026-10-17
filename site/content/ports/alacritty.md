---
title: alacritty
description: rime for the alacritty terminal.
---

# alacritty

{{downloads}}

## install

```sh
mkdir -p ~/.config/alacritty/themes
curl -fsSL https://raw.githubusercontent.com/w0x7y/rime/main/general/alacritty/{{slug}}.toml -o ~/.config/alacritty/themes/{{slug}}.toml
```

then import it:

```toml
# alacritty.toml
[general]
import = ["~/.config/alacritty/themes/{{slug}}.toml"]
```

before alacritty 0.14, `import` was a top-level key instead of living under `[general]`.
