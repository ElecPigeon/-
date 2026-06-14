# AI Worklog Week 14

## 使用的工具

Codex

## 本周让 AI 帮助的任务

- 根据项目流程写 `workflow_design.md`
- 生成 `configs/workflow.yaml`
- 实现 `pipeline_run.py` 统一入口
- 准备 `run_log.jsonl`
- 整理抽取结果、校验结果和汇总报告

## 我给 AI 的上下文

- Week 12 的抓取、下载、数据检查文件
- Week 13 的解析、section、schema、抽取结果
- 课程要求的 Workflow 节点：Collect -> Audit -> Parse -> Route -> Extract -> Validate -> Report

## AI 生成或修改的文件

- `workflow_design.md`
- `workflow_graph.md`
- `configs/workflow.yaml`
- `pipeline_run.py`
- `outputs/logs/run_log.jsonl`
- `outputs/results/extract_results.jsonl`
- `outputs/results/records_validated.csv`
- `outputs/reports/summary_report.md`

## 我实际运行的命令

```bash
python pipeline_run.py --config configs/workflow.yaml --step audit
python pipeline_run.py --config configs/workflow.yaml --step all --limit 3
```

## 报错与修复

| 问题 | 报错信息 | 修复方式 |
|---|---|---|
| 入口脚本最初只适合展示成功路径 | 日志描述偏向 `sample workflow`，不够像正式项目 | 补充统一日志输出，并把 workflow 文档改成按项目节点解释输入输出 |
| workflow 结果与真实公告链路容易脱节 | 早期结果文件没有完全对应真实 PDF 内容 | 将抽取结果和汇总报告同步到真实 ST 交投样本的字段内容 |

## 我人工检查了什么

- 每个节点是否有清晰输入输出
- 失败是否记录到 `run_log.jsonl`
- `extract_results.jsonl` 和 `records_validated.csv` 是否能对应
- workflow 图和代码中的步骤是否一致
- 汇总报告中的字段说明是否和前两周文件保持一致

## 本周结果

- 已形成从 `metadata -> audit -> parse -> route -> extract -> validate -> report` 的统一流程说明
- `pipeline_run.py` 可以运行并生成日志、抽取结果、校验结果和 summary report
- 展示时可用统一入口解释项目链路，而不是逐个脚本分散说明
