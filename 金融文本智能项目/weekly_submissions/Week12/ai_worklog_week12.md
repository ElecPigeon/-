# AI Worklog Week 12

## 使用的工具

Codex

## 本周让 AI 帮助的任务

- 根据选题编写 `crawl_spec.md`
- 生成 `configs/crawl.yaml`
- 编写 `crawl_cninfo.py`、`download_pdfs.py`、`check_dataset.py`
- 规范 `metadata.csv` 字段
- 生成并更新 `dataset_check_report.md`

## 我给 AI 的上下文

- 项目题目：上市公司中标公告关键信息抽取与项目台账生成
- 数据源要求：巨潮资讯网公开公告
- 目标难度：标准档 `1.0`
- Week 12 交付物清单

## AI 生成或修改的文件

- `crawl_spec.md`
- `difficulty_declaration.md`
- `configs/crawl.yaml`
- `src/crawl_cninfo.py`
- `src/download_pdfs.py`
- `src/check_dataset.py`
- `data/metadata/metadata.csv`
- `outputs/reports/dataset_check_report.md`

## 我实际运行的命令

```bash
python src/crawl_cninfo.py --config configs/crawl.yaml --limit 5
python src/crawl_cninfo.py --config configs/crawl.yaml --limit 20
python src/crawl_cninfo.py --config configs/crawl.yaml --limit 80
python src/download_pdfs.py --metadata data/metadata/metadata.csv --limit 80
python src/check_dataset.py --metadata data/metadata/metadata.csv
```

## 报错与修复

| 问题 | 报错信息 | 修复方式 |
|---|---|---|
| 初版抓取脚本只会写入预设样例 | 运行后 `metadata.csv` 只有固定 3 条记录 | 改为调用巨潮公开搜索接口 `fulltextSearch/full`，按关键词分页抓取真实公告 |
| 关键词过宽，容易混入无关公告 | 搜索“中标”时结果里混入非目标公告 | 将抓取关键词改为更具体的标题短语，并增加 `title_include_keywords` 过滤 |
| 重新下载后状态口径不一致 | 已存在文件被记为 `skipped`，影响报告统计 | 在数据检查脚本中按“本地 PDF 是否存在”统计成功下载数，而不是只看状态字段 |

## 我人工检查了什么

- 标题是否确实属于中标相关公告
- 日期与 PDF 链接是否匹配
- `local_pdf_path` 是否可追溯
- `download_status` 和失败记录是否一致
- 随机抽查下载后的 PDF 是否能正常打开
- 检查 `metadata.csv`、`data/pdf/` 和 `dataset_check_report.md` 的记录数是否一致

## 我理解的关键代码

- `crawl_cninfo.py` 负责生成 `metadata.csv`
- `download_pdfs.py` 负责根据 `pdf_url` 下载并更新下载状态
- `check_dataset.py` 负责检查缺失 PDF、重复记录和关键词相关性

## 本周结果

- 已抓取 80 条真实中标相关公告 metadata
- 已下载 80 份对应 PDF
- `dataset_check_report.md` 已更新为真实统计结果
