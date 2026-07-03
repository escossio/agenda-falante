#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from agenda_falante.fake_tts_executor import run_fake_tts_executor, write_execution_report


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run a fake TTS executor for local pipeline validation.")
    parser.add_argument("--plan", required=True, help="Path to the TTS generation plan.")
    parser.add_argument("--report", required=True, help="Path to the execution report JSON.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    plan_path = Path(args.plan)
    report_path = Path(args.report)

    if not plan_path.exists():
        print(f"Error: plan does not exist: {plan_path}", file=sys.stderr)
        return 1
    if plan_path.stat().st_size == 0:
        print(f"Error: plan is empty: {plan_path}", file=sys.stderr)
        return 1

    try:
        plan = json.loads(plan_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"Error: invalid JSON in plan: {exc}", file=sys.stderr)
        return 1

    report = run_fake_tts_executor(plan)
    write_execution_report(report, report_path)
    requests = report.get("requests", [])
    generated = sum(1 for item in requests if item.get("status") == "generated")
    failed = sum(1 for item in requests if item.get("status") == "failed")

    print(f"Total requests: {len(requests)}")
    print(f"Generated: {generated}")
    print(f"Failed: {failed}")
    print(f"Report: {report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

