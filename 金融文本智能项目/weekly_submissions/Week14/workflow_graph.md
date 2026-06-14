# Workflow Graph

```text
metadata.csv
  -> audit dataset
  -> parse docs
  -> route sections
  -> extract fields
  -> validate results
  -> summary report
```

## 节点说明

- `audit`: 检查 metadata、重复记录、PDF 缺失和关键词相关性
- `parse`: 把 PDF/MinerU 输出整理成统一的 `parsed_docs.jsonl`
- `route sections`: 找出“中标情况”和“风险提示”候选段落
- `extract`: 按 schema 输出字段和 evidence
- `validate`: 用 Pydantic 校验字段类型和枚举值
- `summary report`: 汇总成功率、错误类型和后续修复重点
