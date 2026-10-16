---
title: kitty
description: rime for the kitty terminal.
---

# kitty

{{downloads}}

## install

```sh
mkdir -p ~/.config/kitty
curl -fsSL https://raw.githubusercontent.com/w0x7y/Rime/main/general/kitty/{{slug}}.conf -o ~/.config/kitty/{{slug}}.conf
echo 'include {{slug}}.conf' >> ~/.config/kitty/kitty.conf
```

then reload kitty's config with `ctrl+shift+f5`, or open a new window.
