#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from agenda_falante.tts_endpoint_adapter import adapt_tts_plan_item
from agenda_falante.tts_client import execute_real_tts_request_with_endpoint


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Execute one real TTS plan item with explicit confirmation.")
    parser.add_argument("--plan", required=True, help="Path to the TTS generation plan.")
    parser.add_argument("--output", required=True, help="Path to the execution report JSON.")
    parser.add_argument("--base-url", help="Base URL of the real TTS service, e.g. http://127.0.0.1:8000")
    parser.add_argument("--request-id", help="Optional request_id to execute. Defaults to the first missing request.")
    parser.add_argument("--execute-real-tts", action="store_true", help="Required explicit confirmation for real TTS execution.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if bool(args.execute_real_tts) != bool(args.base_url):
        print(
            "Error: real TTS execution requires both --execute-real-tts and --base-url.",
            file=sys.stderr,
        )
        return 1

    plan_path = Path(args.plan)
    output_path = Path(args.output)
    if not plan_path.exists():
        print(f"Error: plan does not exist: {plan_path}", file=sys.stderr)
        return 1

    try:
        plan = json.loads(plan_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"Error: invalid JSON in plan: {exc}", file=sys.stderr)
        return 1

    requests = plan.get("requests", [])
    selected = None
    for request_item in requests:
        if args.request_id and str(request_item.get("request_id")) != args.request_id:
            continue
        selected = request_item
        break

    if selected is None:
        print("Error: no matching request found in plan.", file=sys.stderr)
        return 1

    adapted = adapt_tts_plan_item(selected)
    execution = execute_real_tts_request_with_endpoint(
        plan_item={
            **selected,
            "payload": adapted["payload"],
        },
        service_base_url=args.base_url,
        endpoint_path=adapted["endpoint"],
        execute_real_tts=True,
    )
    report = {
        "report_type": "real_tts_single_execution_report",
        "request": execution,
    }
    output_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Selected request_id: {execution.get('request_id')}")
    print(f"Status: {execution.get('status')}")
    print(f"Output: {output_path}")
    return 0 if execution.get("status") == "generated" else 2


if __name__ == "__main__":
    raise SystemExit(main())
