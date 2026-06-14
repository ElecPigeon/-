# Workflow Design

## 项目目标

将巨潮资讯网中标相关公告从 `metadata.csv` 一路处理为带 evidence 的结构化结果表，并保留每个关键步骤的日志和质量检查结果。

## 节点表

| 节点 | 输入 | 输出 | 成功标准 | 失败处理 | 日志 |
|---|---|---|---|---|---|
| collect | 巨潮公告查询接口 / 抓取配置 | `metadata.csv` | 记录字段完整，可追溯到公告 | 写入 `error_message` 和抓取日志 | `crawl_log.jsonl` |
| audit | `metadata.csv` + `data/pdf/` | `dataset_check_report.md` | 能统计缺失 PDF、重复记录和关键词匹配情况 | 标记缺失样本并补抓 | `run_log.jsonl` |
| parse | PDF 或 MinerU markdown | `parsed_docs.jsonl` | 每条记录包含 `doc_id`、`title`、`pages` | 记录失败文档，进入人工复核 | `run_log.jsonl` |
| route | `parsed_docs.jsonl` + `section_rules.yaml` | `sections.jsonl` / `section_check_report.md` | 能定位项目情况和风险提示 | 调整 include/exclude 规则 | `run_log.jsonl` |
| extract | 路由出的目标章节 + prompt/schema | `extract_results.jsonl` | 字段符合项目定义，关键字段有 evidence | 保留原始输出并人工检查 | `run_log.jsonl` |
| validate | `extract_results.jsonl` + Pydantic schema | `records_validated.csv` | 校验通过或明确报错 | 将失败记录写入错误日志 | `run_log.jsonl` |
| report | 验证结果 + 错误记录 | `summary_report.md` | 可以说明样本量、有效记录和主要问题 | 回到上游节点继续修复 | `run_log.jsonl` |

## 流程图

Collect -> Audit -> Parse -> Route -> Extract -> Validate -> Report

## 人工检查点

- 人工检查 5-10 条 metadata 标题和 PDF 链接
- 人工检查 section 是否命中正文而非目录或备查文件
- 人工检查 evidence_text 是否真的来自输入
- 人工检查 null 字段是否合理，而不是模型漏抽

## 最小运行命令

```bash
python pipeline_run.py --config configs/workflow.yaml --step all --limit 3
```
