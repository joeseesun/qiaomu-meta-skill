# qiaomu-meta-skill

> 创建 skill 最难的不是写一份 `SKILL.md`，而是找到可信先例、守住通用边界，并证明它真的能触发、安装和发布。
>
> Turn workflows, prompts, SOPs, and notes into researched, testable, installable Qiaomu agent skills.

[![GitHub Release](https://img.shields.io/github/v/release/joeseesun/qiaomu-meta-skill?display_name=tag&sort=semver)](https://github.com/joeseesun/qiaomu-meta-skill/releases)
[![Stars](https://img.shields.io/github/stars/joeseesun/qiaomu-meta-skill?style=flat)](https://github.com/joeseesun/qiaomu-meta-skill/stargazers)
[![Last commit](https://img.shields.io/github/last-commit/joeseesun/qiaomu-meta-skill)](https://github.com/joeseesun/qiaomu-meta-skill/commits/main)
[![License](https://img.shields.io/github/license/joeseesun/qiaomu-meta-skill)](LICENSE)

**中文** | [English](#english)

```bash
npx skills add joeseesun/qiaomu-meta-skill
```

**2.8.0 已验证：** 32/32 单元测试、23/23 触发评测、0 个包验证问题；skills.sh 与 SkillsMP 双目录研究和自包含安全发布 dry-run 均通过。

## 这是什么

`qiaomu-meta-skill` 是乔木的 skill 工厂。它基于 [`yaojingang/yao-meta-skill`](https://github.com/yaojingang/yao-meta-skill) 的 Skill OS 2.0 思路做了轻量化改造：保留语义契约、触发评估、发布门禁和运维反馈，但默认先做成能真实复用的轻包。

它是乔木 skill 创建与发布流程的唯一权威，内部已经包含 skills.sh + SkillsMP 双目录发现、GitHub 验源、对比和综合方法，以及 LICENSE、README、乔木 Profile、功能分支、PR、Release、发现和干净安装的完整发布器。命中后不再叠加 generic `skill-creator`，也不需要下载或安装其他 discovery / publisher skill。

## 2.8.0 升级亮点

- 新增 `scripts/publish_skill.py`，元 Skill 现在真正自包含发布能力，不再依赖 `qiaomu-skill-publisher`。
- 完整吸收 MIT LICENSE、README 产品页、乔木 Profile/二维码、仓库名识别、`npx --list` 和临时目录安装验证。
- 新仓库先建立最小默认分支，再让真实 Skill 通过 `codex/` 功能分支和 PR 进入；现有仓库同样禁止直推 `main/master`。
- PR 冲突、失败/未完成检查、requested changes 会阻断自动合并；已存在的 `vX.Y.Z` 会阻断同版本重发。
- 成功合并后创建 GitHub Release，核对远端版本并做隔离 HOME 干净安装；本机同步会先备份旧版本，不直接删除。
- 保留 2.7 的双目录研究、三阶段发布检查、版本/报告一致性、secret scan 和上下文预算门禁。

它适合：

- 把 workflow 变成 skill
- 给已有 skill 做重构、收敛和补强
- 迁移旧 skill，检查安装入口和递归发现风险
- 只做路由、输出评估或发布证据审计，不越权改文件
- 补 trigger、边界、Skill IR、评估和治理文件
- 直接把 skill 做完并由自己完成 GitHub 发布
- 打包成适合乔木团队复用的版本

## 安装

```bash
npx skills add joeseesun/qiaomu-meta-skill
```

验证：

```bash
ls ~/.agents/skills/qiaomu-meta-skill
python3 ~/.agents/skills/qiaomu-meta-skill/scripts/validate_skill.py ~/.agents/skills/qiaomu-meta-skill
```

### 前置条件

- [ ] 已安装 Node.js 18+；运行 `node --version` 确认。
- [ ] 可以运行 npx；运行 `npx --version` 确认。
- [ ] 需要执行内置 Python 验证器时，已安装 Python 3.9+；运行 `python3 --version` 确认。
- [ ] 需要搜索 SkillsMP、skills.sh 或 GitHub 时，当前环境允许只读访问这些公开服务。

## 你可以直接这样说

- “把这个流程整理成一个 skill”
- “把这个流程整理成一个 skill 并发布”
- “帮我优化这个 skill 的触发词和边界”
- “给这个 skill 补上评估和治理文件”
- “基于这个开源 skill 升级乔木 meta skill”
- “把这套 SOP、脚本和提示词封装成团队可复用的 qiaomu skill”

## Skill OS 2.0 乔木版

这次升级不是把 Yao 的完整大系统照搬过来，而是把高价值机制收敛成乔木日常可执行的 6 层：

| 层级 | 乔木版做法 | 什么时候需要 |
|---|---|---|
| Intent | 先讲清重复任务、输入、输出、边界和参考对象 | 创建或重构任何 skill |
| Skill IR | 用 `reports/skill-ir.json` 保存平台中立语义契约 | 团队复用、公开发布、跨平台适配 |
| Package | 保持 `SKILL.md` 精简，把长规则放进 `references/` | 所有 skill |
| Eval | 先做 trigger eval，必要时补 output eval | 触发边界或输出质量有风险 |
| Review | 检查 README、安装、脚本、信任边界和发布证据 | 公开或团队分发 |
| Operate | 记录显式反馈、失败和漂移信号，形成下一轮提案 | 已发布或长期复用 |

## 推荐流程

1. 判断它是不是值得做成 skill。一次性翻译、总结、解释，不强行包装。
2. 使用内置双目录发现流程，从 skills.sh 和 SkillsMP 找到真正相关的热门、可信和互补候选，再回到 GitHub 验源去重。
3. 分开核对安装量、公开评价、来源、维护、安全和许可证；没有评分字段就明确说没有，不能拿 stars 代替评分。
4. 用 `keep / adapt / reject / invent` 提炼共性、舍弃不适合的部分，并补出自己的新机制。
5. 单一样本反馈先抽象成领域中立失效机制；核心规则要跨无关领域验证，领域细节优先留在 eval fixture。
6. 写清 `description`，先验证触发边界，再扩目录。
7. 选择模式：`Scaffold`、`Production`、`Library`、`Governed`。
8. 按风险加门禁，不为好看堆文件。
9. 根据动词控制动作边界：创建/重构可以改文件；审计/评估/诊断默认只给发现与修复建议。
10. 发布前把 README 当成 GitHub 产品页，而不是内部笔记。
11. 创建完成时向用户说明参考了哪些 skill、分别学习了什么、舍弃了什么、乔木版有哪些原创亮点，以及哪些优势已经验证。
12. 公共发布时走验证、安装证明、分支/PR/合并流程。

## 自包含发布

只检查，不修改本地文件或 GitHub：

```bash
python3 scripts/publish_skill.py /path/to/skill --dry-run
```

只补齐 LICENSE、README 与乔木 Profile：

```bash
python3 scripts/publish_skill.py /path/to/skill --prepare-only
```

用户明确要求发布后，执行完整流程：

```bash
python3 scripts/publish_skill.py /path/to/skill
```

这条命令会完成：包验证与 secret scan → 功能分支 → PR → 检查与讨论状态读取 → squash merge → `vX.Y.Z` Release → `npx skills add --list` → 隔离安装 → 本机正式目录同步。

如需把合并留给人工或 CI：

```bash
python3 scripts/publish_skill.py /path/to/skill --no-merge
```

已发布版本只做验证：

```bash
python3 scripts/publish_skill.py /path/to/skill --verify-only
```

详细参数与安全边界见 [`references/publishing.md`](references/publishing.md)。

## 先研究，再创造

先例发现已内置，不检查也不安装其他 skill。优先用统一研究器查询 2–4 组关键词：

```bash
python3 scripts/research_prior_art.py "<query 1>" "<query 2>" --strict --summary \
  --output reports/prior-art-candidates.json
```

底层仍是直接目录查询：

```bash
npx --yes skills find "<query>"
python3 scripts/search_skillsmp.py "<query>" --limit 20 --sort stars
```

skills.sh 负责安装采用信号，SkillsMP 扩展 GitHub、多语言、创作者和职业覆盖；最终按 GitHub 来源与 skill 路径去重。默认覆盖“安装量最高的相关项”“第一方或高可信项”“提供互补机制的专项项”，但不会机械选择榜首。

`skills.sh` 的 installs 是安装遥测；SkillsMP 的 `stars` 是源仓库 stars。两者都不是用户评分，也不能相加。Meta skill 会把安装量、仓库 stars、官方/第一方身份、安全审计、维护活跃度、许可证和真实用户评价分开记录；没有评分证据就写 `rating evidence unavailable`。

详细规则见 [`references/prior-art-research.md`](references/prior-art-research.md)。Production 以上或研究投入较多的 skill 会保留 `reports/prior-art-research.md`。

## 创建完成时怎么汇报

最终回复不能只说“已创建并验证”。至少要让用户看到：

1. **参考学习**：列出 2–4 个真正相关的 skill、来源与选择理由。
2. **分别学了什么**：每个候选对应一个具体机制，以及它落在新 skill 的哪个部分。
3. **没有照搬什么**：说明因过拟合、风险、臃肿、平台绑定或证据不足而舍弃的做法。
4. **乔木版亮点**：解释原创连接与目标场景优势。
5. **证据等级**：区分 `design advantage`、`validated advantage` 和仍待验证的 `hypothesis`。
6. **验证与边界**：给出 trigger、output、runtime 或 human evidence，并明确 `missing evidence`。

详细模板见 [`references/creation-handoff.md`](references/creation-handoff.md)。Production 以上同时保存 `reports/creation-handoff.md`。

## 本地验证命令

```bash
python3 scripts/validate_skill.py .
python3 scripts/export_skill_ir.py . --output reports/skill-ir.json
python3 scripts/trigger_eval.py . --cases evals/trigger_cases.json --output reports/trigger-eval.json
python3 scripts/search_skillsmp.py "seo" --limit 5 --sort stars
python3 scripts/research_prior_art.py "skill creator" "skill evaluation" --strict --summary
python3 scripts/release_check.py . --phase local --run-tests
python3 scripts/publish_skill.py . --dry-run
python3 -m py_compile scripts/*.py
python3 -m unittest discover -s tests -p 'test_*.py'
```

## 输出示例

一次合格的升级或创建通常会留下这些结果：

```text
Updated: SKILL.md
Updated: agents/interface.yaml
Updated: README.md
Added: references/intent-dialogue.md
Added: evals/trigger_cases.json
Generated: reports/skill-ir.json
Generated: reports/trigger-eval.json
Validated: package contract OK
```

## 目录结构

- `SKILL.md`：路由和最小执行骨架
- `agents/interface.yaml`：跨平台适配层
- `references/`：方法论、边界和发布门禁
- `scripts/`：确定性验证、IR 导出、触发评估
- `scripts/research_prior_art.py`：双目录查询、标准化、跨目录归并和降级证据
- `scripts/release_check.py`：本地、PR、已发布三阶段完成门禁
- `scripts/publish_skill.py`：LICENSE/README/Profile 准备、仓库、功能分支、PR、Release、发现、安装和安全同步
- `evals/`：触发和输出评估样例
- `reports/`：评估、决策和证据，默认由脚本生成

根目录的 `SKILL.md` 是唯一可发现入口。仓库内嵌示例应命名为 `SKILL.example.md`，测试夹具应命名为 `SKILL.fixture.md`；复制成独立 skill 后再恢复为 `SKILL.md`。验证器会阻断嵌套的精确 `SKILL.md`，避免安装后被 agent 递归误激活。

## 乔木命名与版权

- 默认生成的 skill 名称使用 `qiaomu-` 前缀。
- 名称尽量短，优先不超过三个连字符分隔词，例如 `qiaomu-cover-designer`。
- 生成的 skill 默认加入向阳乔木版权与联系方式：
  - Copyright (c) 向阳乔木
  - X: https://x.com/vista8
  - GitHub: https://github.com/joeseesun/

## 发布提示

这个 skill 设计成可发布的库型包。发布到 GitHub 前，先确认：

- `SKILL.md` 的 frontmatter 完整
- 需要的 `references/` 已补齐
- README 能让陌生用户知道它能做什么、为什么值得装、怎么安装和怎么排错
- `scripts/validate_skill.py`、`scripts/export_skill_ir.py`、`scripts/trigger_eval.py` 能通过
- `scripts/release_check.py --phase local --run-tests` 没有阻断项
- `scripts/publish_skill.py . --dry-run` 能解析正确仓库与版本，且报告 `default_branch_push: forbidden`
- 根目录之外没有会被递归发现的 `SKILL.md`
- 声称人工盲评时，答案钥匙与匿名评审包分离，且 reviewer、判断、理由、先判断后揭晓的 attestation 齐全
- 没有把 API key、cookie、私有路径或未验证的“已完成”声明写进公开文件

## GitHub README 标准

创建或发布 skill 时，README 不是 `SKILL.md` 的复制品，而是给人看的 GitHub 产品页。

必须覆盖：

- 一句话价值主张
- 一行安装命令
- 真实自然语言触发示例
- 前置条件和验证命令
- 具体输出示例
- 环境变量/配置说明
- Troubleshooting
- 风险边界和致谢

详细模板见 [`references/github-readme-playbook.md`](references/github-readme-playbook.md)。

## Troubleshooting

| 问题 | 常见原因 | 处理方式 |
|---|---|---|
| `validate_skill.py` 报 frontmatter 缺字段 | `SKILL.md` 没有 `name` 或 `description` | 补齐 YAML frontmatter，并保持 description 可自然触发 |
| `trigger_eval.py` 有 false positive | description 太泛，或 negative pattern 不够 | 收窄 description，补 should-not-trigger / near-neighbor case |
| README 看起来像内部笔记 | 直接复制了 `SKILL.md` 的执行规则 | 按产品页重写：价值、安装、触发例子、输出、配置、排错 |
| 发布后别人装不上 | 没有做 install proof 或遗漏依赖 | 跑安装验证，补前置条件和验证命令 |
| SkillsMP 偶发 `IncompleteRead` | 上游分块响应中断 | 保留默认重试；仍失败时统一研究器会记录 `missing evidence`，不要伪造目录结果 |
| 本地和 GitHub 版本不一致 | 只改了 Manifest 或尚未完成 PR/Release | 依次运行 `release_check.py --phase local/pr/published` |
| 发布器拒绝当前版本 | GitHub 已存在同名 `vX.Y.Z` Release | 更新 `manifest.json`、Skill IR、触发报告和交接报告中的版本后再发布 |
| 发布器拒绝合并 PR | 有冲突、失败/未完成检查或 requested changes | 先处理 PR 讨论与检查，不绕过门禁 |
| 找不到乔木 Profile 资产 | Skill 包不完整或资产被删 | 重新安装完整 `qiaomu-meta-skill`；发布器只使用自身 bundled assets |

## 上游致谢

本 skill 的 2.0 升级参考了 [`yaojingang/yao-meta-skill`](https://github.com/yaojingang/yao-meta-skill) 的 Skill IR、评估证据、Review Studio、信任边界和 SkillOps 思路。2.8 的自包含发布能力学习自 [`joeseesun/qiaomu-skill-publisher`](https://github.com/joeseesun/qiaomu-skill-publisher)，保留其 README/Profile/License/安装验证能力，并用功能分支、PR、版本不可变和非破坏同步替换直接推默认分支与覆盖目录。

Upstream inspiration: https://github.com/yaojingang/yao-meta-skill; https://github.com/joeseesun/qiaomu-skill-publisher

## 限制、安全与支持

- 目录安装量和 GitHub stars 只作为来源独立的采用信号，不等于评分或质量证明。
- 研究候选时只读取公开元数据与源码；不会为了学习而执行未经审查的第三方脚本。
- 发布属于外部写操作，只有用户明确要求时才执行，并走功能分支、PR、合并和公开安装验证。
- API key、Cookie、私有路径和运行时数据库不得进入公开仓库；发布门禁会扫描常见敏感信息形态。
- 遇到问题可在 [GitHub Issues](https://github.com/joeseesun/qiaomu-meta-skill/issues) 提交可复现输入、期望结果和验证输出。

<!-- qiaomu-profile:start -->
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
| <img src="assets/qiaomu-profile/qiaomu_reward_qr.png" alt="向阳乔木打赏二维码" width="180" /> | <img src="assets/qiaomu-profile/qiaomu_wechat_public_account_qr.jpg" alt="向阳乔木推荐看公众号二维码" width="180" /> |
| 感谢支持乔木持续分享 AI 实践 | 扫码关注「向阳乔木推荐看」 |

<!-- qiaomu-profile:end -->

---

<a name="english"></a>
## English

`qiaomu-meta-skill` is a governed skill factory for turning repeated workflows, prompts, transcripts, docs, SOPs, scripts, and notes into reusable agent-skill packages.

It keeps prior-art research, synthesis, authoring, trigger evaluation, Skill IR, release gates, and the final evidence handoff inside one canonical workflow. It queries skills.sh and SkillsMP directly, keeps catalog metrics separate, and does not install a second creator or discovery skill.

### Install

```bash
npx skills add joeseesun/qiaomu-meta-skill
```

Verify the installed package:

```bash
test -f ~/.agents/skills/qiaomu-meta-skill/SKILL.md
python3 ~/.agents/skills/qiaomu-meta-skill/scripts/validate_skill.py \
  ~/.agents/skills/qiaomu-meta-skill
```

### Natural-language examples

- “Turn this repeated workflow into a reusable Qiaomu skill.”
- “Research the strongest related skills, then synthesize and publish a better governed package.”
- “Audit this skill's trigger boundary and release evidence without changing files.”

### What 2.8.0 verifies

- resilient SkillsMP requests with bounded retries and explicit degradation
- one dual-catalog prior-art runner without fake cross-catalog scoring
- manifest, Skill IR, trigger-report, secret, Git, PR, release, and clean-install gates
- self-contained LICENSE/README/Profile preparation, feature-branch-only GitHub publishing, release immutability, PR check/review gating, discovery and clean installation
- 32/32 unit tests and 23/23 trigger cases in the local 2.8 release candidate

### Limits

Catalog popularity is not a quality rating. Unavailable ratings, provider runs, human blind reviews, and install proof must remain labelled as missing evidence. Publishing is performed only on explicit request and must use a feature branch, pull request, merged default branch, release, and public clean-install verification.

## License

MIT
