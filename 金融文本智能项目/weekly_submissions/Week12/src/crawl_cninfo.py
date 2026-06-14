from __future__ import annotations

import argparse
import csv
import hashlib
import html
import json
import re
import time
from datetime import datetime
from pathlib import Path

import requests
import yaml


FIELDNAMES = [
    "doc_id",
    "stock_code",
    "stock_name",
    "market",
    "announcement_title",
    "announcement_type",
    "publish_date",
    "url",
    "pdf_url",
    "local_pdf_path",
    "download_status",
    "source",
    "crawl_time",
    "error_message",
    "notes",
]

SEARCH_ENDPOINT = "https://www.cninfo.com.cn/new/fulltextSearch/full"


def build_doc_id(stock_code: str, publish_date: str, title: str) -> str:
    title_hash = hashlib.md5(title.encode("utf-8")).hexdigest()[:8]
    date_part = publish_date.replace("-", "")
    return f"{stock_code}_{date_part}_{title_hash}"


def load_config(config_path: Path) -> dict:
    with config_path.open("r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def write_jsonl(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(payload, ensure_ascii=False) + "\n")


def clean_text(value: str | None) -> str:
    if not value:
        return ""
    value = re.sub(r"</?em>", "", value)
    value = html.unescape(value)
    return " ".join(value.split())


def infer_market(stock_code: str) -> str:
    if stock_code.startswith(("600", "601", "603", "605", "688", "900")):
        return "sh"
    return "sz"


def infer_announcement_type(title: str) -> str:
    if "重大经营合同中标" in title:
        return "重大经营合同中标公告"
    if "中标项目" in title:
        return "中标项目公告"
    if "中标通知书" in title:
        return "中标通知书公告"
    return "中标相关公告"


def build_detail_url(announcement_id: str, org_id: str, announcement_time: int) -> str:
    return (
        "https://www.cninfo.com.cn/new/disclosure/detail?"
        f"announcementId={announcement_id}&orgId={org_id}&announcementTime={announcement_time}"
    )


def should_keep_title(title: str, title_include_keywords: list[str]) -> bool:
    return any(keyword in title for keyword in title_include_keywords)


def fetch_announcements(session: requests.Session, config: dict, limit: int | None) -> list[dict]:
    keywords = config.get("keywords", [])
    start_date = config["date_range"]["start"]
    end_date = config["date_range"]["end"]
    page_size = int(config.get("page_size", 30))
    max_pages_per_keyword = int(config.get("max_pages_per_keyword", 5))
    is_fulltext = bool(config.get("is_fulltext", False))
    title_include_keywords = config.get("title_include_keywords", keywords)
    sleep_seconds = float(config.get("sleep_seconds", 1.5))
    max_records = limit or int(config.get("max_records", 100))

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Referer": "https://www.cninfo.com.cn/new/fulltextSearch",
    }

    seen_announcement_ids: set[str] = set()
    rows: list[dict] = []

    for page_num in range(1, max_pages_per_keyword + 1):
        for keyword in keywords:
            params = {
                "searchkey": keyword,
                "sdate": start_date,
                "edate": end_date,
                "isfulltext": str(is_fulltext).lower(),
                "sortName": "nothing",
                "sortType": "desc",
                "pageNum": page_num,
                "pageSize": page_size,
                "type": "",
            }
            response = session.get(SEARCH_ENDPOINT, params=params, headers=headers, timeout=30)
            response.raise_for_status()
            payload = response.json()
            announcements = payload.get("announcements", [])

            if not announcements:
                continue

            for item in announcements:
                announcement_id = str(item.get("announcementId") or "")
                stock_code = str(item.get("secCode") or "")
                if not announcement_id or announcement_id in seen_announcement_ids:
                    continue
                if len(stock_code) != 6 or not stock_code.isdigit():
                    continue

                title = clean_text(item.get("announcementTitle"))
                if not should_keep_title(title, title_include_keywords):
                    continue

                publish_date = datetime.fromtimestamp(item["announcementTime"] / 1000).strftime("%Y-%m-%d")
                doc_id = build_doc_id(stock_code, publish_date, title)
                pdf_url = f"https://static.cninfo.com.cn/{item['adjunctUrl']}"
                market = infer_market(stock_code)
                org_id = str(item.get("orgId") or "")
                detail_url = build_detail_url(announcement_id, org_id, int(item["announcementTime"]))
                local_pdf_path = f"data/pdf/{stock_code}_{doc_id}.pdf"

                rows.append(
                    {
                        "doc_id": doc_id,
                        "stock_code": stock_code,
                        "stock_name": clean_text(item.get("secName")),
                        "market": market,
                        "announcement_title": title,
                        "announcement_type": infer_announcement_type(title),
                        "publish_date": publish_date,
                        "url": detail_url,
                        "pdf_url": pdf_url,
                        "local_pdf_path": local_pdf_path,
                        "download_status": "pending",
                        "source": config["source"],
                        "crawl_time": datetime.now().isoformat(timespec="seconds"),
                        "error_message": "",
                        "notes": f"keyword={keyword};announcement_id={announcement_id}",
                    }
                )
                seen_announcement_ids.add(announcement_id)
                if len(rows) >= max_records:
                    return rows

            time.sleep(sleep_seconds)

    return rows


def refresh_download_status(base_dir: Path, rows: list[dict]) -> None:
    for row in rows:
        pdf_path = base_dir / row["local_pdf_path"]
        if pdf_path.exists():
            row["download_status"] = "success"


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate metadata.csv for CNINFO bidding announcements.")
    parser.add_argument("--config", required=True, help="Path to crawl yaml config.")
    parser.add_argument("--limit", type=int, default=None, help="Optional row limit for testing.")
    args = parser.parse_args()

    config_path = Path(args.config)
    config = load_config(config_path)

    base_dir = config_path.parent.parent
    output_metadata = base_dir / config["output"]["metadata"]
    crawl_log = base_dir / config["output"]["crawl_log"]
    output_metadata.parent.mkdir(parents=True, exist_ok=True)

    session = requests.Session()
    rows: list[dict] = []
    try:
        rows = fetch_announcements(session, config, args.limit)
        refresh_download_status(base_dir, rows)
        write_jsonl(
            crawl_log,
            {
                "time": datetime.now().isoformat(timespec="seconds"),
                "step": "crawl",
                "status": "success",
                "records": len(rows),
                "error": None,
            },
        )
    except Exception as exc:  # noqa: BLE001
        write_jsonl(
            crawl_log,
            {
                "time": datetime.now().isoformat(timespec="seconds"),
                "step": "crawl",
                "status": "failed",
                "records": len(rows),
                "error": str(exc),
            },
        )
        raise

    with output_metadata.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)

    print(f"metadata written to {output_metadata}")
    print(f"records={len(rows)}")


if __name__ == "__main__":
    main()
