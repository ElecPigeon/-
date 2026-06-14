# AI Worklog Week 13

## 使用的工具

Codex

## 本周让 AI 帮助的任务

- 为中标公告设计 Pydantic Schema
- 生成 `section_rules.yaml`
- 编写 `parse_docs.py` 与 `route_sections.py`
- 准备 `parse_check.md` 和 `section_check_report.md`
- 生成带 evidence 的 `extract_results_v1.jsonl`

## 我给 AI 的上下文

- Week 12 的 `metadata.csv`
- 项目题目：上市公司中标公告关键信息抽取与项目台账生成
- 目标字段：项目名称、招标人、中标阶段、金额原文、风险提示等
- 课程要求：MinerU、section checking、Pydantic、null rule、evidence

## AI 生成或修改的文件

- `.env.example`
- `configs/model_config.yaml`
- `src/schemas.py`
- `src/parse_docs.py`
- `src/route_sections.py`
- `parse_check.md`
- `section_rules.yaml`
- `section_check_report.md`
- `extract_results_v1.jsonl`
- `validation_errors.jsonl`

## 我实际运行的命令

```bash
python src/parse_docs.py --metadata ../Week12/data/metadata/metadata.csv --limit 1
python src/route_sections.py --parsed data/parsed/parsed_docs.jsonl --rules section_rules.yaml
```

## 报错与修复

| 问题 | 报错信息 | 修复方式 |
|---|---|---|
| 初版演示文本与真实 PDF 不一致 | 项目名称、招标人和风险提示不能回到原始 PDF 原文 | 用真实 PDF 文本重新整理 markdown，并同步更新 `parsed_docs.jsonl`、`section_check_report.md` 和 `extract_results_v1.jsonl` |
| 中标金额字段最初被写成 `null` | 真实公告中存在“通行费下浮率为0%，补偿金首次支付比例为80%” | 将 `bid_amount_text` 改为保留原文表达，不强行标准化为货币金额 |

## 我人工检查了什么

- MinerU 解析文本是否保留标题和段落
- section 是否命中项目情况和风险提示段落
- evidence_text 是否真的出现在输入文本中
- null 字段是否有合理依据
- `page_no` 是否与整理后的解析页面一致

## 我理解的关键代码

- `schemas.py` 定义了字段契约和 evidence 结构
- `parse_docs.py` 负责将解析文本整理为统一的 `parsed_docs.jsonl`
- `route_sections.py` 用 section 规则找出候选章节并生成检查结果

## 本周结果

- 已完成 1 条与真实 PDF 对齐的解析、section、evidence 和 schema 校验展示链
- `project_name`、`counterparty`、`project_stage`、`bid_amount_text`、`risk_notice` 均能回到原文
- 当前提交版主要用于展示和答辩，后续若有真实 MinerU / LLM Key，可继续扩充为批量解析版本
