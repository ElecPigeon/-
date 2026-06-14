# Evaluation Report

## 评估样本

- 当前示范样本：1 条完整证据链
- 正式项目计划人工评估：15-25 份 PDF

## Data Quality

- metadata 字段完整
- PDF 路径可追溯
- 当前展示记录不存在重复 doc_id

## Section Quality

- `project_details` 命中率：当前展示记录为 1/1
- `risk_notice` 命中率：当前展示记录为 1/1

## Extraction Quality

- `project_name`：正确
- `counterparty`：正确
- `project_stage`：正确
- `bid_amount_text`：已按原文保留“通行费下浮率为0%，补偿金首次支付比例为80%”
- `risk_notice`：正确

## Evidence Quality

- evidence_text 来自输入文本原文
- page_no 已回填为 1

## Pipeline Stability

- 展示链路流程可跑通
- 批量稳定性仍需在更大样本上验证

## 错误分类

| 错误类型 | 数量 | 示例 | 修复策略 |
|---|---:|---|---|
| schema_error | 1 | 阶段字段写成“收到通知” | 改为枚举值约束 |
| section_error | 0 | 暂无 | 扩样后继续抽查 |
| hallucination | 0 | 暂无 | 强制 evidence 来自输入 |

## 优化前后对比

- 优化前：阶段字段表述不统一
- 优化后：统一为枚举值，并通过 Pydantic 校验

## 局限性

- 当前只展示单条完整证据链，不代表最终大样本准确率
- 金额标准化尚未完成，现阶段保留原文表达
