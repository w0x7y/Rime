local M = {}

local syntax = require("rime.syntax")

--- The default style of a syntax role, as every editor port uses it.
local function role_style(role)
  return vim.deepcopy(syntax[role].style)
end

-- Short variant names; the first is the default. Generated from palettes/ by tools/build.py.
M.variants = require("rime.variants")

---@class RimeConfig
M.defaults = {
  -- Leave the editor background unset so the terminal shows through.
  transparent = false,
  -- Set vim.g.terminal_color_0..15 for :terminal buffers.
  terminal_colors = true,
  -- Give inactive windows a slightly darker background.
  dim_inactive = false,
  -- Extra attributes per syntax group, e.g. { italic = true } or { bold = true }.
  -- The defaults are comments italic and conditionals bold, as in the other editor ports.
  styles = {
    comments = role_style("comment"),
    keywords = role_style("keyword"),
    conditionals = role_style("keyword.conditional"),
    functions = role_style("function"),
    strings = role_style("string"),
    variables = role_style("variable"),
    types = role_style("type"),
  },
  -- Change colours before groups are built: function(colors, variant) end
  on_colors = nil,
  -- Change or add highlight groups: function(highlights, colors, variant) end
  on_highlights = nil,
}

M.config = vim.deepcopy(M.defaults)

---@param opts? RimeConfig
function M.setup(opts)
  opts = opts or {}
  M.config = vim.tbl_deep_extend("force", vim.deepcopy(M.defaults), opts)
  -- A style table replaces the default instead of merging into it, so
  -- `comments = {}` really means "no extra attributes".
  for name, style in pairs(opts.styles or {}) do
    M.config.styles[name] = style
  end
end

--- The short name of a variant: nil gives the default, and "rime-glacier" gives "glacier".
local function short_name(variant)
  return variant and (variant:gsub("^rime%-", "")) or M.variants[1]
end

--- The colorscheme name of a variant, as used by :colorscheme.
local function colors_name(key)
  return key == "rime" and "rime" or ("rime-" .. key)
end

--- The colour names of a variant and its derived shades, with `on_colors` applied,
--- e.g. require("rime").colors("abyss").blue
---@param variant? string rime | glacier | aurora | abyss, or the full name such as rime-abyss
function M.colors(variant)
  variant = short_name(variant)
  local ok, p = pcall(require, "rime.palettes." .. variant)
  if not ok then
    error(("rime: unknown variant %q (expected one of: %s)"):format(variant, table.concat(M.variants, ", ")))
  end
  local c = {
    bg = p.base00, bg_alt = p.base01, bg_sel = p.base02, comment = p.base03,
    muted = p.base04, fg = p.base05, fg_bright = p.base06, white = p.base07,
    red = p.base08, pink = p.base09, yellow = p.base0A, green = p.base0B,
    cyan = p.base0C, blue = p.base0D, violet = p.base0E, steel = p.base0F,
  }
  if M.config.on_colors then
    M.config.on_colors(c, variant)
  end
  -- Derived shades come after on_colors so they follow any changed base colour,
  -- but a shade set explicitly in on_colors is kept.
  local blend = require("rime.util").blend
  c.bg_dark = c.bg_dark or blend(c.bg, "#000000", 0.18)
  c.colorcolumn = c.colorcolumn or blend(c.bg, c.bg_alt, 0.5)
  c.border = c.border or blend(c.bg_alt, c.bg_sel, 0.5)
  c.whitespace = c.whitespace or blend(c.comment, c.bg, 0.45)
  c.diff_add = c.diff_add or blend(c.green, c.bg, 0.85)
  c.diff_change = c.diff_change or blend(c.blue, c.bg, 0.88)
  c.diff_text = c.diff_text or blend(c.blue, c.bg, 0.7)
  c.diff_delete = c.diff_delete or blend(c.red, c.bg, 0.85)
  c.search = c.search or blend(c.yellow, c.bg, 0.72)
  c.none = "NONE"
  return c
end

---@param variant? string rime | glacier | aurora | abyss, or the full name such as rime-abyss
function M.load(variant)
  variant = short_name(variant)
  local cfg = M.config
  local c = M.colors(variant)

  if vim.g.colors_name then
    vim.cmd("hi clear")
  end
  vim.o.termguicolors = true
  vim.o.background = "dark"
  vim.g.colors_name = colors_name(variant)

  local groups = require("rime.groups").get(c, cfg)
  if cfg.on_highlights then
    cfg.on_highlights(groups, c, variant)
  end
  for name, spec in pairs(groups) do
    vim.api.nvim_set_hl(0, name, spec)
  end

  if cfg.terminal_colors then
    local ansi = {
      c.bg_sel, c.red, c.green, c.yellow, c.blue, c.violet, c.cyan, c.fg,
      c.comment, c.red, c.green, c.yellow, c.blue, c.violet, c.cyan, c.white,
    }
    local lighten = require("rime.util").blend
    for i, col in ipairs(ansi) do
      -- brights are lifted versions of the normal accents, as in the terminal ports
      if i >= 10 and i <= 15 then
        col = lighten(col, "#ffffff", 0.22)
      end
      vim.g["terminal_color_" .. (i - 1)] = col
    end
  end
end

return M
