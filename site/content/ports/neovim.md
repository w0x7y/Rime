---
title: neovim
description: rime for neovim. treesitter, lsp semantic tokens, diagnostics, lualine and twenty plugins.
---

# neovim

a lua colorscheme. it covers the editor ui, legacy syntax groups, treesitter captures, lsp semantic tokens, diagnostics and terminal colors. it also styles gitsigns, mini.diff, telescope, fzf-lua, snacks, nvim-cmp, blink.cmp, which-key, indent-blankline, flash, noice, lazy.nvim, mason, nvim-tree, neo-tree and lualine.

tested on neovim 0.12. treesitter capture names follow neovim 0.10 and later.

## install

with [lazy.nvim](https://github.com/folke/lazy.nvim):

```lua
{
  "w0x7y/rime",
  lazy = false,
  priority = 1000,
  config = function()
    require("rime").setup({})
    vim.cmd.colorscheme("{{slug}}")
  end,
}
```

with `vim.pack`, on neovim 0.12 and later:

```lua
vim.pack.add({ "https://github.com/w0x7y/rime" })
vim.cmd.colorscheme("{{slug}}")
```

with vim-plug:

```vim
Plug 'w0x7y/rime'
" after plug#end()
colorscheme {{slug}}
```

with packer.nvim:

```lua
use("w0x7y/rime")
-- after packer has loaded it
vim.cmd.colorscheme("{{slug}}")
```

or by hand:

```sh
git clone https://github.com/w0x7y/rime ~/.local/share/nvim/site/pack/rime/start/rime
```

## variants

| command | variant |
| --- | --- |
| `:colorscheme rime` | rime |
| `:colorscheme rime-glacier` | rime glacier |
| `:colorscheme rime-aurora` | rime aurora |
| `:colorscheme rime-abyss` | rime abyss |
| `:colorscheme rime-frost` | rime frost |

## configuration

`setup()` is optional. call it before `:colorscheme` to change anything. these are the defaults:

```lua
require("rime").setup({
  transparent = false,     -- leave the background unset so the terminal shows through
  terminal_colors = true,  -- set vim.g.terminal_color_0..15
  dim_inactive = false,    -- sidebar background (bg_dark) in inactive windows
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

a style table replaces the default rather than merging into it, so `comments = {}` turns comment italics off. `keywords` applies to every keyword kind except conditionals, which use `conditionals`.

### on_colors

changes the colors before any group is built. derived shades such as `bg_dark`, `border` and the diff backgrounds follow your changes:

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

### on_highlights

changes any group before it is applied:

```lua
require("rime").setup({
  on_highlights = function(hl, c)
    hl.LineNr = { fg = c.steel }
    hl.CursorLine = { bg = c.bg_sel }
  end,
})
```

the names `c` holds are listed on [colors](/docs/colors).

## the colors elsewhere

```lua
local c = require("rime").colors("{{key}}")
print(c.blue)
```

`colors()` takes `"rime"`, `"glacier"`, `"aurora"`, `"abyss"`, `"frost"` or a full name like `"rime-abyss"`, with your `on_colors` applied.

## lualine

lualine picks the matching theme with `theme = "auto"`. you can also name one:

```lua
require("lualine").setup({ options = { theme = "{{slug}}" } })
```

## keyword colors

rime gives each kind of keyword its own color instead of painting them all the same:

| treesitter group | color | examples |
| --- | --- | --- |
| `@keyword`, `@keyword.function`, `@keyword.import` | violet | `const`, `function`, `import` |
| `@keyword.repeat` | yellow | `for`, `while`, `continue` |
| `@keyword.conditional` | bold rose | `if`, `else` |
| `@keyword.return`, `@keyword.exception` | rose | `return`, `try`, `throw` |

to make every keyword one color, link them back in `on_highlights`:

```lua
on_highlights = function(hl)
  for _, g in ipairs({ "@keyword.repeat", "@keyword.conditional", "@keyword.return", "@keyword.exception" }) do
    hl[g] = { link = "Keyword" }
  end
end
```
