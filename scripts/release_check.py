#!/usr/bin/env python3
"""Audit local, PR, or published release readiness for a Qiaomu skill."""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import subprocess
import tempfile
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("qiaomu_validate_skill", SCRIPT_DIR / "validate_skill.py")
if SPEC is None or SPEC.loader is None:  # pragma: no cover
    raise RuntimeError("unable to load validate_skill.py")
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)

SECRET_PATTERNS = {
    "OpenAI-like key": re.compile(r"sk-[A-Za-z0-9_-]{20,}"),
    "AWS access key": re.compile(r"AKIA[0-9A-Z]{16}"),
    "private key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "assigned credential": re.compile(
        r'''(?i)(?:api[_-]?key|secret|password|token)\s*[:=]\s*["']([^"']{8,})["']'''
    ),
}
# Assigned values that are evidently not credentials: environment/template references and
# self-describing test fixtures. Real keys never contain these words.
NON_CREDENTIAL_VALUE = re.compile(
    r"(?i)^\$[{(]|\b(?:fixture|synthetic|opaque|dummy|placeholder|example|redacted)\b|(?:^|[-_])(?:fixture|synthetic|opaque|dummy|placeholder)(?:[-_]|$)"
)
SCAN_SUFFIXES = {".md", ".json", ".yaml", ".yml", ".py", ".js", ".ts", ".sh", ".toml"}
IGNORED_PARTS = {".git", "__pycache__", "node_modules", "dist"}


def load_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return payload


def run(command: list[str], cwd: Path, timeout: float = 120.0, env: dict[str, str] | None = None) -> dict[str, Any]:
    try:
        completed = subprocess.run(
            command,
            cwd=cwd,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
            env=env,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {"ok": False, "returncode": None, "stdout": "", "stderr": str(exc)}
    return {
        "ok": completed.returncode == 0,
        "returncode": completed.returncode,
        "stdout": completed.stdout.strip(),
        "stderr": completed.stderr.strip(),
    }


def scan_secrets(root: Path) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    for path in root.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in SCAN_SUFFIXES:
            continue
        relative = path.relative_to(root)
        if any(part in IGNORED_PARTS for part in relative.parts):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for line_number, line in enumerate(text.splitlines(), 1):
            for label, pattern in SECRET_PATTERNS.items():
                match = pattern.search(line)
                if not match:
                    continue
                if match.groups() and NON_CREDENTIAL_VALUE.search(match.group(1)):
                    continue
                findings.append({"file": str(relative), "line": line_number, "kind": label})
    return findings


def version_consistency(root: Path) -> dict[str, Any]:
    manifest = load_json(root / "manifest.json")
    version = str(manifest.get("version", ""))
    name = str(manifest.get("name", ""))
    evidence: dict[str, Any] = {"manifest_name": name, "manifest_version": version}
    failures: list[str] = []
    ir_path = root / "reports" / "skill-ir.json"
    if not ir_path.is_file():
        failures.append("reports/skill-ir.json missing")
    else:
        package = load_json(ir_path).get("package", {})
        evidence["skill_ir_name"] = package.get("name")
        evidence["skill_ir_version"] = package.get("version")
        if package.get("name") != name:
            failures.append("Skill IR package name does not match manifest")
        if package.get("version") != version:
            failures.append("Skill IR version does not match manifest")
    trigger_path = root / "reports" / "trigger-eval.json"
    if not trigger_path.is_file():
        failures.append("reports/trigger-eval.json missing")
    else:
        trigger = load_json(trigger_path)
        evidence["trigger_ok"] = trigger.get("ok")
        evidence["trigger_summary"] = trigger.get("summary")
        if trigger.get("ok") is not True:
            failures.append("trigger evaluation is not passing")
    return {"ok": not failures, "failures": failures, "evidence": evidence}


def repo_slug(root: Path) -> str | None:
    result = run(["git", "remote", "get-url", "origin"], root)
    if not result["ok"]:
        return None
    url = str(result["stdout"])
    match = re.search(r"github\.com[/:]([^/]+/[^/.]+)(?:\.git)?$", url)
    return match.group(1) if match else None


def gate(items: list[dict[str, Any]], name: str, status: str, evidence: Any) -> None:
    items.append({"gate": name, "status": status, "evidence": evidence})


def feature_branch_status(branch: str, phase: str) -> str:
    if not branch:
        return "block"
    if phase in {"local", "pr"} and branch in {"main", "master"}:
        return "block"
    return "pass"


def output_evidence_status(root: Path) -> tuple[str, dict[str, Any]]:
    path = root / "reports" / "output-evidence.json"
    if not path.is_file():
        return "warn", {"path": str(path.relative_to(root)), "missing_evidence": True}
    try:
        payload = load_json(path)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        return "block", {"path": str(path.relative_to(root)), "error": str(exc)}
    kind = payload.get("evidence_kind")
    recognized = kind in {"provider_backed", "human_blind_review"}
    passed = payload.get("ok") is True
    if recognized and passed:
        return "pass", {"path": str(path.relative_to(root)), "evidence_kind": kind, "ok": True}
    return "warn", {
        "path": str(path.relative_to(root)),
        "evidence_kind": kind,
        "ok": payload.get("ok"),
        "missing_evidence": "recorded fixtures or behavior specifications are not provider/human evidence",
    }


def evaluate(root: Path, phase: str, run_tests: bool, install_check: bool) -> dict[str, Any]:
    root = root.resolve()
    gates: list[dict[str, Any]] = []
    package = VALIDATOR.validate(root)
    gate(gates, "package_validation", "pass" if package["ok"] and not package["warnings"] else "block", package)

    consistency = version_consistency(root)
    gate(gates, "version_and_report_consistency", "pass" if consistency["ok"] else "block", consistency)

    secrets = scan_secrets(root)
    gate(gates, "secret_scan", "pass" if not secrets else "block", {"findings": secrets})

    diff_check = run(["git", "diff", "--check"], root)
    gate(gates, "git_diff_check", "pass" if diff_check["ok"] else "block", diff_check)

    branch_result = run(["git", "branch", "--show-current"], root)
    branch = str(branch_result["stdout"]) if branch_result["ok"] else ""
    gate(gates, "feature_branch", feature_branch_status(branch, phase), {"branch": branch})

    status_result = run(["git", "status", "--porcelain"], root)
    dirty = bool(status_result["stdout"]) if status_result["ok"] else True
    dirty_status = "warn" if phase == "local" and dirty else ("block" if dirty else "pass")
    gate(gates, "clean_worktree", dirty_status, {"dirty": dirty})

    if run_tests:
        tests = run(["python3", "-m", "unittest", "discover", "-s", "tests", "-p", "test_*.py"], root)
        gate(gates, "unit_tests", "pass" if tests["ok"] else "block", tests)
    else:
        gate(gates, "unit_tests", "warn", {"missing_evidence": "rerun with --run-tests"})

    slug = repo_slug(root)
    manifest = load_json(root / "manifest.json")
    version = str(manifest.get("version"))
    name = str(manifest.get("name"))

    if phase == "pr":
        if not slug or not branch:
            gate(gates, "remote_branch", "block", {"repo": slug, "branch": branch})
        else:
            remote_branch = run(["git", "ls-remote", "--heads", "origin", branch], root)
            exists = remote_branch["ok"] and bool(remote_branch["stdout"])
            gate(gates, "remote_branch", "pass" if exists else "block", {"repo": slug, "branch": branch})

    if phase == "pr":
        if slug and branch:
            pr = run(["gh", "pr", "list", "--repo", slug, "--head", branch, "--state", "open", "--json", "url,state"], root)
            rows = json.loads(pr["stdout"] or "[]") if pr["ok"] else []
            gate(gates, "open_pr", "pass" if rows else "block", {"pull_requests": rows, "error": pr["stderr"]})
        else:
            gate(gates, "open_pr", "block", {"repo": slug, "branch": branch})

    if phase == "published":
        if slug:
            default_branch_result = run(
                ["gh", "repo", "view", slug, "--json", "defaultBranchRef", "--jq", ".defaultBranchRef.name"], root
            )
            default_branch = default_branch_result["stdout"] or "main"
            remote_manifest = run(
                ["gh", "api", f"repos/{slug}/contents/manifest.json?ref={default_branch}", "-H", "Accept: application/vnd.github.raw+json"],
                root,
            )
            try:
                remote_version = json.loads(remote_manifest["stdout"]).get("version") if remote_manifest["ok"] else None
            except json.JSONDecodeError:
                remote_version = None
            gate(
                gates,
                "remote_default_version",
                "pass" if remote_version == version else "block",
                {"repo": slug, "default_branch": default_branch, "local_version": version, "remote_version": remote_version},
            )
            release = run(["gh", "release", "view", f"v{version}", "--repo", slug, "--json", "url,tagName,isDraft"], root)
            gate(gates, "github_release", "pass" if release["ok"] else "block", release)
        else:
            gate(gates, "remote_default_version", "block", {"repo": None})
            gate(gates, "github_release", "block", {"repo": None})

    if install_check and slug:
        with tempfile.TemporaryDirectory() as directory:
            temp_home = Path(directory)
            import os

            env = dict(os.environ)
            env["HOME"] = str(temp_home)
            install = run(
                ["npx", "--yes", "skills", "add", slug, "--skill", name, "--yes"],
                temp_home,
                timeout=300,
                env=env,
            )
            installed = temp_home / ".agents" / "skills" / name / "SKILL.md"
            evidence = {**install, "installed_entrypoint": str(installed), "entrypoint_exists": installed.is_file()}
            gate(gates, "clean_install", "pass" if install["ok"] and installed.is_file() else "block", evidence)
    else:
        gate(gates, "clean_install", "warn", {"missing_evidence": "rerun with --install-check after the target revision is remote"})

    output_status, output_evidence = output_evidence_status(root)
    gate(gates, "provider_or_human_output_evidence", output_status, output_evidence)

    blocks = [item for item in gates if item["status"] == "block"]
    warnings = [item for item in gates if item["status"] == "warn"]
    return {
        "ok": not blocks,
        "phase": phase,
        "root": str(root),
        "version": version,
        "repository": slug,
        "summary": {"pass": len(gates) - len(blocks) - len(warnings), "warn": len(warnings), "block": len(blocks)},
        "gates": gates,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check Qiaomu skill release readiness.")
    parser.add_argument("skill_dir", nargs="?", default=".")
    parser.add_argument("--phase", choices=("local", "pr", "published"), default="local")
    parser.add_argument("--run-tests", action="store_true")
    parser.add_argument("--install-check", action="store_true")
    parser.add_argument("--output")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = evaluate(Path(args.skill_dir), args.phase, args.run_tests, args.install_check)
    rendered = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        path = Path(args.output)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)
    if not result["ok"]:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
