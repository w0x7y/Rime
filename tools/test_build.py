"""Checks for the generator and the files it keeps in step.

Run: python3 -m unittest discover -s tools
"""

import json
import os
import pathlib
import re
import shutil
import subprocess
import tempfile
import unittest
from unittest import mock

import build


class GeneratedFiles(unittest.TestCase):
    def test_committed_files_match_the_palettes(self):
        self.assertEqual(
            build.stale(build.build(*build.load())),
            [],
            "run python3 tools/build.py and commit the result",
        )

    def test_check_ignores_formatting(self):
        with tempfile.TemporaryDirectory() as tmp, mock.patch.object(
            build, "ROOT", pathlib.Path(tmp)
        ):
            files = {
                "crlf.lua": ("a = 1\r\n", "a = 1\n"),
                "indent.lua": ("\ta = 1\n", "    a = 1\n"),
                "changed.lua": ("a = 1\n", "a = 2\n"),
                "wrapped.json": ('{"a": [1, 2]}\n', '{\n\t"a": [\n\t\t1,\n\t\t2\n\t]\n}\n'),
                "changed.json": ('{"a": 1}\n', '{"a": 2}\n'),
                "broken.json": ('{"a": 1\n', '{"a": 1}\n'),
            }
            for path, (on_disk, _) in files.items():
                (pathlib.Path(tmp) / path).write_bytes(on_disk.encode())
            generated = {path: text for path, (_, text) in files.items()}
            self.assertEqual(
                build.stale(generated | {"missing.lua": "a = 1\n"}),
                ["changed.lua", "changed.json", "broken.json", "missing.lua"],
            )

    def test_every_variant_names_its_appearance(self):
        for spec in build.load()[0]:
            self.assertIn(spec.get("appearance"), ("dark", "light"), spec["slug"])


class SyntaxRoles(unittest.TestCase):
    """build.SYNTAX decides the colour of each syntax role once, for every editor port."""

    def lua(self, name):
        return (build.ROOT / "lua/rime" / name).read_text()

    def neovim_roles(self):
        return set(
            re.findall(
                r'\b(?:role|colour|role_style)\("([^"]+)"',
                self.lua("groups.lua") + self.lua("init.lua"),
            )
        )

    def roles_used_by(self, port):
        used = set()

        class Recording(dict):
            def __getitem__(self, role):
                used.add(role)
                return super().__getitem__(role)

        with mock.patch.object(build, "SYNTAX", Recording(build.SYNTAX)):
            port(build.load()[0][0])
        return used

    def test_neovim_names_only_known_roles(self):
        self.assertEqual(
            self.neovim_roles() - set(build.SYNTAX), set(), "unknown roles in lua/rime"
        )

    def test_roles_in_a_neovim_style_group_share_its_default(self):
        # e.g. Neovim styles keyword.return with `styles.keywords`, whose default is the keyword role's style
        defaults = dict(
            re.findall(r'(\w+) = role_style\("([^"]+)"\)', self.lua("init.lua"))
        )
        for role, group in re.findall(
            r'\brole\("([^"]+)", st\.(\w+)\)', self.lua("groups.lua")
        ):
            self.assertEqual(
                build.SYNTAX[role][1],
                build.SYNTAX[defaults[group]][1],
                f"Neovim styles {role} with styles.{group}, which defaults to {defaults[group]}'s style",
            )

    def test_every_role_is_shared_by_two_ports(self):
        ports = {
            "Neovim": self.neovim_roles(),
            "Zed": self.roles_used_by(build.zed_theme),
            "VS Code": self.roles_used_by(build.vscode_theme),
        }
        for role in build.SYNTAX:
            users = [port for port, roles in ports.items() if role in roles]
            self.assertGreaterEqual(
                len(users), 2, f"{role} is only used by {users}; keep it in that port"
            )


@unittest.skipUnless(
    shutil.which("nvim") or os.environ.get("RIME_REQUIRE_NVIM"), "needs nvim"
)
class LuaMatchesPython(unittest.TestCase):
    """Neovim blends its derived shades at load time, after on_colors. Unchanged, they must equal the generated ports'."""

    LUA = """
    local rime = require("rime")
    local out = {}
    for _, v in ipairs(rime.variants) do
      rime.load(v)
      local c, term = rime.colors(v), {}
      for i = 0, 15 do term[i + 1] = vim.g["terminal_color_" .. i] end
      out[#out + 1] = { bg_dark = c.bg_dark, border = c.border, ansi = term }
    end
    io.stdout:write(vim.json.encode(out))
    """

    def test_derived_shades_and_terminal_colours(self):
        with tempfile.NamedTemporaryFile("w", suffix=".lua") as script:
            script.write(self.LUA)
            script.flush()
            run = subprocess.run(
                [
                    "nvim",
                    "--headless",
                    "-u",
                    "NONE",
                    "--cmd",
                    f"set rtp^={build.ROOT}",
                    "-l",
                    script.name,
                ],
                capture_output=True,
                text=True,
                check=True,
            )
        for spec, lua in zip(build.load()[0], json.loads(run.stdout)):
            py = build.colours(spec)
            self.assertEqual(
                lua,
                {"bg_dark": py["bg_dark"], "border": py["border"], "ansi": py["ansi"]},
                spec["slug"],
            )


class Noctalia(unittest.TestCase):
    """Noctalia sets text in each on_* colour on its role's fill, so a palette edit must keep them readable."""

    @staticmethod
    def contrast(a, b):
        def luminance(h):
            r, g, b = (
                v / 255 / 12.92 if v <= 10 else ((v / 255 + 0.055) / 1.055) ** 2.4
                for v in build.rgb(h)
            )
            return 0.2126 * r + 0.7152 * g + 0.0722 * b

        hi, lo = sorted((luminance(a), luminance(b)), reverse=True)
        return (hi + 0.05) / (lo + 0.05)

    def test_on_colours_are_readable(self):
        for spec in build.load()[0]:
            for mode in build.noctalia(spec).values():
                for role in (
                    "Primary",
                    "Secondary",
                    "Tertiary",
                    "Error",
                    "Surface",
                    "SurfaceVariant",
                    "Hover",
                ):
                    self.assertGreaterEqual(
                        self.contrast(mode[f"mOn{role}"], mode[f"m{role}"]),
                        4.5,
                        f"{spec['slug']}: mOn{role}",
                    )

    def test_shell_matches_the_editor_chrome(self):
        for spec in build.load()[0]:
            zed, vscode = (
                build.zed_theme(spec)["style"],
                build.vscode_theme(spec)["colors"],
            )
            mode = build.noctalia(spec)["dark"]
            self.assertEqual(mode["mSurface"], zed["editor.background"], spec["slug"])
            self.assertEqual(
                mode["mSurface"], vscode["editor.background"], spec["slug"]
            )
            self.assertEqual(
                mode["mSurfaceVariant"],
                zed["elevated_surface.background"],
                spec["slug"],
            )
            self.assertEqual(
                mode["mHover"], vscode["list.activeSelectionBackground"], spec["slug"]
            )
            self.assertEqual(
                mode["mOnPrimary"], vscode["button.foreground"], spec["slug"]
            )
            self.assertEqual(mode["mOutline"], zed["border"], spec["slug"])

    def test_terminals_share_the_theme_background(self):
        for spec in build.load()[0]:
            zed, vscode = (
                build.zed_theme(spec)["style"],
                build.vscode_theme(spec)["colors"],
            )
            terminals = [
                zed["terminal.background"],
                vscode["terminal.background"],
                build.noctalia(spec)["dark"]["terminal"]["background"],
            ]
            self.assertEqual(terminals, [spec["palette"]["base00"]] * 3, spec["slug"])


class Docs(unittest.TestCase):
    """Prose that quotes generated values, so a release or palette change can't leave it behind."""

    def read(self, path):
        return (build.ROOT / path).read_text()

    def test_install_from_source_names_the_current_version(self):
        versions = re.findall(
            rf"{build.EXTENSION_ID}-(\d+\.\d+\.\d+)\.vsix",
            self.read("vscode/README.md"),
        )
        self.assertEqual(set(versions), {build.VERSION})

    def test_quoted_background_is_the_default_variants(self):
        bg = build.load()[0][0]["palette"]["base00"]
        for path in ("README.md", "vscode/README.md"):
            for line in self.read(path).splitlines():
                if "background" in line:
                    for quoted in re.findall(r"`(#[0-9a-fA-F]{6})`", line):
                        self.assertEqual(quoted.lower(), bg, f"{path}: {line}")


if __name__ == "__main__":
    unittest.main()
