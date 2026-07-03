#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from agenda_falante.tts_client import execute_real_tts_request


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run a real TTS plan with an explicit safety flag.")
    parser.add_argument("--plan", required=True, help="Path to the TTS generation plan.")
    parser.add_argument("--report", required=True, help="Path to the JSON report output.")
    parser.add_argument("--execute-real-tts", action="store_true", help="Required explicit confirmation for real TTS execution.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.execute_real_tts:
        print("Error: real TTS execution requires explicit confirmation via --execute-real-tts.", file=sys.stderr)
        return 1

    plan_path = Path(args.plan)
    report_path = Path(args.report)
    if not plan_path.exists():
        print(f"Error: plan does not exist: {plan_path}", file=sys.stderr)
        return 1
    try:
        plan = json.loads(plan_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"Error: invalid JSON in plan: {exc}", file=sys.stderr)
        return 1

    requests = plan.get("requests", [])
    report = {
        "report_type": "real_tts_execution_report",
        "requests": [execute_real_tts_request(request, execute_real_tts=True) for request in requests],
    }
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Total requests in plan: {len(requests)}")
    print(f"Total report entries: {len(report['requests'])}")
    print(f"Output: {report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
