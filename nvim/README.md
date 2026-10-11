# Rime for Neovim

![Rime in Neovim](../assets/screenshot-rime.png)

A Lua colour scheme with four variants:

| Command | Variant |
|---|---|
| `:colorscheme rime` | Rime |
| `:colorscheme rime-glacier` | Rime Glacier |
| `:colorscheme rime-aurora` | Rime Aurora |
| `:colorscheme rime-abyss` | Rime Abyss |

It covers the editor UI, legacy syntax groups, treesitter captures, LSP semantic tokens, diagnostics and terminal colours. It also styles gitsigns, mini.diff, telescope, fzf-lua, snacks, nvim-cmp, blink.cmp, which-key, indent-blankline, flash, noice, lazy.nvim, mason, nvim-tree, neo-tree and lualine.

Tested on Neovim 0.12. Treesitter capture names follow Neovim 0.10+.

## Install

The plugin lives in the `nvim/` folder of the repository, so tell your plugin manager to add that folder to the runtime path.

**lazy.nvim**

```lua
{
  "w0x7y/Rime",
  lazy = false,
  priority = 1000,
  config = function(plugin)
    vim.opt.rtp:append(plugin.dir .. "/nvim")
    require("rime").setup({})
    vim.cmd.colorscheme("rime")
  end,
}
```

**vim-plug**

```vim
Plug 'w0x7y/Rime', { 'rtp': 'nvim' }
" after plug#end()
colorscheme rime
```

**packer.nvim**

```lua
use({ "w0x7y/Rime", rtp = "nvim" })
-- after packer has loaded it
vim.cmd.colorscheme("rime")
```

**Manual**

```sh
git clone https://github.com/w0x7y/Rime ~/src/Rime
mkdir -p ~/.local/share/nvim/site/pack/rime/start
ln -s ~/src/Rime/nvim ~/.local/share/nvim/site/pack/rime/start/rime
```

## Configuration

`setup()` is optional. Call it before `:colorscheme` if you want to change anything. These are the defaults:

```lua
require("rime").setup({
  transparent = false,     -- leave the background unset so the terminal shows through
  terminal_colors = true,  -- set vim.g.terminal_color_0..15
  dim_inactive = false,    -- darker background in inactive windows
  styles = {
    comments = { italic = true },
    keywords = {},
    conditionals = { bold = true },
    functions = {},
    strings = {},
    variables = {},
    types = {},
  },
  on_colors = nil,      -- function(colors, variant) end
  on_highlights = nil,  -- function(highlights, colors, variant) end
})
```

A style table replaces the default rather than merging into it, so `comments = {}` turns comment italics off. `keywords` applies to every keyword kind except conditionals, which use `conditionals`.

`on_colors` changes the semantic colours before any group is built. Derived shades such as `bg_dark`, `border` and the diff backgrounds follow your changes:

```lua
require("rime").setup({
  on_colors = function(c, variant)
    c.bg = "#0b0e13"
    if variant == "abyss" then
      c.yellow = "#e3dc9e"
    end
  end,
})
```

`on_highlights` lets you change any group before it is applied:

```lua
require("rime").setup({
  on_highlights = function(hl, c)
    hl.LineNr = { fg = c.steel }
    hl.CursorLine = { bg = c.bg_sel }
  end,
})
```

Colour names available in `c`:

- Base colours: `bg`, `bg_alt`, `bg_sel`, `comment`, `muted`, `fg`, `fg_bright`, `white`, `red`, `pink`, `yellow`, `green`, `cyan`, `blue`, `violet`, `steel`
- Derived shades: `bg_dark`, `border`, `colorcolumn`, `whitespace`, `search`, `diff_add`, `diff_change`, `diff_text`, `diff_delete`
- `none`, meaning "NONE" (no colour)

## Using the colours elsewhere

```lua
local c = require("rime").colors("abyss") -- "rime", "glacier", "aurora" or "abyss"; on_colors is applied
print(c.blue)
```

## lualine

lualine picks up the matching theme automatically with `theme = "auto"`. You can also name one directly:

```lua
require("lualine").setup({ options = { theme = "rime-glacier" } })
```

## Keyword colours

Rime gives each kind of keyword its own colour instead of painting them all the same:

| Treesitter group | Colour | Examples |
|---|---|---|
| `@keyword`, `@keyword.function`, `@keyword.import` | violet | `const`, `function`, `import` |
| `@keyword.repeat` | yellow | `for`, `while`, `continue` |
| `@keyword.conditional` | bold rose | `if`, `else` |
| `@keyword.return`, `@keyword.exception` | rose | `return`, `try`, `throw` |

To make every keyword one colour, link them back in `on_highlights`:

```lua
on_highlights = function(hl)
  for _, g in ipairs({ "@keyword.repeat", "@keyword.conditional", "@keyword.return", "@keyword.exception" }) do
    hl[g] = { link = "Keyword" }
  end
end
```

## Files

- `colors/*.lua`: one entry point per variant
- `lua/rime/init.lua`: `setup`, `load` and `colors`
- `lua/rime/groups.lua`: all highlight groups
- `lua/rime/palettes/*.lua`: generated from `palettes/` by `tools/build.py`, so don't edit these by hand
- `lua/lualine/themes/*.lua`: lualine themes
