#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from agenda_falante.composer import compose_wav_segments


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compose a WAV announcement from ordered WAV segments.")
    parser.add_argument("--segments", nargs="+", required=True, help="Ordered list of WAV segment files.")
    parser.add_argument("--output", required=True, help="Output WAV file path.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        result = compose_wav_segments(args.segments, args.output)
    except (FileNotFoundError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(f"Segments: {result['segments_count']}")
    print(f"Output: {result['output_path']}")
    print(f"Approx duration: {result['duration_seconds']:.2f}s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
