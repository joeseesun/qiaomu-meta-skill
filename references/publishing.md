# Self-Contained Skill Publishing

`qiaomu-meta-skill` owns the complete public release path. Do not require or invoke a separate publisher skill after this package is selected.

## Capability contract

The bundled `scripts/publish_skill.py` covers the useful behavior learned from `qiaomu-skill-publisher` and adds governed release safety:

1. strict `SKILL.md` and `manifest.json` identity/version checks
2. MIT `LICENSE` creation when missing
3. README generation or quality validation
4. bundled Qiaomu profile/QR assets and idempotent README block injection
5. GitHub owner/repository detection without conflating repository and skill names
6. repository creation with a baseline default branch when needed
7. feature-branch commit and push; direct default-branch push is forbidden
8. pull-request creation, PR gate execution, review/check inspection, and optional merge
9. immutable version guard: an existing `vX.Y.Z` release requires a version bump
10. GitHub Release creation, `npx skills add --list` discovery, isolated clean install, and optional canonical local sync

## Commands

Read-only audit:

```bash
python3 scripts/publish_skill.py /path/to/skill --dry-run
```

Prepare LICENSE, README and Qiaomu profile locally without GitHub writes:

```bash
python3 scripts/publish_skill.py /path/to/skill --prepare-only
```

Full publication after the user explicitly asks to publish:

```bash
python3 scripts/publish_skill.py /path/to/skill
```

Stop after a passing PR when merge approval must happen elsewhere:

```bash
python3 scripts/publish_skill.py /path/to/skill --no-merge
```

Verify an already released version without creating commits or releases:

```bash
python3 scripts/publish_skill.py /path/to/skill --verify-only
```

Useful target controls:

- `--github-user OWNER`
- `--repo-name REPO`
- `--branch codex/...`
- `--private`
- `--no-sync-local`
- `--skip-qiaomu-profile` only for explicitly non-Qiaomu packages

## Safety decisions

- Full publication is an external mutation and runs only after an explicit publish request.
- `--dry-run` is read-only; unlike the legacy publisher it does not silently create or modify local files.
- New repositories receive an initial README baseline, then the actual Skill enters through a feature branch and PR.
- Existing repositories never receive `HEAD:main` or equivalent direct pushes.
- Staged content passes secret scanning and `git diff --cached --check` before commit.
- Failed or pending checks, merge conflicts, or requested changes block automatic merge.
- Existing releases are immutable. Publishing new content under the same version is blocked.
- Canonical local sync skips an already-canonical source. Replacing another installed copy first moves it to `~/.agents/skill-backups`, outside recursive Skill discovery.

## Evidence boundary

The publisher proves package gates, Git/PR/Release state, discovery and installation. It does not prove the created Skill's domain output quality, user satisfaction, adoption or business outcome. Preserve those as separate output/runtime/human evidence or `missing evidence`.
