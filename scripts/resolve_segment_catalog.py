#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from agenda_falante.segment_resolver import resolve_segment_catalog, write_resolved_catalog


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Resolve segment catalog status from the filesystem.")
    parser.add_argument("--segment-catalog", required=True, help="Path to the segment catalog JSON.")
    parser.add_argument("--audio-dir", required=True, help="Base directory for audio lookup.")
    parser.add_argument("--output", required=True, help="Path to the resolved segment catalog JSON.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    catalog_path = Path(args.segment_catalog)
    audio_dir = Path(args.audio_dir)
    output_path = Path(args.output)

    if not catalog_path.exists():
        print(f"Error: segment catalog does not exist: {catalog_path}", file=sys.stderr)
        return 1
    if catalog_path.stat().st_size == 0:
        print(f"Error: segment catalog is empty: {catalog_path}", file=sys.stderr)
        return 1

    try:
        catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"Error: invalid JSON in segment catalog: {exc}", file=sys.stderr)
        return 1

    resolved = resolve_segment_catalog(catalog, audio_dir)
    segments = resolved.get("segments", [])
    available = sum(1 for segment in segments if segment.get("status") == "available")
    missing = sum(1 for segment in segments if segment.get("status") == "missing")

    write_resolved_catalog(resolved, output_path)

    print(f"Total segments: {len(segments)}")
    print(f"Available: {available}")
    print(f"Missing: {missing}")
    print(f"Audio directory: {audio_dir}")
    print(f"Output: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

