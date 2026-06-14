from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from src.schemas import BiddingAnnouncementExtract


def load_jsonl(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8") as fh:
        return [json.loads(line) for line in fh if line.strip()]


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate extraction results with Pydantic schema.")
    parser.add_argument(
        "--input",
        default="outputs/results/final_results.jsonl",
        help="Path to extraction jsonl.",
    )
    parser.add_argument(
        "--output",
        default="outputs/results/records_validated.csv",
        help="Path to validation csv.",
    )
    args = parser.parse_args()

    input_path = BASE_DIR / args.input
    output_path = BASE_DIR / args.output
    output_path.parent.mkdir(parents=True, exist_ok=True)

    rows = load_jsonl(input_path)
    with output_path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["doc_id", "is_valid", "notes"])
        for row in rows:
            try:
                BiddingAnnouncementExtract.model_validate(row)
                writer.writerow([row["doc_id"], "yes", "schema validation passed"])
            except Exception as exc:  # noqa: BLE001
                writer.writerow([row.get("doc_id", ""), "no", str(exc)])

    print(f"validation written to {output_path}")


if __name__ == "__main__":
    main()
