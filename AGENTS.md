# Rime

A colorscheme in five variants, ported to Neovim, Zed, VS Code and many terminals. Read `CONTEXT.md` before naming anything: it defines variant, palette, port, colour name, syntax role and derived shade.

## Sources of truth

Most ports are generated. Edit the source, then run `python3 tools/build.py` and commit the regenerated files with it.

| To change                                                      | Edit                                                                                   |
| -------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| A variant's colours and appearance (dark or light)             | `palettes/<slug>.json`                                                                 |
| Which colour each kind of code gets in Neovim, Zed and VS Code | `SYNTAX` in `tools/build.py`                                                           |
| Version, extension description, variant list and order         | constants at the top of `tools/build.py` (the first variant in `ORDER` is the default) |
| Neovim UI and plugin highlights, options                       | `lua/rime/groups.lua`, `lua/rime/init.lua`                                             |
| Screenshots and `vscode/icon.png`                              | run `python3 tools/screenshots/render.py` after the above                              |

A generated file is anything `build()` in `tools/build.py` returns; `python3 tools/build.py --check` names the stale ones. `tools/build.py` uses only the Python standard library.

## Syntax roles

- A role belongs in `SYNTAX` only when two or more ports use it. A highlight only one port has stays in that port.
- Role names follow Neovim treesitter captures. Each port maps its own scope names onto roles; the colour and style are decided in `SYNTAX` alone.
- Neovim's `styles` option restyles a group of roles at once, so every role in one group carries that group's default style.
- Some ports can't separate what Neovim separates (Zed has one capture for `if`, `for` and `return`). Map the coarse scope to the closest role and note it in that port's README.

## Neovim

The plugin sits at the top of the repository. `lua/rime/init.lua` blends the derived shades at load time, after the user's `on_colors`, so it repeats what `colours()` in `tools/build.py` computes. The two use the same shade names and must produce the same colours.

## Checks

Run both before committing; CI runs them on every push:

```sh
python3 tools/build.py --check
python3 -m unittest discover -s tools
```

The Lua-against-Python test needs `nvim` on the path.

## Changes and releases

- Record every user-visible colour change in `vscode/CHANGELOG.md` under `## Unreleased`.
- To release, set `VERSION` in `tools/build.py`, run the build, rename `## Unreleased` to the version, and update the `.vsix` filename in `vscode/README.md`.
- Commit subjects are short imperative sentences ("Point the README's VS Code section at the Marketplace"), with a body explaining why. Commits, pull requests and release notes credit only the human author: no co-author trailers or tool attribution.
