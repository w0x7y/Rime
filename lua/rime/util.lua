local M = {}

local function rgb(hex)
	hex = hex:gsub("#", "")
	return tonumber(hex:sub(1, 2), 16), tonumber(hex:sub(3, 4), 16), tonumber(hex:sub(5, 6), 16)
end

--- Blend colour `a` towards `b` by `t` (0 returns a, 1 returns b).
---@param a string #rrggbb
---@param b string #rrggbb
---@param t number
function M.blend(a, b, t)
	local ar, ag, ab = rgb(a)
	local br, bg, bb = rgb(b)
	local function ch(x, y)
		return math.floor(x + (y - x) * t + 0.5)
	end
	return string.format("#%02x%02x%02x", ch(ar, br), ch(ag, bg), ch(ab, bb))
end

return M
