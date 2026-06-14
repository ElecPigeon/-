# Parse Check

## Document

- doc_id: `002200_20250412_5b117085`
- title: `关于收到中标通知书的公告`
- pdf_path: `data/pdf/002200_002200_20250412_5b117085.pdf`
- parsed_path: `data/parsed/markdown/002200_20250412_5b117085.md`

## Page Check

- 页码是否保留：是，当前检查文档保留了 `page_no=1`、`page_no=2`、`page_no=3`
- 是否有乱码：否，证券代码、项目名称、金额表达和风险提示可读
- 表格是否完整：当前检查文档无表格，主要为段落和编号条目
- 标题层级是否合理：是，已识别出“中标情况”“中标项目情况”“风险提示”等层级
- 目录是否混入正文：否

## Target Content

- 目标章节是否出现：是，已定位到“一、中标情况”“二、中标项目情况”和“四、风险提示”
- 关键字段是否能在解析文本中找到：
  - `project_name`：可找到
  - `counterparty`：可找到
  - `project_stage`：可找到
  - `bid_amount_text`：可找到
  - `risk_notice`：可找到
- 是否需要人工修正：后续批量处理中仍需人工抽样复核 section 命中情况，尤其要检查长段落换行是否影响 evidence 提取
