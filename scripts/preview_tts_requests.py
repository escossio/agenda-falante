#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from agenda_falante.tts_client import preview_tts_request


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Preview TTS requests in dry-run mode.")
    parser.add_argument("--plan", required=True, help="Path to the TTS generation plan.")
    parser.add_argument("--output", required=True, help="Path to the preview JSON output.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    plan_path = Path(args.plan)
    output_path = Path(args.output)

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

    requests = plan.get("requests", [])
    previews = [preview_tts_request(request) for request in requests]
    preview = {
        "preview_type": "tts_requests_preview",
        "tts_engine": "escossio_tts",
        "requests": previews,
    }
    output_path.write_text(json.dumps(preview, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"Total requests in plan: {len(requests)}")
    print(f"Total previews generated: {len(previews)}")
    print("TTS engine: escossio_tts")
    print(f"Output: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

