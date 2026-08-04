# Review And Release Gates

乔木 skill 发布前不靠“看起来差不多”，而靠一组轻重分层的门禁。

## Gate 语义

- `pass`：证据存在且满足要求。
- `warn`：可以继续，但风险必须显式展示。
- `block`：不能声称生产、公开、治理或团队可复用已经就绪。

## 分层门禁

### Scaffold

- `SKILL.md` frontmatter 有 `name` 和准确 `description`。
- README 有一句话价值、安装方式、自然语言触发例子。
- 明确什么不做。

### Production

- `agents/interface.yaml` 与 `SKILL.md` 对齐。
- `evals/trigger_cases.json` 覆盖 should-trigger、should-not-trigger、near-neighbor。
- README 有验证命令、输出示例、Troubleshooting、风险边界。
- 根目录之外不存在精确命名的 `SKILL.md`；内嵌示例和夹具分别使用 `SKILL.example.md`、`SKILL.fixture.md`。
- 可运行：

```bash
python3 scripts/validate_skill.py .
python3 scripts/trigger_eval.py . --cases evals/trigger_cases.json
```

### Library

- 导出 `reports/skill-ir.json`。
- 说明 target platforms、degradation、trust、permissions。
- 做 install 验证或说明为什么暂时不能验证。
- 有 review cadence 和 owner。

### Governed

- 涉及账号、密钥、网络、文件写入、发布、付费服务、公开承诺时使用。
- 必须有 rollback boundary、trust boundary、secret scan、公开 claim guard。
- output eval 或人工 review 缺失时标记 `missing evidence`；盲评只有在答案隔离、判断先于揭晓、reviewer/decision/reason 齐全时才算完成证据。
- 不把计划、草稿、未审 telemetry 当证据。

## 可执行发布检查

```bash
# 本地：允许工作树尚未提交，但要求包、版本、报告、secret 和测试通过
python3 scripts/release_check.py . --phase local --run-tests

# PR：额外要求干净工作树、远端分支和开放 PR
python3 scripts/release_check.py . --phase pr --run-tests

# 已发布：额外核对默认分支版本、GitHub Release 和隔离 HOME 的干净安装
python3 scripts/release_check.py . --phase published --run-tests --install-check
```

完整发布由同包脚本执行，不再依赖独立 publisher skill：

```bash
# 只读审计
python3 scripts/publish_skill.py /path/to/skill --dry-run

# 用户明确要求发布后：准备 → 功能分支 → PR → 合并 → Release → 安装验证
python3 scripts/publish_skill.py /path/to/skill
```

发布器必须阻断直推默认分支、同版本重发、secret、冲突、失败/未完成检查和 requested changes。详细行为见 [Self-Contained Skill Publishing](publishing.md)。

`local` 阶段的 dirty worktree 是警告，因为正在开发；到了 `pr` 和 `published` 阶段则是阻断。缺失 provider/human output evidence 或尚未运行 install check 必须保留为警告或 `missing evidence`，不能伪装成已验证。

只有 `reports/output-evidence.json` 明确记录通过的 `provider_backed` 或 `human_blind_review` 证据，发布检查才把输出证据记为 `pass`。行为规格、静态 fixture 或仅存在一个 scorecard 文件仍然是警告，不能靠文件名冒充验证。

## 公开发布提醒

Qiaomu-owned 公开 skill 的正常完成线是：

1. feature branch
2. 验证
3. PR
4. merge 到 `main`
5. 安装或发现能力验证

不要直接推 default branch；也不要把验证过的 PR 长期悬着。
