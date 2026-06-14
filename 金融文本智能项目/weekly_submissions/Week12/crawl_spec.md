# Crawl Spec

## 项目名称

cninfo_bidding_announcements_tracker

## 数据来源

巨潮资讯网公开公告。

## 抓取范围

- 股票池或行业：A 股上市公司，不限定单一行业，优先保留工程建设、电力设备、信息技术和制造业公司样本
- 时间范围：2024-01-01 至 2026-05-28
- 市场：`sz`、`sh`
- 公告类型：中标相关公告
- 关键词：
  - `中标`
  - `中标通知书`
  - `重大经营合同中标`
  - `关于中标项目的公告`

## 数据量目标

Week 12 先完成 5-10 条小样本测试，确认标题、日期、PDF 链接和下载路径无误；正式项目目标为 80-120 份 PDF，满足标准档 `1.0` 的基础数据规模要求。

## metadata 字段

最低保存以下字段：

- `doc_id`
- `stock_code`
- `stock_name`
- `market`
- `announcement_title`
- `announcement_type`
- `publish_date`
- `url`
- `pdf_url`
- `local_pdf_path`
- `download_status`
- `source`
- `crawl_time`
- `error_message`
- `notes`

## PDF 保存规则

- PDF 文件统一保存到 `data/pdf/`
- 文件名格式：`{stock_code}_{doc_id}.pdf`
- `local_pdf_path` 必须能唯一定位本地 PDF 文件
- 若本地文件已存在，则跳过下载并将 `download_status` 记录为 `skipped`

## 限速与失败处理

- 请求之间至少休眠 `1.5` 秒
- 下载失败写入 `outputs/logs/failed_downloads.csv`
- 抓取日志写入 `outputs/logs/crawl_log.jsonl`
- `error_message` 不允许静默为空，失败时需记录异常原因

## 是否需要多公告匹配

不需要。本项目以单份中标相关公告为基本记录粒度。

## 合规说明

- 不绕过登录、验证码或访问限制
- 保留日志
- 只抓取公开可访问数据
