from __future__ import annotations

import argparse
import json
from pathlib import Path

import yaml


def load_jsonl(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8") as fh:
        return [json.loads(line) for line in fh if line.strip()]


def load_rules(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def main() -> None:
    parser = argparse.ArgumentParser(description="Route sections from parsed docs using keyword rules.")
    parser.add_argument("--parsed", required=True, help="Path to parsed_docs.jsonl")
    parser.add_argument("--rules", required=True, help="Path to section_rules.yaml")
    args = parser.parse_args()

    parsed_path = Path(args.parsed)
    rules_path = Path(args.rules)
    week13_dir = Path(__file__).resolve().parents[1]

    docs = load_jsonl(parsed_path)
    rules = load_rules(rules_path)["target_sections"]
    output_path = week13_dir / "data/parsed/sections.jsonl"

    routed_sections: list[dict] = []
    for doc in docs:
        full_text = "\n".join(page["text"] for page in doc["pages"])
        for section_name, rule in rules.items():
            include_keywords = rule.get("include_keywords", [])
            found = any(keyword in full_text for keyword in include_keywords)
            routed_sections.append(
                {
                    "doc_id": doc["doc_id"],
                    "title": doc["title"],
                    "target_section": section_name,
                    "found": found,
                    "page_start": 1 if found else None,
                    "page_end": 1 if found else None,
                }
            )

    with output_path.open("w", encoding="utf-8") as fh:
        for item in routed_sections:
            fh.write(json.dumps(item, ensure_ascii=False) + "\n")

    print(f"sections written to {output_path}")


if __name__ == "__main__":
    main()
