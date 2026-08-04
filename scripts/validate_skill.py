#!/usr/bin/env python3
"""Validate the lightweight Qiaomu skill package contract."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

try:
    import yaml  # type: ignore
except Exception:  # pragma: no cover - fallback keeps the script dependency-light.
    yaml = None


REQUIRED_ROOT_FILES = ["SKILL.md", "README.md", "agents/interface.yaml", "manifest.json"]
REQUIRED_FRONTMATTER = ["name", "description"]
REQUIRED_INTERFACE_FIELDS = ["display_name", "short_description", "default_prompt"]
REQUIRED_MANIFEST_FIELDS = ["name", "version", "owner", "updated_at", "status", "maturity_tier"]
IGNORED_DISCOVERY_DIRS = {".git", "dist", "node_modules", "__pycache__"}
FORBIDDEN_DISCOVERY_DEPENDENCIES = (
    '.agents/skills/find-skills/SKILL.md',
    'npx skills add https://github.com/vercel-labs/skills --skill find-skills',
)
EVIDENCE_TIERS = {"production", "library", "governed"}
MAX_PRODUCTION_SKILL_BYTES = 14_000


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(read_text(path))
    except json.JSONDecodeError as exc:
        raise ValueError(f"{path}: invalid JSON: {exc}") from exc
    if not isinstance(payload, dict):
        raise ValueError(f"{path}: expected JSON object")
    return payload


def load_yaml(path: Path) -> dict[str, Any]:
    text = read_text(path)
    if yaml is not None:
        payload = yaml.safe_load(text) or {}
        return payload if isinstance(payload, dict) else {}
    return {}


def parse_frontmatter(text: str) -> dict[str, Any]:
    if not text.startswith("---\n"):
        return {}
    lines = text.splitlines()
    try:
        end = lines[1:].index("---") + 1
    except ValueError:
        return {}
    frontmatter_text = "\n".join(lines[1:end])
    if yaml is not None:
        payload = yaml.safe_load(frontmatter_text) or {}
        return payload if isinstance(payload, dict) else {}

    data: dict[str, Any] = {}
    current_key = ""
    for raw in frontmatter_text.splitlines():
        if not raw.strip():
            continue
        if raw.startswith(" ") and current_key:
            data[current_key] = f"{data.get(current_key, '')}\n{raw.strip()}".strip()
            continue
        if ":" not in raw:
            continue
        key, value = raw.split(":", 1)
        current_key = key.strip()
        data[current_key] = value.strip().strip("'\"|")
    return data


def markdown_links(text: str) -> list[str]:
    return re.findall(r"\]\(([^)]+\.md)\)", text)


def discover_skill_entrypoints(root: Path) -> list[Path]:
    """Return exact SKILL.md entrypoints that an installer may expose recursively."""
    entries: list[Path] = []
    for path in root.rglob("SKILL.md"):
        relative = path.relative_to(root)
        if any(part in IGNORED_DISCOVERY_DIRS for part in relative.parts):
            continue
        entries.append(relative)
    return sorted(entries)


def validate_evidence_reports(
    root: Path,
    manifest: dict[str, Any],
    failures: list[str],
    warnings: list[str],
) -> None:
    tier = str(manifest.get("maturity_tier", "")).lower()
    if tier not in EVIDENCE_TIERS:
        return
    required_reports = (
        "reports/skill-ir.json",
        "reports/trigger-eval.json",
        "reports/prior-art-research.md",
        "reports/creation-handoff.md",
    )
    for relative in required_reports:
        if not (root / relative).is_file():
            failures.append(f"{tier} package missing evidence artifact: {relative}")

    ir_path = root / "reports" / "skill-ir.json"
    if ir_path.is_file():
        try:
            package = load_json(ir_path).get("package", {})
        except ValueError as exc:
            failures.append(str(exc))
            package = {}
        if package.get("name") != manifest.get("name"):
            failures.append("reports/skill-ir.json package.name does not match manifest.json")
        if package.get("version") != manifest.get("version"):
            failures.append("reports/skill-ir.json package.version does not match manifest.json")

    trigger_path = root / "reports" / "trigger-eval.json"
    if trigger_path.is_file():
        try:
            trigger = load_json(trigger_path)
        except ValueError as exc:
            failures.append(str(exc))
            trigger = {}
        if trigger.get("ok") is not True:
            failures.append("reports/trigger-eval.json is not passing")
        summary = trigger.get("summary", {})
        total = summary.get("total") if isinstance(summary, dict) else None
        passed = summary.get("passed") if isinstance(summary, dict) else None
        if not isinstance(total, int) or total <= 0 or passed != total:
            failures.append("reports/trigger-eval.json summary is incomplete or failing")

    handoff_path = root / "reports" / "creation-handoff.md"
    if handoff_path.is_file() and str(manifest.get("version")) not in read_text(handoff_path):
        warnings.append("reports/creation-handoff.md may not mention the current manifest version")


def validate(root: Path) -> dict[str, Any]:
    root = root.resolve()
    failures: list[str] = []
    warnings: list[str] = []
    manifest: dict[str, Any] = {}
    skill_bytes = 0

    for rel in REQUIRED_ROOT_FILES:
        if not (root / rel).exists():
            failures.append(f"missing required file: {rel}")

    if root.name == "qiaomu-meta-skill":
        for rel in ("SKILL.md", "README.md", "references/prior-art-research.md"):
            path = root / rel
            if not path.exists():
                continue
            normalized = read_text(path).replace("$HOME/", "").replace("~/", "")
            for forbidden in FORBIDDEN_DISCOVERY_DEPENDENCIES:
                if forbidden in normalized:
                    failures.append(f"{rel} contains external discovery-skill dependency: {forbidden}")
        for relative in ("scripts/research_prior_art.py", "scripts/release_check.py", "scripts/publish_skill.py"):
            if not (root / relative).is_file():
                failures.append(f"qiaomu-meta-skill missing built-in factory script: {relative}")

    skill_entrypoints = discover_skill_entrypoints(root)
    nested_entrypoints = [path for path in skill_entrypoints if path != Path("SKILL.md")]
    if nested_entrypoints:
        joined = ", ".join(str(path) for path in nested_entrypoints)
        failures.append(
            "nested discoverable skill entrypoints found: "
            f"{joined}; rename embedded examples to SKILL.example.md and fixtures to SKILL.fixture.md"
        )

    skill_md = root / "SKILL.md"
    if skill_md.exists():
        skill_text = read_text(skill_md)
        skill_bytes = len(skill_text.encode("utf-8"))
        frontmatter = parse_frontmatter(skill_text)
        for field in REQUIRED_FRONTMATTER:
            if not frontmatter.get(field):
                failures.append(f"SKILL.md missing frontmatter field: {field}")
        description = str(frontmatter.get("description", ""))
        if frontmatter.get("name") == "qiaomu-meta-skill":
            for token in ("skill", "qiaomu", "workflow"):
                if token not in description.lower():
                    warnings.append(f"description may be missing routing token: {token}")
        for rel in markdown_links(skill_text):
            if rel.startswith(("http://", "https://", "#")):
                continue
            if not (root / rel).exists():
                failures.append(f"SKILL.md links to missing reference: {rel}")

    readme = root / "README.md"
    if readme.exists():
        readme_text = read_text(readme)
        readme_checks = {
            "install command": "npx skills add" in readme_text,
            "natural examples": "你可以直接这样说" in readme_text,
            "verification commands": "validate_skill.py" in readme_text,
            "troubleshooting": "Troubleshooting" in readme_text,
        }
        manifest_path = root / "manifest.json"
        if manifest_path.exists():
            try:
                manifest_for_readme = load_json(manifest_path)
            except ValueError:
                manifest_for_readme = {}
            upstream = str(manifest_for_readme.get("upstream_inspiration", "")).strip()
            if upstream:
                readme_checks["declared upstream credit"] = upstream in readme_text
        for label, ok in readme_checks.items():
            if not ok:
                warnings.append(f"README may be missing {label}")

    interface_path = root / "agents" / "interface.yaml"
    if interface_path.exists():
        interface = load_yaml(interface_path)
        meta = interface.get("interface", {}) if isinstance(interface, dict) else {}
        compatibility = interface.get("compatibility", {}) if isinstance(interface, dict) else {}
        for field in REQUIRED_INTERFACE_FIELDS:
            if not meta.get(field):
                failures.append(f"agents/interface.yaml missing interface.{field}")
        targets = compatibility.get("adapter_targets", [])
        if not isinstance(targets, list) or not targets:
            failures.append("agents/interface.yaml missing compatibility.adapter_targets")
        for expected in ("openai", "claude", "generic", "agent-skills-compatible"):
            if isinstance(targets, list) and expected not in targets:
                warnings.append(f"adapter target not declared: {expected}")

    manifest_path = root / "manifest.json"
    if manifest_path.exists():
        try:
            manifest = load_json(manifest_path)
        except ValueError as exc:
            failures.append(str(exc))
            manifest = {}
        for field in REQUIRED_MANIFEST_FIELDS:
            if not manifest.get(field):
                failures.append(f"manifest.json missing field: {field}")
        if manifest.get("version") and not re.match(r"^\d+\.\d+\.\d+$", str(manifest["version"])):
            failures.append("manifest.json version must be semver-like")
        if "release_gates" not in manifest:
            warnings.append("manifest.json missing release_gates")
        if manifest.get("context_budget_tier") == "production" and skill_bytes > MAX_PRODUCTION_SKILL_BYTES:
            warnings.append(
                f"SKILL.md exceeds production context budget: {skill_bytes} > {MAX_PRODUCTION_SKILL_BYTES} bytes"
            )

    validate_evidence_reports(root, manifest, failures, warnings)

    cases_path = root / "evals" / "trigger_cases.json"
    if cases_path.exists():
        try:
            cases = load_json(cases_path)
        except ValueError as exc:
            failures.append(str(exc))
            cases = {}
        for bucket in ("should_trigger", "should_not_trigger", "near_neighbor"):
            if not cases.get(bucket):
                warnings.append(f"evals/trigger_cases.json has no {bucket} cases")
    else:
        warnings.append("evals/trigger_cases.json missing; recommended for production/library packages")

    scripts_dir = root / "scripts"
    if scripts_dir.exists():
        for script in sorted(scripts_dir.glob("*.py")):
            text = read_text(script)
            if "argparse" not in text and 'SCRIPT_INTERFACE = "internal-module"' not in text:
                warnings.append(f"script has no argparse help or internal-module marker: {script.name}")

    return {
        "ok": not failures,
        "root": str(root),
        "failures": failures,
        "warnings": warnings,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate a Qiaomu skill package.")
    parser.add_argument("skill_dir", nargs="?", default=".", help="Skill directory to validate.")
    args = parser.parse_args()

    result = validate(Path(args.skill_dir))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if not result["ok"]:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
