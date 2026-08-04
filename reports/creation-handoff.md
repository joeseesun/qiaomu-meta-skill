# Qiaomu Meta Skill Creation Handoff

## Result

- Skill: `qiaomu-meta-skill` 2.8.1
- Job: research, create, evaluate, package, govern, and safely publish reusable Qiaomu skills through one self-contained workflow
- Status: README showcase and privacy-safe Codex skill-history catalog prepared on a feature branch; public 2.8.1 evidence remains `missing evidence` until the release workflow completes

## Reference skills studied

### `yaojingang/yao-meta-skill`

- Why shortlisted: direct meta-skill reference with full-lifecycle engineering, evaluation, governance, and portability concepts.
- Learned: Skill IR, evidence boundaries, release gates, output evaluation, review layers, and post-release iteration.
- Applied in: Qiaomu Skill OS layers, gate ladder, Skill IR export, output-eval method, and SkillOps references.

### `wshobson/agents@evaluation-methodology`

- Why shortlisted: complementary evaluation specialist found during prior-art research.
- Learned: separate evaluation dimensions, compare before/after behavior, preserve confidence and evidence limits.
- Applied in: trigger-first evaluation, output assertions, evidence labels, and the distinction between design and validated advantages.

### `joeseesun/qiaomu-skill-publisher`

- Why shortlisted: the user's explicit reference and the existing Qiaomu implementation of LICENSE, README, Profile, repository naming and `npx` installation.
- Learned: idempotent profile markers, strict YAML handling, repository/skill-name separation, public README scaffolding, discovery and temporary installation.
- Applied in: bundled `scripts/publish_skill.py`, `references/publishing.md`, profile assets, trigger cases and publisher regression tests.

## Absorbed and rejected

- `keep`: platform-neutral intent, trigger/output evaluation, evidence-bound claims, release gates, publisher README/Profile/License preparation and install verification.
- `adapt`: compress a large Skill OS into a lighter Chinese-first Qiaomu workflow; source Qiaomu profile assets from the meta package itself; route every publication through review.
- `reject`: copying upstream dashboards; multiple creator/discovery/publisher skills; popularity-only ranking; direct default-branch push; destructive local replacement; same-version rerelease; unsupported completion claims.
- `invent`: resilient dual-catalog research, safe self-contained publisher, feature-branch-only new-repository bootstrap, PR state gate, release immutability, structured publication evidence and rollback-preserving local sync.

## Advantages and highlights

- `design advantage`: prior-art discovery, synthesis, creation, validation, and handoff remain inside one canonical workflow, avoiding conflicting creator instructions. Evidence: `SKILL.md` Router Rules and Compact Workflow.
- `design advantage`: skills.sh installs and SkillsMP repository stars remain source-separated and cannot be combined into a fake score. Evidence: `references/prior-art-research.md`.
- `design advantage`: every created Production+ skill must expose design lineage and distinguish design advantages, validated advantages, and hypotheses. Evidence: `references/creation-handoff.md`.
- `design advantage`: catalog discovery now degrades explicitly under transient failures instead of losing the whole research run or hiding missing evidence. Evidence: `scripts/search_skillsmp.py` and `scripts/research_prior_art.py`.
- `design advantage`: local, PR, and published completion states are machine-checkable instead of prose-only. Evidence: `scripts/release_check.py`.
- `design advantage`: authoring and publishing now share one authority and one gate system; a separate publisher skill is no longer required. Evidence: `scripts/publish_skill.py` and `references/publishing.md`.
- `design advantage`: the integrated publisher cannot push directly to `main/master`, reuse a released version, silently ignore a failed push, or delete an installed skill without rollback.
- `validated advantage`: publisher unit tests cover URL parsing, profile idempotence, generated README quality, default-branch rejection, pending-check blocking, read-only dry-run and bundled assets.
- `hypothesis`: the richer handoff should improve user trust and adoption decisions, but a human comprehension or install-conversion study remains `missing evidence`.
- `design advantage`: the README now leads with the user outcome, a one-line installation command, a capability comparison, natural-language examples, and 28 evidence-backed practice cases instead of internal architecture.
- `validated advantage`: the Codex history catalog distinguishes 18 public repositories from 10 local/private cases and separates created/updated packages from researched prior art without publishing raw dialogue or local paths.

## Verification and limits

- Deterministic package validation: passed with 0 failures and 0 warnings.
- Trigger eval: passed 23/23, with 0 false positives and 0 false negatives.
- Unit tests: passed 35/35, including 10 publisher-specific regressions and 3 Codex history catalog integrity/privacy checks.
- Self-contained publisher dry-run against this repository: passed, resolved `joeseesun/qiaomu-meta-skill`, planned no unwanted file changes, and reported default-branch push as forbidden.
- Independent `--prepare-only` fixture: passed; created MIT LICENSE, product README, three bundled Profile assets and an idempotent profile block, then passed the package validator with zero warnings.
- Integrated discovery verifier against the currently published repository: passed; `npx skills add joeseesun/qiaomu-meta-skill --list` found `qiaomu-meta-skill`. This verifies the verifier path; 2.8.1 requires its own post-release proof.
- Live dual-catalog smoke: passed in strict mode for `skill evaluation`; skills.sh and SkillsMP both completed, producing 9 merged candidate families with source metrics kept separate.
- Local release readiness: passed with 6 pass, 3 warn, and 0 block. Warnings accurately record the dirty worktree, unavailable clean-install proof before a remote revision exists, and missing provider/human output evidence.
- PR, merged default-branch, GitHub release, and public clean-install proof for 2.8.1: `missing evidence` until the current release workflow completes.
- Provider-backed head-to-head output evaluation: `missing evidence`.
- Human blind comparison of handoff persuasiveness: `missing evidence`.
