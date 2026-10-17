---
title: vs code
description: rime for vs code, vscodium, cursor and the other forks, on the marketplace and open vsx.
---

# vs code

five themes in one extension: rime, rime glacier, rime aurora and rime abyss, which are dark, and the light rime frost.

## install

search for **rime theme** in the extensions view, or run:

```sh
code --install-extension w0x7y.rime-theme
```

it's on the [vs code marketplace](https://marketplace.visualstudio.com/items?itemName=w0x7y.rime-theme), and on [open vsx](https://open-vsx.org/extension/w0x7y/rime-theme) for vscodium, cursor and the other forks. then run **preferences: color theme** and pick a rime variant, or set it in `settings.json`:

```jsonc
{
  "workbench.colorTheme": "{{name}}"
}
```

to follow the system's light and dark mode:

```jsonc
{
  "window.autoDetectColorScheme": true,
  "workbench.preferredDarkColorTheme": "Rime",
  "workbench.preferredLightColorTheme": "Rime Frost"
}
```

## from source

```sh
git clone https://github.com/w0x7y/rime
cd rime/vscode
npx @vscode/vsce package
code --install-extension rime-theme-*.vsix
```

## notes

- semantic highlighting is on, so builtins like `Math`, `Error`, `Boolean` and `parseInt` get their color from the language server. without one they fall back to the plain grammar colors.
- in typescript and javascript the grammar gives `return`, `await` and `yield` the same scope, so all three use the rose return color.
