# Dataset Check Report

## Summary
- Total records: 80
- Downloaded PDFs: 80
- Failed downloads: 0
- Duplicate doc_id: 0
- Potentially irrelevant records: 0

## Keyword Match
- Keywords: 中标通知书, 中标项目, 重大经营合同中标, 项目中标

## Missing Files
- Missing local PDF count: 0

## Duplicate Records
- Duplicate doc_id count: 0

## Sample Inspection
| doc_id | title | pdf_ok | relevant | notes |
|---|---|---|---|---|
| 002973_20260529_7eef2917 | 侨银股份：关于近期收到两份中标通知书的公告 | yes | yes | keyword=关于收到中标通知书的公告;announcement_id=1225335051 |
| 002152_20260529_38be93dc | 广电运通：关于收到中标通知书的公告 | yes | yes | keyword=关于收到中标通知书的公告;announcement_id=1225334783 |
| 301235_20260528_7f622120 | 华康洁净：关于项目中标及收到成交通知书的公告 | yes | yes | keyword=关于收到中标通知书的公告;announcement_id=1225334693 |
| 300540_20260528_eafe39f1 | 蜀道装备：关于收到中标通知书的公告 | yes | yes | keyword=关于收到中标通知书的公告;announcement_id=1225333534 |
| 301310_20260527_ce54426e | 鑫宏业：关于全资子公司收到中标通知书的公告 | yes | yes | keyword=关于收到中标通知书的公告;announcement_id=1225332564 |

## Risks
- 当前数据量已达到标准档下限，但后续仍建议继续扩充到 80-120 份 PDF 的更稳定区间。
- 部分公告可能包含“中标”关键词但不属于最终目标类型，需人工抽样确认。
- 若 PDF 下载失败，必须回写 metadata 并保留失败日志。
