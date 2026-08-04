#!/usr/bin/env python3
"""Keep the public Codex history showcase accurate and privacy-safe."""

from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "reports" / "codex-skill-catalog.md"
README = ROOT / "README.md"


def numbered_names(section: str) -> list[str]:
    return re.findall(r"^\d+\. `([^`]+)`$", section, flags=re.MULTILINE)


class CodexSkillCatalogTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.catalog = CATALOG.read_text(encoding="utf-8")
        cls.readme = README.read_text(encoding="utf-8")

    def test_catalog_counts_are_explicit_and_unique(self) -> None:
        public_block, remainder = self.catalog.split(
            "### Local, private, or not publicly released", maxsplit=1
        )
        private_block = remainder.split("## Dated prior-art candidates", maxsplit=1)[0]
        public = numbered_names(public_block)
        private = numbered_names(private_block)
        self.assertEqual(18, len(public))
        self.assertEqual(10, len(private))
        self.assertEqual(28, len(set(public + private)))
        self.assertIn("Total deduplicated cases: 28", self.catalog)

    def test_public_cases_link_to_their_repositories(self) -> None:
        public_block = self.catalog.split(
            "### Local, private, or not publicly released", maxsplit=1
        )[0]
        for name in numbered_names(public_block):
            self.assertIn(
                f"https://github.com/joeseesun/{name}",
                self.readme,
                f"README lacks public repository link for {name}",
            )

    def test_catalog_does_not_publish_local_paths_or_raw_session_files(self) -> None:
        self.assertNotIn("/Users/", self.catalog)
        self.assertNotIn(".jsonl", self.catalog)
        self.assertNotRegex(self.catalog, r"gh[opusr]_[A-Za-z0-9]{20,}")


if __name__ == "__main__":
    unittest.main()
