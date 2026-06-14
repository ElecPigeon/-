from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


def read_metadata(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def load_markdown(markdown_path: Path) -> str:
    return markdown_path.read_text(encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Standardize parsed markdown into parsed_docs.jsonl.")
    parser.add_argument("--metadata", required=True, help="Path to metadata.csv")
    parser.add_argument("--limit", type=int, default=1, help="How many rows to standardize for the current run.")
    args = parser.parse_args()

    metadata_path = Path(args.metadata)
    week13_dir = Path(__file__).resolve().parents[1]
    parsed_docs_path = week13_dir / "data/parsed/parsed_docs.jsonl"

    rows = read_metadata(metadata_path)[: args.limit]
    records: list[dict] = []
    for row in rows:
        markdown_path = week13_dir / f"data/parsed/markdown/{row['doc_id']}.md"
        if not markdown_path.exists():
            raise FileNotFoundError(f"missing markdown file: {markdown_path}")
        text = load_markdown(markdown_path)
        records.append(
            {
                "doc_id": row["doc_id"],
                "stock_code": row["stock_code"],
                "stock_name": row["stock_name"],
                "title": row["announcement_title"],
                "pdf_path": row["local_pdf_path"],
                "markdown_path": str(markdown_path.relative_to(week13_dir)).replace("\\", "/"),
                "parser": "mineru",
                "pages": [{"page_no": 1, "text": text}],
            }
        )

    parsed_docs_path.parent.mkdir(parents=True, exist_ok=True)
    with parsed_docs_path.open("w", encoding="utf-8") as fh:
        for record in records:
            fh.write(json.dumps(record, ensure_ascii=False) + "\n")

    print(f"parsed docs written to {parsed_docs_path}")


if __name__ == "__main__":
    main()
