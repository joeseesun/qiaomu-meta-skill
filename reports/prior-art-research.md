# Prior-Art Research

## Self-contained publishing integration 2.8

- Researched at: 2026-08-04
- Reference: [`joeseesun/qiaomu-skill-publisher`](https://github.com/joeseesun/qiaomu-skill-publisher) at `8bd944b7723e710d38f9fa4034e8ba6addbbdfed`
- Scope: absorb its useful publishing behavior into `qiaomu-meta-skill` so creation and publication no longer require a second skill
- License: MIT

### Keep

- strict frontmatter parsing and repository/skill-name separation
- MIT LICENSE creation
- README generation and placeholder checks
- Qiaomu profile/QR asset injection with stable markers
- `npx skills add --list` discovery and real temporary installation
- optional canonical `~/.agents/skills/<name>` synchronization

### Adapt

- Profile assets now come from `qiaomu-meta-skill/assets/qiaomu-profile`, removing the runtime dependency on a separate `qiaomu-profile` skill.
- README validation combines publisher placeholders with the meta validator's product-page, upstream-credit and evidence requirements.
- Repository creation uses an initial baseline followed by feature-branch PR publication, including for brand-new repositories.
- Local synchronization moves an existing target to `~/.agents/skill-backups` before replacement, outside recursive skill discovery.

### Reject

- `git push origin main` and `git push HEAD:main`: conflict with governed review and the global no-default-branch rule.
- swallowing push failures and still returning a repository URL: creates false completion claims.
- deleting the existing canonical skill directory with `shutil.rmtree`: risks data loss and removes rollback.
- verifying after an unsafe direct push: install proof cannot repair a broken publication path.
- reusing an existing release version for new content: violates immutable release expectations.

### Invent

- one self-contained `scripts/publish_skill.py` with read-only dry-run, prepare-only, PR-only, full publish and verify-only modes
- PR mergeability, requested-review and status-check gate
- version immutability guard before publication
- reuse of the bundled `local / pr / published` release checker inside the publisher
- structured JSON results that separate repository, PR, release, discovery, installation and local-sync evidence

### Evidence boundary

The integration can validate packaging and publication mechanics. It cannot establish domain output quality, user adoption or business outcomes. Those remain separate output/runtime/human evidence or `missing evidence`.

- Researched at: 2026-07-30
- Scope: improve `qiaomu-meta-skill` with a repeatable discover-compare-synthesize gate
- Queries: `skill creator`, `skill evaluation`, `meta skill`, `create agent skills`
- Discovery method at research time: skills.sh via the Skills CLI plus direct source review. SkillsMP was added to the built-in method on 2026-08-03 and did not contribute to this historical shortlist.
- Rating evidence: unavailable. The public skills.sh ranking and API expose install telemetry, not user star ratings or written reviews.

| Candidate | Relevance | Installs on 2026-07-30 | Quality and trust evidence | Keep / adapt | Reject / limit | License note |
|---|---|---:|---|---|---|---|
| `anthropics/skills@skill-creator` | Direct skill creation and iteration | 333.1K–333.2K | First-party source; 165,077 repository stars; three skills.sh audits passed; actively maintained | intent capture, realistic evals, old-vs-new baseline, qualitative plus quantitative review, trigger-description optimization | do not copy its large Claude-specific orchestration or require heavy benchmarking for every skill | repository contains mixed licensing; verify file-level terms before reuse |
| `openai/skills@skill-creator` | Direct Codex-compatible authoring guidance | 2.8K–2.9K | First-party source; 24,321 repository stars; three skills.sh audits passed; actively maintained | concise instructions, progressive disclosure, appropriate degrees of freedom, initialization and validation discipline | popularity is lower and is not a quality verdict; do not treat generic anatomy text as domain insight | verify repository/file license before reuse |
| `wshobson/agents@evaluation-methodology` | Complementary evaluation discipline | 4.8K | 38,358 repository stars; MIT repository; actively maintained | weighted dimensions, trigger-first prioritization, before/after comparison, confidence/evidence awareness | do not adopt claimed scores, badges, or Monte Carlo gates without running and validating the referenced toolchain | MIT at repository level |

## Synthesis ledger

### Keep

- Search before drafting and inspect actual source, not only result snippets.
- Treat routing, output quality, robustness, and token cost as separate evaluation surfaces.
- Compare an improved skill against the old version or a no-skill baseline when the added rigor is justified.
- Use progressive disclosure and deterministic validation scripts.

### Adapt

- Make prior-art discovery mandatory for new or substantial skill work, but proportional: a compact handoff for Scaffold, a durable report for Production and above.
- Use installs as an adoption signal and first-party/audit/repository data as trust signals. Keep each signal labeled instead of collapsing them into one score.
- Keep Qiaomu's lighter gate ladder and Chinese-first packaging while borrowing rigorous evaluation patterns only where they improve the output contract.

### Reject

- Ranking candidates by installs alone.
- Calling GitHub stars, installs, curated status, or security audits “user ratings.”
- Auto-installing or executing every candidate skill during research.
- Copying upstream prose or combining entire workflows into a bloated collage.
- Requiring expensive multi-agent or Monte Carlo evaluations for low-risk personal scaffolds.

### Invent

- A four-part `keep / adapt / reject / invent` contribution ledger that makes the original synthesis explicit.
- A three-role shortlist: popularity anchor, trust anchor, and complementary specialist.
- A privacy-aware degradation path that avoids leaking sensitive search terms and records `missing evidence` instead of fabricating confidence.
- A dated `reports/prior-art-research.md` artifact linked to Production+ gates.

## Original contribution

Qiaomu Meta Skill 2.1 turns ecosystem discovery into a defensible research gate. It does not promise to choose a universal “best” skill; it selects relevant evidence, separates popularity from sentiment and trust, documents what was rejected, then requires an original contribution tied to the user's output contract.

## Missing evidence

- skills.sh did not expose a public user-rating or written-review field during this research.
- No head-to-head output benchmark was run for the three upstream skills because their platforms, toolchains, and output contracts differ.
- Repository-level stars and licenses do not automatically apply to every file; file-level reuse terms must still be checked before copying or redistribution.
