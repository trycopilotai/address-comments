#!/usr/bin/env python3
"""The packaging test for the skill package under skills/address-comments/.

It reads the package's files and their modes. It starts no
agent and does not follow the skill. Its verbose output is
recorded in evidence/transcripts/package-check.txt.

Runs offline with the standard library:

    python3 tests/test_package.py -v
"""

from __future__ import annotations

import os
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PACKAGE = ROOT / "skills" / "address-comments"
FILES = {"SKILL.md", "agents/openai.yaml"}
TEXT_SUFFIXES = {".md", ".yaml"}
MARKERS = (
    "`AGENT:`",
    "`AGENTS:`",
    "`TO AGENT`",
    "`TO AGENTS`",
    "`TODO(agent)`",
    "`TODO(agents)`",
    "TODO(code-review:<id>)",
)
DEFAULT_LOG = "`.address-comments/review-log.md`"
HOST_PATH = re.compile(r"(/Users/|/home/|~/|\$HOME)")


def package_files() -> set:
    found = set()
    for directory, _names, files in os.walk(str(PACKAGE)):
        for name in files:
            path = Path(directory) / name
            found.add(path.relative_to(PACKAGE).as_posix())
    return found


def read(relative: str) -> str:
    return (PACKAGE / relative).read_text(encoding="utf-8")


class PackageTest(unittest.TestCase):
    def test_1_files(self) -> None:
        """The package is SKILL.md and agents/openai.yaml."""
        self.assertEqual(package_files(), FILES)

    def test_2_no_program(self) -> None:
        """No package file is executable, has a #! line, or is not .md/.yaml."""
        for relative in sorted(package_files()):
            path = PACKAGE / relative
            self.assertFalse(path.is_symlink(), relative)
            self.assertIn(path.suffix, TEXT_SUFFIXES, relative)
            self.assertFalse(os.access(str(path), os.X_OK), relative)
            self.assertFalse(path.read_bytes().startswith(b"#!"), relative)

    def test_3_markers(self) -> None:
        """SKILL.md names the four labels and the three marker shapes."""
        text = read("SKILL.md")
        for marker in MARKERS:
            self.assertIn(marker, text)

    def test_4_default_log(self) -> None:
        """SKILL.md gives .address-comments/review-log.md as the default log."""
        text = " ".join(read("SKILL.md").split())
        self.assertIn("When no path is given, use " + DEFAULT_LOG, text)

    def test_5_no_host_path(self) -> None:
        """No package file contains /Users/, /home/, ~/ or $HOME."""
        for relative in sorted(package_files()):
            self.assertIsNone(HOST_PATH.search(read(relative)), relative)


if __name__ == "__main__":
    unittest.main()
