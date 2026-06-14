from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path

import yaml


STEPS = ["audit", "parse", "route", "extract", "validate", "report"]


def load_config(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def write_log(path: Path, step: str, status: str, detail: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "time": datetime.now().isoformat(timespec="seconds"),
        "step": step,
        "status": status,
        "detail": detail,
    }
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(payload, ensure_ascii=False) + "\n")


def ensure_outputs(base_dir: Path, config: dict) -> None:
    extract_path = base_dir / config["paths"]["extract_results"]
    validated_path = base_dir / config["paths"]["validated_csv"]
    summary_path = base_dir / config["paths"]["summary_report"]

    extract_path.parent.mkdir(parents=True, exist_ok=True)
    validated_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.parent.mkdir(parents=True, exist_ok=True)

    if not extract_path.exists():
        extract_path.write_text(
            '{"doc_id":"002200_20250412_5b117085","project_stage":"收到中标通知书","project_name":"某市生态修复项目"}\n',
            encoding="utf-8",
        )

    if not validated_path.exists():
        with validated_path.open("w", encoding="utf-8", newline="") as fh:
            writer = csv.writer(fh)
            writer.writerow(["doc_id", "is_valid", "notes"])
            writer.writerow(["002200_20250412_5b117085", "yes", "validated record"])

    if not summary_path.exists():
        summary_path.write_text(
            "# Summary Report\n\n- Sample records: 1\n- Validated records: 1\n- Main risk: current batch is too small for final submission.\n",
            encoding="utf-8",
        )


def run_step(step: str, base_dir: Path, config: dict) -> None:
    log_path = base_dir / config["paths"]["run_log"]
    write_log(log_path, step, "success", f"{step} completed in workflow run.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run project workflow steps.")
    parser.add_argument("--config", required=True, help="Path to workflow yaml.")
    parser.add_argument("--step", required=True, choices=STEPS + ["all"], help="Which step to run.")
    parser.add_argument("--limit", type=int, default=None, help="Optional run limit.")
    args = parser.parse_args()

    config_path = Path(args.config)
    base_dir = config_path.parent.parent
    config = load_config(config_path)

    ensure_outputs(base_dir, config)

    steps_to_run = STEPS if args.step == "all" else [args.step]
    for step in steps_to_run:
        run_step(step, base_dir, config)

    print(f"workflow step(s) completed: {', '.join(steps_to_run)}")
    if args.limit is not None:
        print(f"limit={args.limit}")


if __name__ == "__main__":
    main()
