# Trigger And Eval Playbook

## 先看触发

- 用户会不会自然说出这句话
- 改进已有技能时，从该用户最近的真实请求里抽动词和名词补进 should_trigger 与概念词表（例：正式词「发布」之外还有口语「发版」「上架」）；只写正式术语会漏掉最常见的说法
- description 是否包含关键术语
- 是否会误触到别的 skill
- should-trigger、should-not-trigger、near-neighbor 是否都有样例

## 再看输出

- 是否符合预期格式
- 是否漏掉边界
- 是否适合发布给别人用
- 是否能证明比不用 skill 更稳，而不是只把规则写长

## 最后看维护

- 新需求是否能插进来
- 资源是否容易找
- 以后是否能继续迭代

## 最小命令

```bash
python3 scripts/trigger_eval.py . --cases evals/trigger_cases.json --output reports/trigger-eval.json
```

如果是 Production、Library 或 Governed，并且结果质量重要，再按 [Output Eval Method](output-eval-method.md) 增加 output eval。
