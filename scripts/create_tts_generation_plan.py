#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from agenda_falante.segment_resolver import write_resolved_catalog
from agenda_falante.tts_generation_plan import build_tts_generation_plan


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a TTS generation plan from a resolved segment catalog.")
    parser.add_argument("--resolved-segment-catalog", required=True, help="Path to the resolved segment catalog.")
    parser.add_argument("--output", required=True, help="Path to the TTS generation plan JSON.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    catalog_path = Path(args.resolved_segment_catalog)
    output_path = Path(args.output)

    if not catalog_path.exists():
        print(f"Error: resolved segment catalog does not exist: {catalog_path}", file=sys.stderr)
        return 1
    if catalog_path.stat().st_size == 0:
        print(f"Error: resolved segment catalog is empty: {catalog_path}", file=sys.stderr)
        return 1

    try:
        catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"Error: invalid JSON in resolved segment catalog: {exc}", file=sys.stderr)
        return 1

    segments = catalog.get("segments", [])
    missing = sum(1 for segment in segments if segment.get("status") == "missing")
    available = sum(1 for segment in segments if segment.get("status") == "available")
    plan = build_tts_generation_plan(catalog)
    requests = plan.get("requests", [])

    write_resolved_catalog(plan, output_path)

    print(f"Total segments read: {len(segments)}")
    print(f"Missing: {missing}")
    print(f"Available: {available}")
    print(f"Requests created: {len(requests)}")
    print(f"Output: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

