from __future__ import annotations

import argparse
import csv
from collections import Counter
from pathlib import Path


KEYWORDS = [
    "中标通知书",
    "中标项目",
    "重大经营合同中标",
    "项目中标",
]


def read_metadata(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def main() -> None:
    parser = argparse.ArgumentParser(description="Check CNINFO dataset quality.")
    parser.add_argument("--metadata", required=True, help="Path to metadata.csv")
    args = parser.parse_args()

    metadata_path = Path(args.metadata)
    base_dir = metadata_path.parent.parent.parent
    report_path = base_dir / "outputs/reports/dataset_check_report.md"
    rows = read_metadata(metadata_path)

    total_records = len(rows)
    success_downloads = 0
    failed_downloads = sum(1 for row in rows if row["download_status"] == "failed")
    missing_pdfs = 0
    irrelevant_records: list[dict] = []
    for row in rows:
        pdf_path = base_dir / row["local_pdf_path"]
        if pdf_path.exists():
            success_downloads += 1
        else:
            missing_pdfs += 1
        title = row["announcement_title"]
        if not any(keyword in title for keyword in KEYWORDS):
            irrelevant_records.append(row)

    duplicate_doc_ids = sum(count - 1 for count in Counter(row["doc_id"] for row in rows).values() if count > 1)

    report_path.parent.mkdir(parents=True, exist_ok=True)
    with report_path.open("w", encoding="utf-8") as fh:
        fh.write("# Dataset Check Report\n\n")
        fh.write("## Summary\n")
        fh.write(f"- Total records: {total_records}\n")
        fh.write(f"- Downloaded PDFs: {success_downloads}\n")
        fh.write(f"- Failed downloads: {failed_downloads}\n")
        fh.write(f"- Duplicate doc_id: {duplicate_doc_ids}\n")
        fh.write(f"- Potentially irrelevant records: {len(irrelevant_records)}\n\n")
        fh.write("## Keyword Match\n")
        fh.write(f"- Keywords: {', '.join(KEYWORDS)}\n\n")
        fh.write("## Missing Files\n")
        fh.write(f"- Missing local PDF count: {missing_pdfs}\n\n")
        fh.write("## Duplicate Records\n")
        fh.write(f"- Duplicate doc_id count: {duplicate_doc_ids}\n\n")
        fh.write("## Sample Inspection\n")
        fh.write("| doc_id | title | pdf_ok | relevant | notes |\n")
        fh.write("|---|---|---|---|---|\n")
        for row in rows[:5]:
            pdf_ok = "yes" if (base_dir / row["local_pdf_path"]).exists() else "no"
            relevant = "yes" if any(keyword in row["announcement_title"] for keyword in KEYWORDS) else "no"
            fh.write(
                f"| {row['doc_id']} | {row['announcement_title']} | {pdf_ok} | {relevant} | {row['notes']} |\n"
            )
        fh.write("\n## Risks\n")
        if total_records >= 80:
            fh.write("- 当前数据量已达到标准档下限，但后续仍建议继续扩充到 80-120 份 PDF 的更稳定区间。\n")
        else:
            fh.write("- 当前数据量仍偏小，后续需要继续扩大到 80-120 份 PDF。\n")
        fh.write("- 部分公告可能包含“中标”关键词但不属于最终目标类型，需人工抽样确认。\n")
        fh.write("- 若 PDF 下载失败，必须回写 metadata 并保留失败日志。\n")

    print(f"report written to {report_path}")


if __name__ == "__main__":
    main()
