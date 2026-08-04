#!/usr/bin/env python3
"""Regression tests for the self-contained safe skill publisher."""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("publish_skill", ROOT / "scripts" / "publish_skill.py")
if SPEC is None or SPEC.loader is None:  # pragma: no cover
    raise RuntimeError("unable to load scripts/publish_skill.py")
PUBLISH = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = PUBLISH
SPEC.loader.exec_module(PUBLISH)


class FakeRunner:
    def __init__(self) -> None:
        self.calls: list[list[str]] = []

    def __call__(self, args: list[str], _cwd: Path, **_kwargs: object):
        self.calls.append(args)
        if args[:4] == ["git", "remote", "get-url", "origin"]:
            return PUBLISH.CommandResult(args, 2, "", "no origin")
        if args[:3] == ["gh", "api", "user"]:
            return PUBLISH.CommandResult(args, 0, "joeseesun", "")
        if args[:3] == ["gh", "repo", "view"]:
            return PUBLISH.CommandResult(args, 1, "", "not found")
        return PUBLISH.CommandResult(args, 0, "ok", "")


class PublishSkillTest(unittest.TestCase):
    def test_origin_parser_supports_https_and_ssh(self) -> None:
        self.assertEqual(
            PUBLISH.parse_origin("https://github.com/joeseesun/qiaomu-demo.git"),
            ("joeseesun", "qiaomu-demo"),
        )
        self.assertEqual(
            PUBLISH.parse_origin("git@github.com:joeseesun/qiaomu-demo.git"),
            ("joeseesun", "qiaomu-demo"),
        )

    def test_profile_marker_inside_code_fence_is_ignored(self) -> None:
        text = "```md\n<!-- qiaomu-profile:start -->\n```\n\n## License\n"
        updated = PUBLISH.insert_profile(text)
        self.assertEqual(updated.count(PUBLISH.PROFILE_START), 2)
        self.assertIn("## 关于向阳乔木", updated)
        self.assertEqual(PUBLISH.insert_profile(updated), updated)

    def test_generated_readme_passes_public_contract(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            upstream = "https://github.com/example/upstream"
            text = PUBLISH.generated_readme(
                {
                    "name": "qiaomu-demo",
                    "description": "把重复工作流整理成可验证的技能包。",
                    "version": "1.0.0",
                    "owner": "向阳乔木",
                },
                "joeseesun",
                "qiaomu-demo",
                upstream,
            )
            (root / "README.md").write_text(text, encoding="utf-8")
            self.assertEqual(PUBLISH.check_readme(root, upstream, require_profile=False), [])
            self.assertIn("validate_skill.py", text)

    def test_default_branch_push_is_rejected(self) -> None:
        for branch in ("", "main", "master"):
            with self.assertRaises(PUBLISH.PublishError):
                PUBLISH.assert_feature_branch(branch, "main")
        PUBLISH.assert_feature_branch("codex/publish-demo-v1-0-0", "main")
        with self.assertRaises(PUBLISH.PublishError):
            PUBLISH.assert_feature_branch("feature/publish-demo", "main")

    def test_failed_or_pending_checks_block_merge(self) -> None:
        ok, blockers = PUBLISH.pr_is_mergeable(
            {
                "mergeable": "MERGEABLE",
                "reviewDecision": "",
                "statusCheckRollup": [{"name": "test", "status": "IN_PROGRESS", "conclusion": None}],
            }
        )
        self.assertFalse(ok)
        self.assertTrue(any("pending" in item for item in blockers))

    def test_requested_changes_block_merge(self) -> None:
        ok, blockers = PUBLISH.pr_is_mergeable(
            {
                "mergeable": "MERGEABLE",
                "reviewDecision": "",
                "reviews": [{"state": "CHANGES_REQUESTED"}],
                "statusCheckRollup": [],
            }
        )
        self.assertFalse(ok)
        self.assertTrue(any("requested changes" in item for item in blockers))

    def test_dry_run_is_read_only_and_reports_planned_files(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "SKILL.md").write_text(
                "---\nname: qiaomu-demo\ndescription: |\n  把重复工作流整理成可验证的 qiaomu skill。\n---\n",
                encoding="utf-8",
            )
            (root / "manifest.json").write_text(
                json.dumps(
                    {
                        "name": "qiaomu-demo",
                        "version": "1.0.0",
                        "owner": "向阳乔木",
                        "upstream_inspiration": "https://github.com/example/upstream",
                    }
                ),
                encoding="utf-8",
            )
            args = argparse.Namespace(
                skill_dir=str(root),
                github_user=None,
                repo_name=None,
                branch=None,
                private=False,
                dry_run=True,
                prepare_only=False,
                verify_only=False,
                no_merge=False,
                no_sync_local=True,
                skip_qiaomu_profile=False,
            )
            result = PUBLISH.publish(args, FakeRunner())
            self.assertTrue(result["ok"])
            self.assertIn("LICENSE", result["would_change"])
            self.assertIn("README.md", result["would_change"])
            self.assertFalse((root / "LICENSE").exists())
            self.assertFalse((root / "README.md").exists())
            self.assertEqual(result["default_branch_push"], "forbidden")

    def test_profile_assets_are_bundled(self) -> None:
        for name in PUBLISH.PROFILE_ASSETS:
            self.assertTrue((PUBLISH.PROFILE_SOURCE / name).is_file(), name)

    def test_prepare_package_writes_license_readme_and_profile(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "manifest.json").write_text(
                json.dumps({"upstream_inspiration": "https://github.com/example/upstream"}),
                encoding="utf-8",
            )
            result = PUBLISH.prepare_package(
                root,
                {
                    "name": "qiaomu-demo",
                    "description": "把重复工作流整理成可验证的 qiaomu skill。",
                    "version": "1.0.0",
                    "owner": "向阳乔木",
                },
                "joeseesun",
                "qiaomu-demo",
                write=True,
                include_profile=True,
            )
            self.assertEqual(result["failures"], [])
            self.assertTrue((root / "LICENSE").is_file())
            self.assertIn(PUBLISH.PROFILE_START, (root / "README.md").read_text(encoding="utf-8"))
            for name in PUBLISH.PROFILE_ASSETS.values():
                self.assertTrue((root / PUBLISH.PROFILE_TARGET / name).is_file())

    def test_local_sync_preserves_previous_copy_outside_skill_discovery(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            home = base / "home"
            source = base / "source"
            target = home / ".agents" / "skills" / "qiaomu-demo"
            source.mkdir(parents=True)
            target.mkdir(parents=True)
            (source / "SKILL.md").write_text("new\n", encoding="utf-8")
            (target / "SKILL.md").write_text("old\n", encoding="utf-8")
            with patch.object(PUBLISH.Path, "home", return_value=home):
                result = PUBLISH.sync_local(source, "qiaomu-demo")
            self.assertEqual(result["status"], "updated")
            self.assertEqual((target / "SKILL.md").read_text(encoding="utf-8"), "new\n")
            backup = Path(result["backup"])
            self.assertIn("skill-backups", backup.parts)
            self.assertEqual((backup / "SKILL.md").read_text(encoding="utf-8"), "old\n")


if __name__ == "__main__":
    unittest.main()
