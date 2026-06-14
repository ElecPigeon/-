# Demo Script

## 1. 项目介绍

我们的项目题目是“上市公司中标公告关键信息抽取与项目台账生成”。目标是从巨潮中标相关公告中抽取项目名称、招标人、中标阶段、金额原文和风险提示，形成可以追溯到原公告的结构化结果。

## 2. 数据来源

数据全部来自巨潮资讯网公开公告。我们用“中标”“中标通知书”“重大经营合同中标”等关键词筛选样本，并在 `metadata.csv` 中记录标题、日期、URL、PDF 路径和下载状态。

## 3. 证据链展示

按下面顺序展示 1 条样例：

1. 打开原始 PDF 对应的 `metadata.csv` 记录
2. 展示原始 PDF：`data/pdf/002200_002200_20250412_5b117085.pdf`
3. 展示解析后的 `parsed_docs_sample.jsonl`
3. 展示 section 命中“中标情况”和“风险提示”
4. 展示 `final_results.jsonl` 中的结构化结果
5. 解释 `project_name` 和 `risk_notice` 的 evidence_text
6. 展示 `eval_report_final.md` 中的评估结论

## 4. 方法总结

整体 workflow 为：

`metadata -> audit -> parse -> route -> extract -> validate -> report`

## 5. 局限与优化

- 有些公告不披露明确金额，因此保留 `bid_amount_text` 原文并允许为 `null`
- 后续会继续优化标题筛选规则和 section 路由规则
