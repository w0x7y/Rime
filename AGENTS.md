# Rime

A colorscheme in five variants, ported to Neovim, Zed, VS Code and many terminals. Read `CONTEXT.md` before naming anything: it defines variant, palette, port, color name, syntax role and derived shade.

## Sources of truth

Most ports are generated. Edit the source, then run `python3 tools/build.py` and commit the regenerated files with it.

| To change                                                     | Edit                                                                                                        |
| ------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| A variant's colors and appearance (dark or light)             | `palettes/<slug>.json`                                                                                      |
| Which color each kind of code gets in Neovim, Zed and VS Code | `SYNTAX` in `tools/build.py`                                                                                |
| Version, extension description, variant list and order        | constants at the top of `tools/build.py` (the first variant in `ORDER` is the default)                      |
| Neovim UI and plugin highlights, options                      | `lua/rime/groups.lua`, `lua/rime/init.lua`                                                                  |
| Screenshots and `vscode/icon.png`                             | run `python3 tools/screenshots/render.py` after the above                                                   |
| The website                                                   | `site/` (see `site/README.md`); it reads `site/data.json`, which the build writes                           |
| A new port                                                    | a generator in `tools/build.py`, a page in `site/content/ports/` and an entry in `PORTS` in `site/build.ts` |

A port with one file per variant is a line in `PER_VARIANT`; the site's build fails if a port has files but no page or `PORTS` entry. A generated file is anything `build()` in `tools/build.py` returns; `python3 tools/build.py --check` names the stale ones, and any file in a generated folder it no longer writes. `tools/build.py` uses only the Python standard library.

## Syntax roles

- A role belongs in `SYNTAX` only when two or more ports use it. A highlight only one port has stays in that port.
- Role names follow Neovim treesitter captures. Each port maps its own scope names onto roles; the color and style are decided in `SYNTAX` alone.
- Neovim's `styles` option restyles a group of roles at once, so every role in one group carries that group's default style.
- Some ports can't separate what Neovim separates (Zed has one capture for `if`, `for` and `return`). Map the coarse scope to the closest role and note it in that port's README.

## Neovim

The plugin sits at the top of the repository. `lua/rime/init.lua` blends the derived shades at load time, after the user's `on_colors`, so it repeats what `colours()` in `tools/build.py` computes. The two use the same shade names and must produce the same colors.

## Checks

Run both before committing; CI runs them on every push:

```sh
python3 tools/build.py --check
python3 -m unittest discover -s tools
```

The Lua-against-Python test needs `nvim` on the path. After changing `site/`, also run `bun run typecheck` and `bun run build` in `site/`; the build fails on a link to a page, file or heading that doesn't exist.

CI installs one pinned Neovim release: to move it, change `NVIM_VERSION` and `NVIM_SHA256` together in `.github/workflows/check.yml`. Actions are pinned to commits, and Dependabot opens a monthly pull request for them and for the site's packages.

## Changes and releases

- Record every user-visible color change in `vscode/CHANGELOG.md` under `## Unreleased`.
- To release, set `VERSION` in `tools/build.py`, run the build, rename `## Unreleased` to the version, and update the `.vsix` filename in `vscode/README.md`.
- Commit subjects are short imperative sentences ("Point the README's VS Code section at the Marketplace"), with a body explaining why. Commits, pull requests and release notes credit only the human author: no co-author trailers or tool attribution.
