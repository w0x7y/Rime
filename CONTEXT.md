# Rime

A cold dark colorscheme, shipped as several variants and ported to many editors and terminals.

## Language

**Variant**:
One complete colorscheme: Rime, Rime Glacier, Rime Aurora or Rime Abyss. The first, Rime, is the default.
_Avoid_: flavour, style, theme (when you mean one variant)

**Palette**:
The 16 base16 colours that define a variant. Every other colour in every port comes from it.
_Avoid_: colorscheme, theme file

**Port**:
Rime's files for one piece of software, such as Neovim, Zed, VS Code or kitty.
_Avoid_: integration, extension (that is a Zed and VS Code packaging term)

**Colour name**:
The meaning given to one palette slot, such as `bg`, `comment`, `fg` or `blue`.
_Avoid_: semantic role, role (a role is what a token is, see Syntax role)

**Syntax role**:
What a piece of code is, such as a function, keyword, comment or JSON key, and the colour name and style it gets. Roles are shared by the editor ports; each port decides which of its own token names belong to which role.
_Avoid_: token type, scope, highlight group, capture (those are one editor's names for a role)

**Derived shade**:
A colour made by blending colour names, such as `bg_dark`, `border` or a diff background.
_Avoid_: computed colour, extra colour
