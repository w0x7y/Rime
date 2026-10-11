-- usage: nvim --headless -u NONE --cmd "set rtp+=<parsers> rtp+=<repo>/nvim" -l export_html.lua <colorscheme> <file> <out.html>
vim.cmd.packadd("nvim.tohtml")
local scheme, file, out = _G.arg[1], _G.arg[2], _G.arg[3]
vim.cmd.colorscheme(scheme)
vim.cmd.edit(file)
vim.treesitter.start(0, "typescript")
vim.wo.number = true
vim.fn.writefile(require("tohtml").tohtml(0, { title = scheme, number_lines = true }), out)
