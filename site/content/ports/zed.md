---
title: zed
description: rime for zed. all five variants in one theme file.
---

# zed

all five variants in one theme file.

{{downloads}}

## install

put the file in zed's themes folder:

```sh
mkdir -p ~/.config/zed/themes
curl -fsSL https://raw.githubusercontent.com/w0x7y/Rime/main/zed/themes/rime.json -o ~/.config/zed/themes/rime.json
```

or install it as a dev extension: clone the repository, run `zed: install dev extension` from the command palette and pick the `zed/` folder.

then open the theme selector (`cmd-k cmd-t` on macos, `ctrl-k ctrl-t` on linux) and pick a rime variant, or set it in `settings.json`:

```json
{
  "theme": "{{name}}"
}
```

to follow the system's light and dark mode:

```json
{
  "theme": {
    "mode": "system",
    "dark": "Rime",
    "light": "Rime Frost"
  }
}
```

## notes

- zed puts `if`, `for`, `return` and `try` into one `keyword.control` capture, so those keywords share the rose color. declaration keywords such as `const`, `function` and `import` stay violet. neovim and vs code can tell loops from conditionals; zed can't.
- object properties are plain text, and json keys are rose.
