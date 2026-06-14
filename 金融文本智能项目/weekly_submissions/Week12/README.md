# Week 12 Deliverables

本文件夹对应 Week 12 课后提交材料，主题为“上市公司中标公告关键信息抽取与项目台账生成”。

建议运行顺序：

```bash
python src/crawl_cninfo.py --config configs/crawl.yaml --limit 3
python src/download_pdfs.py --metadata data/metadata/metadata.csv --limit 3
python src/check_dataset.py --metadata data/metadata/metadata.csv
```

当前已预置：

- 抓取规格 `crawl_spec.md`
- 难度声明 `difficulty_declaration.md`
- 抓取配置 `configs/crawl.yaml`
- 抓取、下载、检查脚本 `src/`
- `metadata.csv`
- 数据检查报告 `outputs/reports/dataset_check_report.md`
- AI 工作记录 `ai_worklog_week12.md`

当前状态：

- 已抓取 80 条真实中标相关公告 metadata
- 已下载 80 份对应 PDF
- `dataset_check_report.md` 已更新为真实统计结果
