# Rime Theme

A cold dark theme in four variants: **Rime**, **Rime Glacier**, **Rime Aurora** and **Rime Abyss**.

![Rime variants](https://raw.githubusercontent.com/w0x7y/Rime/main/assets/screenshot-all.png)

All four share a blue-black background (`#0f1218`) and lean on blues, teals and violets. Keywords are split by kind: declarations are violet, loops yellow, conditionals bold rose, and returns and exceptions rose.

## Install

Search for **Rime Theme** in the Extensions view, or run:

```sh
code --install-extension w0x7y.rime-theme
```

VSCodium, Cursor and other editors that use Open VSX can install it from [open-vsx.org](https://open-vsx.org/extension/w0x7y/rime-theme).

Then run **Preferences: Color Theme** and pick a Rime variant.

## Install from source

```sh
git clone https://github.com/w0x7y/Rime
cd Rime/vscode
npx @vscode/vsce package
code --install-extension rime-theme-0.1.0.vsix
```

## Notes

- Semantic highlighting is on, so builtins like `Math`, `Error` and `Boolean` get their colour from the language server. Without a language server they fall back to the plain grammar colours.
- In TypeScript and JavaScript the grammar gives `return`, `await` and `yield` the same scope, so all three use the rose return colour.
- The theme files are generated from the repository's `palettes/` folder by `tools/build.py`. Edit the palettes, not the JSON.

## License

MIT
