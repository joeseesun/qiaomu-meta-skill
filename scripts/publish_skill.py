#!/usr/bin/env python3
"""Safely prepare and publish a Qiaomu agent skill through GitHub review gates.

This script absorbs the useful behavior of qiaomu-skill-publisher while keeping
qiaomu-meta-skill's stricter release contract: no direct default-branch push,
immutable released versions, PR inspection, a versioned GitHub Release, and a
clean npx installation check before reporting success.
"""

from __future__ import annotations

import argparse
import datetime as dt
import importlib.util
import json
import os
import re
import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = PACKAGE_ROOT / "scripts"
PROFILE_SOURCE = PACKAGE_ROOT / "assets" / "qiaomu-profile"
PROFILE_TARGET = Path("assets/qiaomu-profile")
PROFILE_ASSETS = {
    "qiaomu_avatar.jpeg": "qiaomu_avatar.jpeg",
    "qiaomu_reward_qr.png": "qiaomu_reward_qr.png",
    "qiaomu_wechat_public_account_qr.jpg": "qiaomu_wechat_public_account_qr.jpg",
}
PROFILE_START = "<!-- qiaomu-profile:start -->"
PROFILE_END = "<!-- qiaomu-profile:end -->"
DEFAULT_BRANCHES = {"main", "master"}


def load_module(name: str, path: Path) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:  # pragma: no cover
        raise RuntimeError(f"unable to load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


VALIDATOR = load_module("qiaomu_publish_validate", SCRIPT_DIR / "validate_skill.py")
RELEASE = load_module("qiaomu_publish_release", SCRIPT_DIR / "release_check.py")


class PublishError(RuntimeError):
    pass


@dataclass
class CommandResult:
    args: list[str]
    returncode: int | None
    stdout: str
    stderr: str

    @property
    def ok(self) -> bool:
        return self.returncode == 0


Runner = Callable[..., CommandResult]


def run(
    args: list[str],
    cwd: Path,
    *,
    timeout: float = 300.0,
    env: dict[str, str] | None = None,
    check: bool = True,
) -> CommandResult:
    try:
        completed = subprocess.run(
            args,
            cwd=cwd,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
            env=env,
        )
        result = CommandResult(args, completed.returncode, completed.stdout.strip(), completed.stderr.strip())
    except (OSError, subprocess.TimeoutExpired) as exc:
        result = CommandResult(args, None, "", str(exc))
    if check and not result.ok:
        command = " ".join(args)
        detail = result.stderr or result.stdout or "unknown error"
        raise PublishError(f"command failed: {command}\n{detail}")
    return result


def load_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise PublishError(f"{path} must contain a JSON object")
    return payload


def identity(root: Path) -> dict[str, str]:
    skill_path = root / "SKILL.md"
    manifest_path = root / "manifest.json"
    if not skill_path.is_file():
        raise PublishError("missing SKILL.md")
    if not manifest_path.is_file():
        raise PublishError("missing manifest.json; public Qiaomu skills require versioned metadata")
    frontmatter = VALIDATOR.parse_frontmatter(skill_path.read_text(encoding="utf-8"))
    manifest = load_json(manifest_path)
    name = str(frontmatter.get("name", "")).strip()
    description = " ".join(str(frontmatter.get("description", "")).split())
    version = str(manifest.get("version", "")).strip()
    owner = str(manifest.get("owner", "向阳乔木")).strip() or "向阳乔木"
    if not name or not description:
        raise PublishError("SKILL.md frontmatter requires name and description")
    if manifest.get("name") != name:
        raise PublishError("manifest.json name does not match SKILL.md")
    if not re.fullmatch(r"\d+\.\d+\.\d+", version):
        raise PublishError("manifest.json version must be semantic X.Y.Z")
    return {"name": name, "description": description, "version": version, "owner": owner}


def parse_origin(url: str) -> tuple[str | None, str | None]:
    match = re.search(r"github\.com[/:]([^/]+)/([^/]+?)(?:\.git)?$", url.strip())
    return (match.group(1), match.group(2)) if match else (None, None)


def origin_identity(root: Path, runner: Runner = run) -> tuple[str | None, str | None]:
    result = runner(["git", "remote", "get-url", "origin"], root, check=False)
    return parse_origin(result.stdout) if result.ok else (None, None)


def check_cli_prerequisites(root: Path, runner: Runner = run) -> None:
    for command in (["git", "--version"], ["gh", "--version"], ["npx", "--version"]):
        runner(command, root)
    runner(["gh", "auth", "status"], root)


def github_user(root: Path, explicit: str | None, origin_owner: str | None, runner: Runner = run) -> str:
    if explicit:
        return explicit
    if origin_owner:
        return origin_owner
    result = runner(["gh", "api", "user", "--jq", ".login"], root)
    if not result.stdout:
        raise PublishError("unable to resolve GitHub user")
    return result.stdout.strip()


def ensure_license(root: Path, owner: str, *, write: bool) -> list[str]:
    path = root / "LICENSE"
    if path.exists():
        return []
    if write:
        year = dt.datetime.now().year
        path.write_text(
            f"""MIT License

Copyright (c) {year} {owner}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the \"Software\"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
""",
            encoding="utf-8",
        )
    return ["LICENSE"]


def profile_block() -> str:
    return f"""{PROFILE_START}
## 关于向阳乔木

向阳乔木（乔向阳 / Joe）是一位实践型 AI 产品与内容创作者，长期把前沿 AI 变化转译成可复用的工作流、产品判断、AI 编程实践、AI 搜索实践和 GEO/AI 营销方法。

- 个人网站: https://qiaomu.ai
- 博客: https://blog.qiaomu.ai
- X: https://x.com/vista8
- GitHub: https://github.com/joeseesun/
- 微信公众号: 向阳乔木推荐看

### 支持与关注

| 打赏支持 | 微信公众号 |
|---|---|
| <img src=\"assets/qiaomu-profile/qiaomu_reward_qr.png\" alt=\"向阳乔木打赏二维码\" width=\"180\" /> | <img src=\"assets/qiaomu-profile/qiaomu_wechat_public_account_qr.jpg\" alt=\"向阳乔木推荐看公众号二维码\" width=\"180\" /> |
| 感谢支持乔木持续分享 AI 实践 | 扫码关注「向阳乔木推荐看」 |

{PROFILE_END}"""


def marker_outside_fence(text: str, marker: str, start: int = 0) -> int:
    in_fence = False
    offset = 0
    for line in text.splitlines(keepends=True):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
        index = line.find(marker) if not in_fence else -1
        absolute = offset + index if index >= 0 else -1
        if absolute >= start:
            return absolute
        offset += len(line)
    return -1


def insert_profile(text: str) -> str:
    block = profile_block()
    start = marker_outside_fence(text, PROFILE_START)
    end = marker_outside_fence(text, PROFILE_END, max(0, start)) if start >= 0 else -1
    if start >= 0 and end > start:
        end += len(PROFILE_END)
        return text[:start].rstrip() + "\n\n" + block + "\n\n" + text[end:].lstrip()
    insertion = re.search(r"\n##\s+(?:License|许可证|授权)\b|\n<a name=\"english\"></a>|\n##\s+English\b", text, re.I)
    if insertion:
        return text[: insertion.start()].rstrip() + "\n\n" + block + "\n\n" + text[insertion.start() :].lstrip()
    return text.rstrip() + "\n\n" + block + "\n"


def ensure_profile(root: Path, *, write: bool) -> list[str]:
    if not PROFILE_SOURCE.is_dir():
        raise PublishError(f"bundled profile assets missing: {PROFILE_SOURCE}")
    changes: list[str] = []
    target = root / PROFILE_TARGET
    for source_name, target_name in PROFILE_ASSETS.items():
        source = PROFILE_SOURCE / source_name
        destination = target / target_name
        if not source.is_file():
            raise PublishError(f"bundled profile asset missing: {source_name}")
        same = destination.is_file() and source.read_bytes() == destination.read_bytes()
        if not same:
            changes.append(destination.relative_to(root).as_posix())
            if write:
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, destination)
    readme = root / "README.md"
    if readme.is_file():
        current = readme.read_text(encoding="utf-8")
        updated = insert_profile(current)
        if updated != current:
            changes.append("README.md profile block")
            if write:
                readme.write_text(updated, encoding="utf-8")
    return changes


def generated_readme(meta: dict[str, str], github_owner: str, repo: str, upstream: str) -> str:
    first = re.split(r"[。.]", meta["description"], maxsplit=1)[0].strip()
    upstream_line = f"Upstream inspiration: {upstream}" if upstream else "Upstream inspiration: none declared"
    return f"""# {repo}

> {first}。

[![Stars](https://img.shields.io/github/stars/{github_owner}/{repo}?style=flat-square)](https://github.com/{github_owner}/{repo}/stargazers)
[![Last commit](https://img.shields.io/github/last-commit/{github_owner}/{repo}?style=flat-square)](https://github.com/{github_owner}/{repo}/commits/main)
[![License](https://img.shields.io/github/license/{github_owner}/{repo}?style=flat-square)](LICENSE)

```bash
npx skills add {github_owner}/{repo}
```

## 为什么值得用

{meta["description"]}

## 你可以直接这样说

- “使用 ${meta['name']} 处理这个任务。”
- “先审计输入和边界，再按 ${meta['name']} 完成并验证。”
- “按这个 skill 的完整工作流执行，不要跳过门禁。”

## 安装与验证

```bash
npx skills add {github_owner}/{repo}
test -f ~/.agents/skills/{meta['name']}/SKILL.md
python3 ~/.agents/skills/{meta['name']}/scripts/validate_skill.py ~/.agents/skills/{meta['name']}
```

## 前置条件

- [ ] 已安装 Node.js 与 npx：`node --version && npx --version`
- [ ] 已安装 Python 3：`python3 --version`
- [ ] 已阅读该 Skill 的权限与风险边界

## 输出

安装后得到完整 Skill 包，包括 `SKILL.md`、`references/`、`scripts/`、`evals/` 和已声明的资产；具体输出以 Skill 的 Output Contract 为准。

## 风险与边界

- Skill 以本地文件和明确授权为边界，不应静默扩大权限。
- 发布前检查公开文件中没有密钥、Cookie、私有路径或未经验证的结果声明。
- Agent Skill 具有执行能力；安装前请审查源码与权限。

## Troubleshooting

| 问题 | 原因 | 解决 |
|---|---|---|
| `No valid skills found` | YAML frontmatter 无效 | 使用块标量 `description: |` 并重新验证 |
| 找不到 Skill | 安装源或名称错误 | 运行 `npx skills add {github_owner}/{repo} --list` |
| 验证脚本失败 | 前置依赖或证据文件缺失 | 按错误路径补齐后重新运行 |

## 致谢

{upstream_line}

## License

MIT

Copyright (c) 向阳乔木
X: https://x.com/vista8 · GitHub: https://github.com/joeseesun/
"""


PLACEHOLDERS = (
    r"<!--\s*TODO",
    r"your-org/your-repo",
    r"docs/assets/product-screenshot\.png",
    r"特性\s*1[：:]描述",
    r"\[用户的自然语言输入\]",
    r"\[解决方案\]",
    r"（在此补充",
)


def check_readme(root: Path, upstream: str, *, require_profile: bool) -> list[str]:
    path = root / "README.md"
    if not path.is_file():
        return ["README.md missing"]
    text = path.read_text(encoding="utf-8")
    failures = [f"README placeholder found: {pattern}" for pattern in PLACEHOLDERS if re.search(pattern, text, re.I)]
    requirements = {
        "install command": "npx skills add" in text,
        "natural-language examples": "你可以直接这样说" in text or "Natural-language examples" in text,
        "verification command": "validate_skill.py" in text,
        "prerequisite checklist": "- [ ]" in text,
        "troubleshooting": "Troubleshooting" in text,
        "license": "## License" in text or "## 许可证" in text,
        "upstream credit": not upstream or upstream in text,
        "Qiaomu profile": not require_profile or (PROFILE_START in text and PROFILE_END in text),
    }
    failures.extend(f"README missing {label}" for label, passed in requirements.items() if not passed)
    return failures


def prepare_package(
    root: Path,
    meta: dict[str, str],
    github_owner: str,
    repo: str,
    *,
    write: bool,
    include_profile: bool,
) -> dict[str, Any]:
    manifest = load_json(root / "manifest.json")
    upstream = str(manifest.get("upstream_inspiration", "")).strip()
    changes = ensure_license(root, meta["owner"], write=write)
    readme = root / "README.md"
    if not readme.exists():
        changes.append("README.md")
        if write:
            readme.write_text(generated_readme(meta, github_owner, repo, upstream), encoding="utf-8")
    if include_profile:
        changes.extend(ensure_profile(root, write=write))
    failures = [] if not write and not readme.exists() else check_readme(root, upstream, require_profile=include_profile)
    return {"changes": sorted(set(changes)), "failures": failures}


def repo_exists(root: Path, slug: str, runner: Runner = run) -> bool:
    return runner(["gh", "repo", "view", slug, "--json", "url"], root, check=False).ok


def release_exists(root: Path, slug: str, version: str, runner: Runner = run) -> bool:
    return runner(["gh", "release", "view", f"v{version}", "--repo", slug], root, check=False).ok


def is_git_repo(root: Path, runner: Runner = run) -> bool:
    return runner(["git", "rev-parse", "--is-inside-work-tree"], root, check=False).stdout == "true"


def default_branch(root: Path, slug: str, runner: Runner = run) -> str:
    result = runner(
        ["gh", "repo", "view", slug, "--json", "defaultBranchRef", "--jq", ".defaultBranchRef.name"],
        root,
        check=False,
    )
    return result.stdout.strip() if result.ok and result.stdout.strip() else "main"


def branch_slug(name: str, version: str) -> str:
    safe_name = re.sub(r"[^a-z0-9-]+", "-", name.lower()).strip("-")
    return f"codex/publish-{safe_name}-v{version.replace('.', '-')}"


def assert_feature_branch(branch: str, default: str) -> None:
    if not branch or branch in DEFAULT_BRANCHES or branch == default:
        raise PublishError(f"refusing direct default-branch publication: {branch or '<detached>'}")
    if not branch.startswith("codex/"):
        raise PublishError(f"publication branch must use the codex/ prefix: {branch}")


def copy_package(source: Path, destination: Path) -> None:
    ignore = shutil.ignore_patterns(".git", ".DS_Store", "__pycache__", "*.pyc", "*.pyo")
    shutil.copytree(source, destination, dirs_exist_ok=True, ignore=ignore)


def staged_changes(root: Path, runner: Runner = run) -> bool:
    return not runner(["git", "diff", "--cached", "--quiet"], root, check=False).ok


def pr_is_mergeable(payload: dict[str, Any]) -> tuple[bool, list[str]]:
    blockers: list[str] = []
    mergeable = payload.get("mergeable")
    if mergeable != "MERGEABLE":
        blockers.append(f"PR mergeability is not ready: {mergeable or 'unknown'}")
    if payload.get("reviewDecision") == "CHANGES_REQUESTED":
        blockers.append("PR has requested changes")
    if any(review.get("state") == "CHANGES_REQUESTED" for review in payload.get("reviews") or []):
        blockers.append("a PR review requested changes")
    for check in payload.get("statusCheckRollup") or []:
        conclusion = check.get("conclusion")
        status = check.get("status")
        state = check.get("state")
        if conclusion in {"FAILURE", "CANCELLED", "TIMED_OUT", "ACTION_REQUIRED"}:
            blockers.append(f"check failed: {check.get('name', 'unknown')}")
        elif state in {"ERROR", "FAILURE", "PENDING", "EXPECTED"}:
            blockers.append(f"status check not successful: {check.get('context', 'unknown')}")
        elif status and (status != "COMPLETED" or conclusion is None):
            blockers.append(f"check still pending: {check.get('name', 'unknown')}")
    return not blockers, blockers


def verify_discovery(root: Path, slug: str, skill_name: str, runner: Runner = run) -> dict[str, Any]:
    listed = runner(["npx", "--yes", "skills", "add", slug, "--list"], root, timeout=300, check=False)
    ok = listed.ok and "Found" in listed.stdout and skill_name in listed.stdout and "No valid skills found" not in listed.stdout
    return {"ok": ok, "returncode": listed.returncode, "skill": skill_name, "found": skill_name in listed.stdout}


def sync_local(source: Path, skill_name: str) -> dict[str, Any]:
    target = Path.home() / ".agents" / "skills" / skill_name
    if target.resolve() == source.resolve():
        return {"status": "skipped", "target": str(target), "reason": "source is already canonical"}
    staging = target.parent / f".{skill_name}.incoming"
    backup_root = Path.home() / ".agents" / "skill-backups"
    timestamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    backup = backup_root / f"{skill_name}-{timestamp}"
    if staging.exists():
        raise PublishError(f"stale local sync staging path exists: {staging}")
    copy_package(source, staging)
    if target.exists() or target.is_symlink():
        backup_root.mkdir(parents=True, exist_ok=True)
        target.rename(backup)
    staging.rename(target)
    return {"status": "updated" if backup.exists() else "created", "target": str(target), "backup": str(backup) if backup.exists() else None}


def release_check(root: Path, phase: str, *, install: bool) -> dict[str, Any]:
    report = RELEASE.evaluate(root, phase, run_tests=True, install_check=install)
    if not report["ok"]:
        blocks = [item["gate"] for item in report["gates"] if item["status"] == "block"]
        raise PublishError(f"{phase} release gates blocked: {', '.join(blocks)}")
    return report


def publish(args: argparse.Namespace, runner: Runner = run) -> dict[str, Any]:
    source = Path(args.skill_dir).expanduser().resolve()
    if not source.is_dir():
        raise PublishError(f"skill directory does not exist: {source}")
    meta = identity(source)
    check_cli_prerequisites(source, runner)
    origin_owner, origin_repo = origin_identity(source, runner)
    owner = github_user(source, args.github_user, origin_owner, runner)
    repo = args.repo_name or origin_repo or meta["name"]
    slug = f"{owner}/{repo}"
    planned = prepare_package(
        source,
        meta,
        owner,
        repo,
        write=not args.dry_run,
        include_profile=not args.skip_qiaomu_profile,
    )
    if args.dry_run:
        return {
            "ok": not planned["failures"],
            "mode": "dry-run",
            "skill": meta,
            "repository": slug,
            "repository_exists": repo_exists(source, slug, runner),
            "would_change": planned["changes"],
            "failures": planned["failures"],
            "default_branch_push": "forbidden",
        }
    if planned["failures"]:
        raise PublishError("README preparation failed: " + "; ".join(planned["failures"]))
    package = VALIDATOR.validate(source)
    if not package["ok"] or package["warnings"]:
        raise PublishError(f"package validation failed: {package}")
    if args.prepare_only:
        return {"ok": True, "mode": "prepare-only", "skill": meta, "repository": slug, "changes": planned["changes"]}

    exists = repo_exists(source, slug, runner)
    if exists and release_exists(source, slug, meta["version"], runner):
        if not args.verify_only:
            raise PublishError(
                f"release v{meta['version']} already exists; bump manifest.json before publishing changes, "
                "or use --verify-only"
            )
        discovery = verify_discovery(source, slug, meta["name"], runner)
        published = release_check(source, "published", install=True)
        return {"ok": discovery["ok"] and published["ok"], "mode": "verify-only", "repository": slug, "discovery": discovery, "release": published}

    if args.verify_only:
        raise PublishError("--verify-only requires an existing versioned release")

    if not exists:
        visibility = "--private" if args.private else "--public"
        runner(
            [
                "gh",
                "repo",
                "create",
                slug,
                visibility,
                "--add-readme",
                "--description",
                meta["description"][:300],
            ],
            source,
        )

    source_origin = origin_identity(source, runner)
    source_matches = is_git_repo(source, runner) and source_origin == (owner, repo)
    temporary: tempfile.TemporaryDirectory[str] | None = None
    if source_matches:
        workspace = source
    else:
        temporary = tempfile.TemporaryDirectory(prefix="qiaomu-skill-publish-")
        workspace = Path(temporary.name) / repo
        runner(["git", "clone", f"https://github.com/{slug}.git", str(workspace)], source)
        copy_package(source, workspace)

    default = default_branch(workspace, slug, runner)
    current_result = runner(["git", "branch", "--show-current"], workspace, check=False)
    current = current_result.stdout.strip() if current_result.ok else ""
    branch = args.branch or (current if current and current != default else branch_slug(meta["name"], meta["version"]))
    if current != branch:
        runner(["git", "switch", "-c", branch], workspace)
    assert_feature_branch(branch, default)

    local_gates = release_check(workspace, "local", install=False)
    secrets = RELEASE.scan_secrets(workspace)
    if secrets:
        raise PublishError(f"secret scan blocked publication: {secrets}")
    runner(["git", "add", "-A"], workspace)
    runner(["git", "diff", "--cached", "--check"], workspace)
    if staged_changes(workspace, runner):
        runner(["git", "commit", "-m", f"release: prepare {meta['name']} v{meta['version']}"], workspace)
    runner(["git", "push", "-u", "origin", branch], workspace)

    existing_pr = runner(
        ["gh", "pr", "list", "--repo", slug, "--head", branch, "--state", "open", "--json", "url", "--jq", ".[0].url"],
        workspace,
        check=False,
    )
    pr_url = existing_pr.stdout.strip() if existing_pr.ok else ""
    if not pr_url:
        body = (
            f"Publish `{meta['name']}` v{meta['version']} through the Qiaomu governed release flow.\n\n"
            "- package validation and secret scan run locally\n"
            "- no direct default-branch push\n"
            "- merge is followed by a versioned Release and clean installation check"
        )
        created = runner(
            [
                "gh",
                "pr",
                "create",
                "--repo",
                slug,
                "--base",
                default,
                "--head",
                branch,
                "--title",
                f"release: {meta['name']} v{meta['version']}",
                "--body",
                body,
            ],
            workspace,
        )
        pr_url = created.stdout.strip().splitlines()[-1]
    pr_gates = release_check(workspace, "pr", install=False)
    review = runner(
        [
            "gh",
            "pr",
            "view",
            pr_url,
            "--repo",
            slug,
            "--json",
            "url,state,mergeable,reviewDecision,statusCheckRollup,comments,reviews",
        ],
        workspace,
    )
    review_payload = json.loads(review.stdout)
    mergeable, blockers = pr_is_mergeable(review_payload)
    if not mergeable:
        raise PublishError("PR is not ready to merge: " + "; ".join(blockers))
    if args.no_merge:
        return {
            "ok": True,
            "mode": "pr-ready",
            "repository": slug,
            "branch": branch,
            "pull_request": pr_url,
            "local_gates": local_gates["summary"],
            "pr_gates": pr_gates["summary"],
            "discussion_count": len(review_payload.get("comments") or []),
        }

    runner(
        [
            "gh",
            "pr",
            "merge",
            pr_url,
            "--repo",
            slug,
            "--squash",
            "--delete-branch",
            "--subject",
            f"release: {meta['name']} v{meta['version']}",
        ],
        workspace,
    )
    runner(["git", "fetch", "origin", default], workspace)
    runner(["git", "switch", default], workspace)
    runner(["git", "pull", "--ff-only", "origin", default], workspace)
    runner(
        [
            "gh",
            "release",
            "create",
            f"v{meta['version']}",
            "--repo",
            slug,
            "--target",
            default,
            "--title",
            f"v{meta['version']}",
            "--generate-notes",
        ],
        workspace,
    )
    discovery = verify_discovery(workspace, slug, meta["name"], runner)
    if not discovery["ok"]:
        raise PublishError(f"npx skill discovery failed: {discovery}")
    published = release_check(workspace, "published", install=True)
    sync = {"status": "skipped"} if args.no_sync_local else sync_local(source, meta["name"])
    result = {
        "ok": True,
        "mode": "published",
        "repository": f"https://github.com/{slug}",
        "release": f"https://github.com/{slug}/releases/tag/v{meta['version']}",
        "install": f"npx skills add {slug}",
        "pull_request": pr_url,
        "discovery": discovery,
        "published_gates": published["summary"],
        "sync": sync,
        "direct_default_branch_push": False,
    }
    if temporary is not None:
        temporary.cleanup()
    return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Prepare and publish a Qiaomu skill through branch, PR, Release, and install gates.")
    parser.add_argument("skill_dir", help="Skill package directory")
    parser.add_argument("--github-user")
    parser.add_argument("--repo-name")
    parser.add_argument("--branch", help="Feature branch; defaults to codex/publish-<skill>-v<version>")
    parser.add_argument("--private", action="store_true")
    parser.add_argument("--dry-run", action="store_true", help="Read-only audit; do not edit files or GitHub")
    parser.add_argument("--prepare-only", action="store_true", help="Prepare local LICENSE/README/Profile and stop")
    parser.add_argument("--verify-only", action="store_true", help="Verify an existing release and clean install")
    parser.add_argument("--no-merge", action="store_true", help="Stop after the PR passes local and PR gates")
    parser.add_argument("--no-sync-local", action="store_true", help="Do not sync a noncanonical source into ~/.agents/skills")
    parser.add_argument("--skip-qiaomu-profile", action="store_true", help="Only for explicitly non-Qiaomu packages")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    try:
        result = publish(args)
    except (PublishError, json.JSONDecodeError) as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False, indent=2))
        raise SystemExit(2)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if not result.get("ok"):
        raise SystemExit(2)


if __name__ == "__main__":
    main()
