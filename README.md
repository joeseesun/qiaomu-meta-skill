# qiaomu-meta-skill

> 把一句「把这个流程做成 Skill」，变成一个真正能被发现、能稳定触发、能通过验证、还能一键开源的 Skill。

[![GitHub Release](https://img.shields.io/github/v/release/joeseesun/qiaomu-meta-skill?display_name=tag&sort=semver)](https://github.com/joeseesun/qiaomu-meta-skill/releases)
[![Stars](https://img.shields.io/github/stars/joeseesun/qiaomu-meta-skill?style=flat)](https://github.com/joeseesun/qiaomu-meta-skill/stargazers)
[![Last commit](https://img.shields.io/github/last-commit/joeseesun/qiaomu-meta-skill)](https://github.com/joeseesun/qiaomu-meta-skill/commits/main)
[![License](https://img.shields.io/github/license/joeseesun/qiaomu-meta-skill)](LICENSE)

```bash
npx skills add joeseesun/qiaomu-meta-skill
```

安装以后，你只需要把提示词、SOP、聊天记录、旧 Skill、脚本或一个模糊想法交给 Agent：

```text
用乔木元 Skill，把这套工作流做成一个可复用的 Skill；
先研究同类热门 Skill，完成触发评测和安全检查，然后发布到 GitHub。
```

它会自己完成：**需求收敛 → 同类检索 → 取长避短 → Skill 设计 → 触发评测 → 格式校验 → README → API 泄露检查 → PR → Release → npx 安装验证**。

**v2.8.1 本地候选已验证：** 35/35 单元测试、23/23 触发评测、0 个包校验问题。公开发布证据以 [Releases](https://github.com/joeseesun/qiaomu-meta-skill/releases) 为准。

## 为什么我做了这个

Skill 正在变成 Agent 时代真正可复用的软件单元，但“写一份 `SKILL.md`”离一个好用的 Skill 还很远：

- 描述写得太宽，会到处误触发；写得太窄，又永远叫不出来。
- 把一段长 Prompt 换个文件名，不会自动变成可靠工作流。
- 不研究已有方案，很容易重复造一个更差的轮子。
- 本地能跑，不代表别人能安装，更不代表可以安全发布。
- README、许可证、版本、密钥泄露、PR、Release 和安装证明，经常在最后一步一起失控。

Anthropic 与 OpenAI 的官方 `skill-creator` 奠定了很好的基础。乔木元 Skill 在此之上补齐了我实际做几十个 Skill 时最需要的一段：**先搜索再创造、用证据控制质量，并把成品安全发布给别人使用。**

初始方法来自搭档姚老师的 [`yaojingang/yao-meta-skill`](https://github.com/yaojingang/yao-meta-skill)。我继续研究并整合 Anthropic、OpenAI 等 Agent Skill 的公开最佳实践，随后加入 skills.sh、SkillsMP、GitHub 验源、乔木式轻量门禁与自包含发布能力。

## 它比普通 Skill 创建器多做什么

| 能力 | 普通“生成 SKILL.md” | qiaomu-meta-skill |
|---|---:|---:|
| 从 Prompt / SOP / 对话 / 旧 Skill 提炼工作流 | ✓ | ✓ |
| 先搜索 skills.sh 与 SkillsMP 的相关 Skill |  | ✓ |
| 回到 GitHub 核对来源、维护、安全与许可证 |  | ✓ |
| 记录 `keep / adapt / reject / invent`，避免拼贴抄袭 |  | ✓ |
| 测试该触发与不该触发的真实说法 | 视实现而定 | ✓ |
| 区分设计优势、已验证优势和待验证假设 |  | ✓ |
| 校验目录、版本、上下文预算与递归发现 |  | ✓ |
| README、MIT License、乔木 Profile 自动准备 |  | ✓ |
| Secret / API 泄露扫描 |  | ✓ |
| 功能分支、PR、检查、Release |  | ✓ |
| `npx skills add` 公开发现与隔离安装验证 |  | ✓ |

它不是让 Skill 变得更重，而是让复杂度与风险匹配：个人试验走轻量 `Scaffold`，公开发布才启用完整 `Governed` 门禁。

## 真实做出来过什么

截至 2026-08-04，我扫描并去重了本机 Codex 会话、创建交接和 prior-art 报告。能确认有明确创建或实质重构证据的 Qiaomu Skill 共 **28 个**；其中 **18 个已有公开仓库**。这不是“可能适用”的演示列表，而是真实对话留下的工作结果。

### 已公开，可直接查看

| Skill | 它解决什么问题 |
|---|---|
| [`qiaomu-campus-resume`](https://github.com/joeseesun/qiaomu-campus-resume) | 一问一答深挖大学生经历，生成 ATS 友好的精美 PDF 简历 |
| [`qiaomu-course-designer`](https://github.com/joeseesun/qiaomu-course-designer) | 通过依赖感知访谈，把模糊课程想法收敛成课程蓝图 |
| [`qiaomu-ppt`](https://github.com/joeseesun/qiaomu-ppt) | 从资料研究、大纲到可编辑、可验证的 PPT / HTML Deck |
| [`qiaomu-bento-ppt`](https://github.com/joeseesun/qiaomu-bento-ppt) | 独立生成和编辑 Bento 风格演示文稿 |
| [`qiaomu-cover-designer`](https://github.com/joeseesun/qiaomu-cover-designer) | 从 URL 或内容生成多风格高级概念封面 |
| [`qiaomu-book-script`](https://github.com/joeseesun/qiaomu-book-script) | 把非虚构书籍提炼成能让人停下手指的口播稿 |
| [`qiaomu-drama-generator`](https://github.com/joeseesun/qiaomu-drama-generator) | 生成中文竖屏短剧的人设、大纲与完整剧本 |
| [`qiaomu-xinzhiyuan-title`](https://github.com/joeseesun/qiaomu-xinzhiyuan-title) | 基于真实语料学习新智元风格的 AI 科技标题 |
| [`qiaomu-read-helper`](https://github.com/joeseesun/qiaomu-read-helper) | 用飞书章节、划线和评论完成共读与读书笔记 |
| [`qiaomu-goal-meta-skill`](https://github.com/joeseesun/qiaomu-goal-meta-skill) | 把模糊任务收敛成结果、验证、边界完整的 Codex Goal |
| [`qiaomu-ai-prd`](https://github.com/joeseesun/qiaomu-ai-prd) | 把一句产品想法变成 AI 编程助手可执行的 PRD |
| [`qiaomu-model-cli`](https://github.com/joeseesun/qiaomu-model-cli) | 并发编排 Grok、Kimi 与 Claude Code 等本地模型 CLI |
| [`qiaomu-ai-access`](https://github.com/joeseesun/qiaomu-ai-access) | 检查 AI 服务访问环境信号与合规隐私卫生 |
| [`qiaomu-seo`](https://github.com/joeseesun/qiaomu-seo) | 研究、审计、实施并验证传统搜索与 AI 搜索 SEO |
| [`qiaomu-youtube-download`](https://github.com/joeseesun/qiaomu-youtube-download) | 搜索、下载并验证 YouTube 视频、音频、字幕与元数据 |
| [`qiaomu-wx-video`](https://github.com/joeseesun/qiaomu-wx-video) | 下载并验证微信视频号视频或直播回放 |
| [`qiaomu-music-publisher`](https://github.com/joeseesun/qiaomu-music-publisher) | 从 Suno 下载歌曲、歌词和封面并完成音乐发布工作流 |
| [`qiaomu-meta-skill`](https://github.com/joeseesun/qiaomu-meta-skill) | 元 Skill 自己也持续用同一套研究、评测和发布门禁迭代 |

<details>
<summary><strong>另外 10 个本地或未公开案例</strong></summary>

`qiaomu-vps-website-ops`、`qiaomu-profile`、`qiaomu-xhs-promo`、`qiaomu-xhs-writer`、`qiaomu-kazike-title`、`qiaomu-kazike-writer`、`qiaomu-xinzhiyuan-writer`、`qiaomu-twitter`、`qiaomu-douyin`、`qiaomu-cut`。

它们只用于证明场景覆盖，不提供不可访问的仓库链接，也不把“本地存在”表述为“已经公开发布”。

</details>

完整扫描口径与去重清单见 [`reports/codex-skill-catalog.md`](reports/codex-skill-catalog.md)。扫描只输出 Skill 名称、用途和公开状态，不复制私人对话、附件、Token 或本机路径。

## 它研究过哪些 Skill

乔木元 Skill 不会看到排行榜第一名就照搬。它会从 skills.sh、SkillsMP 与 GitHub 找出“流行度锚点、可信来源、互补专家”，阅读源文件后再决定保留、改造、拒绝或原创。

<details>
<summary><strong>已进入公开 prior-art 报告的完整去重清单</strong></summary>

### Skill 创建与评测

- [`anthropics/skills@skill-creator`](https://github.com/anthropics/skills)
- [`openai/skills@skill-creator`](https://github.com/openai/skills)
- [`wshobson/agents@evaluation-methodology`](https://github.com/wshobson/agents)
- [`yaojingang/yao-meta-skill`](https://github.com/yaojingang/yao-meta-skill)
- [`joeseesun/qiaomu-skill-publisher`](https://github.com/joeseesun/qiaomu-skill-publisher)

### 访谈、课程与简历

- [`alirezarezvani/claude-skills@grill-me`](https://github.com/alirezarezvani/claude-skills/tree/main/engineering/grill-me/skills/grill-me)
- [`mattpocock/skills@grill-me`](https://github.com/mattpocock/skills/tree/main/skills/productivity/grill-me)
- [`addyosmani/agent-skills@interview-me`](https://github.com/addyosmani/agent-skills/tree/main/skills/interview-me)
- [`tyrealq/q-skills@q-educator`](https://github.com/tyrealq/q-skills/tree/main/skills/q-educator)
- [`kevintsai1202/teaching-site-skills@course-outline-design`](https://github.com/kevintsai1202/teaching-site-skills/tree/main/course-outline-design)
- [`pedrohcgs/claude-code-my-workflow@interview-me`](https://github.com/pedrohcgs/claude-code-my-workflow/tree/main/.claude/skills/interview-me)
- [`pedrohcgs/claude-code-my-workflow@syllabus`](https://github.com/pedrohcgs/claude-code-my-workflow/tree/main/.claude/skills/syllabus)
- [`rendercv/rendercv-skill`](https://github.com/rendercv/rendercv-skill)
- [`erichowens/some_claude_skills@cv-creator`](https://skills.sh/erichowens/some_claude_skills/cv-creator)
- [`eachlabs/skills@resume-design-generation`](https://skills.sh/eachlabs/skills/resume-design-generation)
- [`amruthpillai/reactive-resume`](https://github.com/amruthpillai/reactive-resume)
- [`xitanggg/open-resume`](https://github.com/xitanggg/open-resume)
- [`jakegut/resume`](https://github.com/jakegut/resume)
- [`posquit0/Awesome-CV`](https://github.com/posquit0/Awesome-CV)
- [`liantze/AltaCV`](https://github.com/liantze/AltaCV)
- [`tw93/kami`](https://github.com/tw93/kami)
- [`mmmlllnnn/ResumeCollection`](https://github.com/mmmlllnnn/ResumeCollection)

### 内容、社交与 SEO

- [`autoclaw-cc/xiaohongshu-mcp-skills`](https://github.com/autoclaw-cc/xiaohongshu-mcp-skills)
- [`vivy-yi/xiaohongshu-skills@content-marketing`](https://github.com/vivy-yi/xiaohongshu-skills)
- `vivy-yi/xiaohongshu-skills@copywriting-skills`
- `vivy-yi/xiaohongshu-skills@title-writing`
- `vivy-yi/xiaohongshu-skills@hashtag-optimization`
- [`redfox-data/redfox-community@xiaohongshu-rewrite`](https://github.com/redfox-data/redfox-community)
- [`langchain-ai/deepagents@social-media`](https://github.com/langchain-ai/deepagents)
- [`content-designer/ux-writing-skill`](https://github.com/content-designer/ux-writing-skill)
- [`zc277584121/marketing-skills@content-rewrite`](https://github.com/zc277584121/marketing-skills)
- [`coreyhaines31/marketingskills@seo-audit`](https://github.com/coreyhaines31/marketingskills)
- `coreyhaines31/marketingskills@programmatic-seo`
- `coreyhaines31/marketingskills@ai-seo`
- [`agricidaniel/claude-seo@seo-ecommerce`](https://github.com/agricidaniel/claude-seo)
- [`affaan-m/ECC@seo`](https://github.com/affaan-m/ECC)
- [`firecrawl/firecrawl-workflows@firecrawl-seo-audit`](https://github.com/firecrawl/firecrawl-workflows)

### 对话中明确要求研究或吸收的项目

- [`hugohe3/ppt-master`](https://github.com/hugohe3/ppt-master)
- [`zarazhangrui/frontend-slides`](https://github.com/zarazhangrui/frontend-slides)
- [`nyblnet/bento`](https://github.com/nyblnet/bento)
- [`yArna/isChinaUser`](https://github.com/yArna/isChinaUser)
- [`larksuite/cli`](https://github.com/larksuite/cli)
- 本地 `baocut`、`gsap`、`lottie` Skill，以及 `qiaomu-mondo-poster-design` 等乔木已有能力

</details>

“研究过”只表示它被纳入有日期的对比与取舍，或在对话中被明确要求查阅，不代表依赖、安装、背书或复制。安装量是采用信号，仓库 stars 是仓库关注度；两者都不是用户评分，也不会被加成一个虚假的总分。

## 你可以直接这样说

- “把这个提示词升级成一个可以给团队复用的 Skill。”
- “采访我，把这套隐性工作方法整理成 Skill；每次只问一个关键问题。”
- “先搜索同类热门 Skill，分析优缺点，再做一个不抄袭的版本。”
- “优化这个已有 Skill 的触发率、准确性和指令遵循。”
- “审计这个 Skill，只给问题和建议，先不要修改文件。”
- “把这个 Skill 发布到 GitHub，生成 npx 安装命令并验证别人能装。”

## 它到底会产出什么

根据场景复杂度，元 Skill 会创建必要而非礼仪性的文件：

```text
your-skill/
├── SKILL.md                    # Agent 路由与最小执行骨架
├── README.md                   # 给人看的产品页
├── LICENSE                     # 默认 MIT
├── manifest.json               # 版本、作者、平台与门禁
├── agents/interface.yaml       # 跨 Agent 接口
├── references/                 # 长方法、判断与安全边界
├── scripts/                    # 可重复验证与确定性工具
├── evals/trigger_cases.json    # 应触发、不应触发、近邻场景
└── reports/                    # Skill IR、研究、评测与发布证据
```

个人试验不会被迫拥有整套目录；公开、高风险或团队复用的 Skill 才会逐级增加门禁。

## 一套完整工作流

1. **Intent**：确认重复任务、目标用户、输入、输出、边界与成功标准。
2. **Search**：用 2–4 组意图关键词查询 skills.sh 与 SkillsMP，再回到 GitHub 验源。
3. **Synthesis**：记录每个候选的 `keep / adapt / reject / invent`，明确原创贡献。
4. **Package**：写精简 `SKILL.md`，把长判断放进 references，把确定性动作放进 scripts。
5. **Eval**：先测触发边界；风险需要时再补输出、运行时或人工评测。
6. **Release**：检查版本、README、许可证、秘密信息与安装入口，经功能分支和 PR 发布。
7. **Verify**：创建 Release，确认远端默认分支，并在隔离环境完成公开安装。

## 安装与验证

```bash
npx skills add joeseesun/qiaomu-meta-skill
```

只安装这个 Skill：

```bash
npx skills add joeseesun/qiaomu-meta-skill --skill qiaomu-meta-skill
```

验证：

```bash
test -f ~/.agents/skills/qiaomu-meta-skill/SKILL.md
python3 ~/.agents/skills/qiaomu-meta-skill/scripts/validate_skill.py \
  ~/.agents/skills/qiaomu-meta-skill
```

前置条件：

- [ ] Node.js 18+：`node --version`
- [ ] npx 可用：`npx --version`
- [ ] Python 3.9+：`python3 --version`
- [ ] 发布到 GitHub 时安装并登录 GitHub CLI：`gh auth status`
- [ ] 搜索或发布时允许访问 skills.sh、SkillsMP 与 GitHub

## 内置搜索

```bash
python3 scripts/research_prior_art.py \
  "<query 1>" "<query 2>" \
  --strict --summary \
  --output reports/prior-art-candidates.json
```

底层数据源：

```bash
npx --yes skills find "<query>"
python3 scripts/search_skillsmp.py "<query>" --limit 20 --sort stars
```

详细方法见 [`references/prior-art-research.md`](references/prior-art-research.md)。

## 自包含发布

只检查，不改文件、不写 GitHub：

```bash
python3 scripts/publish_skill.py /path/to/skill --dry-run
```

正式发布：

```bash
python3 scripts/publish_skill.py /path/to/skill
```

发布器会依次执行包验证、版本一致性、secret scan、功能分支、PR 检查、合并、GitHub Release、`npx skills add --list`、隔离安装和本地安全同步。

- 不直接推送 `main/master`
- 不覆盖已经发布的同版本 Release
- 不吞掉 push 或检查失败
- 不破坏性删除旧的本地 Skill
- PR 冲突、未完成/失败检查或 requested changes 会阻断自动合并

完整参数见 [`references/publishing.md`](references/publishing.md)。

## 本地质量检查

```bash
python3 scripts/validate_skill.py .
python3 scripts/export_skill_ir.py . --output reports/skill-ir.json
python3 scripts/trigger_eval.py . --cases evals/trigger_cases.json --output reports/trigger-eval.json
python3 scripts/release_check.py . --phase local --run-tests
python3 -m unittest discover -s tests -p 'test_*.py'
```

## 常见问题 / Troubleshooting

| 问题 | 常见原因 | 处理方式 |
|---|---|---|
| `No valid skills found` | `SKILL.md` frontmatter 不完整或嵌套入口错误 | 运行 `scripts/validate_skill.py`，修正 `name`、`description` 与根入口 |
| Skill 到处误触发 | description 太泛 | 补 should-not-trigger 与 near-neighbor 用例，收窄描述 |
| Skill 永远不触发 | 用户自然说法没有进入 description | 从真实对话补触发词，再跑 trigger eval |
| README 像内部说明书 | 把 `SKILL.md` 直接复制成 README | 重写成价值、安装、说法、输出、风险与排错 |
| 发布后别人装不上 | 只验证本地目录，没有公开发现和隔离安装 | 完整运行发布器，不把 push 成功当作发布完成 |
| 发布器拒绝版本 | `vX.Y.Z` 已存在 | 提升版本；已发布版本不可覆盖 |
| SkillsMP 网络中断 | 上游分块响应或限流 | 让统一研究器重试并保留 `missing evidence`，不要编造结果 |

## 设计哲学：Fork 它，而不是膜拜它

Skill 不应该是一套不可修改的“标准答案”。它更像把个人经验编译成 Agent 可以执行的源代码。

建议先安装、跑一个真实任务，然后 fork：删除不属于你的规则，加入你自己的判断、工具、风格、评测与发布边界。一个越来越像你的 Skill，才真正符合 Skill 的理念。

## 致谢与来源

- [`yaojingang/yao-meta-skill`](https://github.com/yaojingang/yao-meta-skill)：Skill IR、评测证据、Review、信任边界与 SkillOps 方法。
- [`anthropics/skills`](https://github.com/anthropics/skills)：Skill 创建、迭代与真实评测实践。
- [`openai/skills`](https://github.com/openai/skills)：渐进披露、自由度与可验证的 Skill 打包方法。
- [`joeseesun/qiaomu-skill-publisher`](https://github.com/joeseesun/qiaomu-skill-publisher)：README、Profile、License 与安装验证；其能力现已安全内建。
- skills.sh、SkillsMP 与所有在 prior-art 报告中被研究的开源作者。

上游思想以语义方式吸收并保留归因，不整库镜像，不复制许可证不明的正文，也不把搜索热度冒充质量。

Upstream inspiration: https://github.com/yaojingang/yao-meta-skill; https://github.com/joeseesun/qiaomu-skill-publisher

## 安全与证据边界

- 公开候选只读取元数据与源码，不会为了学习而执行未经审查的第三方脚本。
- API key、Cookie、Token、私有附件、绝对路径和原始对话不得进入公开仓库。
- 目录安装量、仓库 stars、安全审计和许可证分别记录，不合并为“最佳 Skill 分数”。
- 没有 provider 实跑、人工盲评或用户结果时，必须明确标记 `missing evidence`。
- 发布是外部写操作，只有明确要求时才执行，并通过功能分支、PR、Release 与公开安装验证。

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

`qiaomu-meta-skill` turns prompts, SOPs, transcripts, scripts, and existing skills into researched, evaluated, installable agent-skill packages.

Unlike a one-shot `SKILL.md` generator, it includes dual-catalog prior-art research, GitHub source verification, trigger evaluation, evidence-aware release gates, secret scanning, pull-request publication, versioned Releases, and clean `npx` installation verification.

```bash
npx skills add joeseesun/qiaomu-meta-skill
```

Try saying:

- “Turn this repeated workflow into a reusable skill.”
- “Research the strongest related skills, then synthesize an original version.”
- “Publish this skill to GitHub and prove that a clean machine can discover and install it.”

The project is intentionally fork-friendly: install it, run a real workflow, then replace Qiaomu's defaults with your own judgment, tools, style, and evaluation boundary.

## License

MIT
