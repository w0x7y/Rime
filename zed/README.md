# Rime for Zed

Four themes in one extension: **Rime**, **Rime Glacier**, **Rime Aurora** and **Rime Abyss**.

## Install

**As a dev extension**

1. Clone the repository.
2. In Zed, run `zed: install dev extension` from the command palette.
3. Pick the `zed/` folder.

**As a plain theme file**

```sh
mkdir -p ~/.config/zed/themes
cp themes/rime.json ~/.config/zed/themes/
```

Then open the theme selector (`cmd-k cmd-t` on macOS, `ctrl-k ctrl-t` on Linux) and pick a Rime variant. You can also set it in `settings.json`:

```json
{
  "theme": {
    "mode": "dark",
    "dark": "Rime",
    "light": "One Light"
  }
}
```

## Notes

- Zed puts `if`, `for`, `return` and `try` into one `keyword.control` capture, so those keywords share the rose colour. Declaration keywords such as `const`, `function` and `import` stay violet. Neovim and VS Code can separate loops from conditionals; Zed can't.
- Object properties are plain text and JSON keys are rose.
- `themes/rime.json` is generated from `palettes/` by `tools/build.py`. Edit the palettes, not this file.
