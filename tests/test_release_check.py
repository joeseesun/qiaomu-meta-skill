#!/usr/bin/env python3
"""Tests for release-readiness evidence checks."""

from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("release_check", ROOT / "scripts" / "release_check.py")
if SPEC is None or SPEC.loader is None:  # pragma: no cover
    raise RuntimeError("unable to load release_check.py")
RELEASE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RELEASE)


class ReleaseCheckTest(unittest.TestCase):
    def test_secret_scan_reports_location_without_value(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            credential = "abcdefgh" + "ijklmnop"
            key_name = "api_" + "key"
            (root / "config.md").write_text(key_name + ' = "' + credential + '"\n', encoding="utf-8")
            result = RELEASE.scan_secrets(root)
        self.assertEqual(result, [{"file": "config.md", "line": 1, "kind": "assigned credential"}])

    def test_version_consistency_detects_stale_skill_ir(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "reports").mkdir()
            (root / "manifest.json").write_text(
                json.dumps({"name": "qiaomu-test", "version": "2.0.0"}), encoding="utf-8"
            )
            (root / "reports" / "skill-ir.json").write_text(
                json.dumps({"package": {"name": "qiaomu-test", "version": "1.0.0"}}), encoding="utf-8"
            )
            (root / "reports" / "trigger-eval.json").write_text(
                json.dumps({"ok": True, "summary": {"total": 1, "passed": 1}}), encoding="utf-8"
            )
            result = RELEASE.version_consistency(root)
        self.assertFalse(result["ok"])
        self.assertTrue(any("version" in item.lower() for item in result["failures"]))

    def test_secret_scan_skips_fixtures_and_env_references_but_keeps_real_values(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "fixture.js").write_text(
                "token: 'opaque-provider-token',\n"
                "clientSecret: 'client-secret-fixture',\n"
                'API_KEY="${LISTENHUB_API_KEY:-fallback}"\n'
                "api_key = '" + "kq_live_" + "9f8a7b6c5d4e3f2a1b0c'\n",
                encoding="utf-8",
            )
            findings = RELEASE.scan_secrets(root)
        self.assertEqual([item["line"] for item in findings], [4])

    def test_current_package_contains_no_secret_like_values(self) -> None:
        self.assertEqual(RELEASE.scan_secrets(ROOT), [])

    def test_published_phase_can_verify_from_main(self) -> None:
        self.assertEqual(RELEASE.feature_branch_status("main", "published"), "pass")
        self.assertEqual(RELEASE.feature_branch_status("main", "pr"), "block")

    def test_behavior_spec_is_not_provider_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "reports").mkdir()
            (root / "reports" / "output-evidence.json").write_text(
                json.dumps({"ok": True, "evidence_kind": "behavior_specification"}), encoding="utf-8"
            )
            status, evidence = RELEASE.output_evidence_status(root)
        self.assertEqual(status, "warn")
        self.assertIn("not provider/human evidence", evidence["missing_evidence"])


if __name__ == "__main__":
    unittest.main()
