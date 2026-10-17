---
title: foot
description: rime for the foot terminal.
---

# foot

{{downloads}}

## install

```sh
curl -fsSL https://raw.githubusercontent.com/w0x7y/rime/main/general/foot/{{slug}}.ini -o ~/.config/foot/{{slug}}.ini
```

then include it:

```ini
# foot.ini
[main]
include=~/.config/foot/{{slug}}.ini
```

the files use foot 1.26's `[colors-dark]` section, or `[colors-light]` for rime frost. on older versions of foot, rename it to `[colors]`.
