# 上市公司中标公告关键信息抽取与项目台账生成

## 项目目标

本项目从巨潮资讯网公开披露的中标相关公告 PDF 中抽取结构化金融事件信息，形成可追溯、可比较的项目台账。核心目标是识别项目名称、招标人、中标阶段、金额原文和风险提示，并为关键字段保留 evidence。

## 数据来源

- 数据源：巨潮资讯网公开公告
- 公告类型：
  - 关于中标项目的公告
  - 关于收到中标通知书的公告
  - 关于重大经营合同中标的公告
- 时间范围：2024-01-01 至 2026-05-28
- 目标规模：80-120 份 PDF

## 目录结构

```text
final_repo/
  README.md
  requirements.txt
  .env.example
  AGENTS.md
  configs/
  data/
  prompts/
  src/
  outputs/
  tests/
  pipeline_run.py
  demo_script.md
  ai_usage_statement.md
  ai_worklog_all.md
  optimization_log.md
  final_slides_outline.md
```

## 环境安装

```bash
python -m pip install -r requirements.txt
```

## .env 说明

复制 `.env.example` 为 `.env`，再填入真实 MinerU 和 LLM API Key。真实 `.env` 不得提交。

## 最小运行命令

```bash
python pipeline_run.py --step all --limit 3
```

## 输出文件说明

- `data/metadata/metadata.csv`：公告主元数据表
- `data/metadata/metadata_week12_batch.csv`：Week 12 批量抓取的 80 条真实 metadata
- `data/pdf/`：用于 demo 的原始 PDF 样本
- `data/parsed/parsed_docs_sample.jsonl`：与真实 PDF 对齐的展示用解析文档
- `outputs/results/final_results.jsonl`：最终结构化抽取结果
- `outputs/results/records_validated.csv`：Pydantic 校验结果
- `outputs/reports/eval_report_final.md`：人工评估与错误分类摘要
- `outputs/reports/section_check_report.md`：section 检查记录
- `outputs/reports/dataset_check_report_week12.md`：Week 12 批量数据检查报告
- `outputs/logs/sample_run_log.jsonl`：运行日志

## 评估结果摘要

- 当前提交版包含 1 条完整证据链展示结果
- `project_name`、`counterparty`、`project_stage` 和 `risk_notice` 能给出原文 evidence
- `bid_amount_text` 已保留原文“通行费下浮率为0%，补偿金首次支付比例为80%”

## 主要局限

- 当前仓库中的解析、section 和抽取结果以展示链路为主，尚未扩展为批量 MinerU/LLM 结果
- 批量解析依赖 MinerU API 稳定性
- 标题筛选和金额标准化仍需扩大样本后继续优化
