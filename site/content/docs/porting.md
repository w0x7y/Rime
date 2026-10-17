---
title: porting
description: how rime's ports are built, and how to add one for software it doesn't support yet.
---

# porting

if you port rime to your software of choice, open a [pull request](https://github.com/w0x7y/rime/pulls).

## how ports are made

most ports are generated. `tools/build.py` reads the palettes and the `SYNTAX` table and writes every file: the neovim modules, the zed and vs code themes, the terminal files and the rest. a new port is usually one function there that returns a file's text for one variant, and one line in `PER_VARIANT` that says where the file goes, so it stays in sync with every color change after it.

the port also needs a page on this site: `site/content/ports/<port>.md` and an entry in `PORTS` in `site/build.ts`. the site's build stops if a port has files but no page.

`build()` returns every generated file, and `python3 tools/build.py --check` names the ones that are out of date or no longer generated. the script uses only the python standard library; keep it that way.

## the rules

- name things the way the repository does: a **variant** is one complete colorscheme, a **palette** its 16 colors, a **port** rime's files for one piece of software.
- terminals get the [16 terminal colors](/docs/colors#terminal-colors) the other terminal ports use.
- a role belongs in `SYNTAX` only when two or more ports use it. a highlight only one port has stays in that port.
- role names follow neovim's treesitter captures. each port maps its own scope names onto roles; the color and style are decided in `SYNTAX` alone.
- some software can't separate what neovim separates. map the coarse scope to the closest role and note it in the port's readme.

## before the pull request

run the checks; ci runs them on every push:

```sh
python3 tools/build.py --check
python3 -m unittest discover -s tools
cd site && bun install && bun run build  # fails on a broken link
```

record any color change people will see in `vscode/CHANGELOG.md`, under `## Unreleased`.
