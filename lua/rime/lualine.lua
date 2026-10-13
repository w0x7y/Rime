local M = {}

--- lualine theme for a Rime variant. Used by lua/lualine/themes/rime*.lua, so
--- `theme = "auto"` or `theme = "rime-abyss"` both work.
---@param variant string rime | glacier | aurora | abyss
function M.theme(variant)
	local c = require("rime").colors(variant)
	local function mode(accent)
		return {
			a = { fg = c.bg, bg = accent, gui = "bold" },
			b = { fg = accent, bg = c.bg_sel },
			c = { fg = c.muted, bg = c.bg_alt },
		}
	end
	return {
		normal = mode(c.blue),
		insert = mode(c.green),
		visual = mode(c.violet),
		replace = mode(c.red),
		command = mode(c.yellow),
		terminal = mode(c.cyan),
		inactive = {
			a = { fg = c.comment, bg = c.bg_alt },
			b = { fg = c.comment, bg = c.bg_alt },
			c = { fg = c.comment, bg = c.bg_alt },
		},
	}
end

return M
