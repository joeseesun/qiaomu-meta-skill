#!/usr/bin/env python3
"""Ensure prior-art discovery stays built into qiaomu-meta-skill."""

from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ACTIVE_DOCS = (
    ROOT / "SKILL.md",
    ROOT / "README.md",
    ROOT / "references" / "prior-art-research.md",
    ROOT / "references" / "skill-engineering-method.md",
    ROOT / "agents" / "interface.yaml",
)
FORBIDDEN = (
    ".agents/skills/find-skills/SKILL.md",
    "npx skills add https://github.com/vercel-labs/skills --skill find-skills",
)


class BuiltInDiscoveryTest(unittest.TestCase):
    def test_no_external_discovery_skill_dependency(self) -> None:
        for path in ACTIVE_DOCS:
            text = path.read_text(encoding="utf-8").replace("$HOME/", "").replace("~/", "")
            for forbidden in FORBIDDEN:
                self.assertNotIn(forbidden, text, f"{path} contains {forbidden}")

    def test_direct_catalog_query_is_documented(self) -> None:
        skill_text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn('npx --yes skills find "<query>"', skill_text)
        self.assertIn('scripts/search_skillsmp.py "<query>"', skill_text)
        self.assertIn("SkillsMP", skill_text)
        self.assertIn("built-in prior-art discovery", skill_text.lower())

    def test_publishing_is_built_in(self) -> None:
        skill_text = (ROOT / "SKILL.md").read_text(encoding="utf-8").lower()
        self.assertIn("built-in github publishing", skill_text)
        self.assertIn("scripts/publish_skill.py", skill_text)
        self.assertTrue((ROOT / "scripts" / "publish_skill.py").is_file())
        self.assertNotIn("qiaomu-skill-publisher/scripts/publish_skill.py", skill_text)


if __name__ == "__main__":
    unittest.main()
