---
title: css
description: rime as css custom properties.
---

# css

css custom properties, with both the base16 slots and the color names. this site runs on them.

{{downloads}}

## use

```css
@import "{{slug}}.css";

body {
  background: var(--rime-bg);
  color: var(--rime-fg);
}

a {
  color: var(--rime-blue); /* or var(--base0D) */
}
```

every color name is there as `--rime-<name>`, with `_` written as `-`: `--rime-bg-alt`, `--rime-fg-bright`. the full list is on [colors](/docs/colors).
