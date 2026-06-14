from __future__ import annotations

import argparse
import csv
import time
from pathlib import Path
from urllib.parse import urlparse

import requests


def is_allowed_cninfo_url(url: str) -> bool:
    hostname = urlparse(url).hostname or ""
    return hostname.endswith("cninfo.com.cn")


def read_metadata(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def write_metadata(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def append_failed(path: Path, row: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    exists = path.exists()
    with path.open("a", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=["doc_id", "pdf_url", "error_message"])
        if not exists:
            writer.writeheader()
        writer.writerow(row)


def main() -> None:
    parser = argparse.ArgumentParser(description="Download CNINFO PDFs from metadata.")
    parser.add_argument("--metadata", required=True, help="Path to metadata.csv")
    parser.add_argument("--limit", type=int, default=None, help="Optional row limit for testing.")
    parser.add_argument("--sleep-seconds", type=float, default=1.5, help="Rate limit between downloads.")
    args = parser.parse_args()

    metadata_path = Path(args.metadata)
    base_dir = metadata_path.parent.parent.parent
    failed_log = base_dir / "outputs/logs/failed_downloads.csv"
    rows = read_metadata(metadata_path)
    if args.limit is not None:
        rows = rows[: args.limit]

    session = requests.Session()
    fieldnames = list(rows[0].keys()) if rows else []

    for row in rows:
        pdf_url = row["pdf_url"]
        if not is_allowed_cninfo_url(pdf_url):
            row["download_status"] = "failed"
            row["error_message"] = "pdf_url is not a cninfo domain"
            append_failed(failed_log, {"doc_id": row["doc_id"], "pdf_url": pdf_url, "error_message": row["error_message"]})
            continue

        output_path = base_dir / row["local_pdf_path"]
        output_path.parent.mkdir(parents=True, exist_ok=True)

        if output_path.exists():
            row["download_status"] = "skipped"
            row["error_message"] = ""
            continue

        try:
            response = session.get(pdf_url, timeout=30)
            response.raise_for_status()
            output_path.write_bytes(response.content)
            row["download_status"] = "success"
            row["error_message"] = ""
        except Exception as exc:  # noqa: BLE001
            row["download_status"] = "failed"
            row["error_message"] = str(exc)
            append_failed(failed_log, {"doc_id": row["doc_id"], "pdf_url": pdf_url, "error_message": row["error_message"]})
        time.sleep(args.sleep_seconds)

    all_rows = read_metadata(metadata_path)
    update_map = {row["doc_id"]: row for row in rows}
    merged_rows = [update_map.get(row["doc_id"], row) for row in all_rows]
    write_metadata(metadata_path, merged_rows, fieldnames or list(merged_rows[0].keys()))
    print(f"updated metadata: {metadata_path}")


if __name__ == "__main__":
    main()
