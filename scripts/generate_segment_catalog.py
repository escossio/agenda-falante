#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from agenda_falante.manifest import write_contacts_manifest
from agenda_falante.segment_catalog import build_segment_catalog


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a segment catalog from a normalized contacts manifest.")
    parser.add_argument("--contacts-manifest", required=True, help="Path to the normalized contacts manifest.")
    parser.add_argument("--output", required=True, help="Path to the segment catalog JSON output.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    input_path = Path(args.contacts_manifest)
    output_path = Path(args.output)

    if not input_path.exists():
        print(f"Error: input file does not exist: {input_path}", file=sys.stderr)
        return 1
    if input_path.stat().st_size == 0:
        print(f"Error: input file is empty: {input_path}", file=sys.stderr)
        return 1

    try:
        manifest = json.loads(input_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"Error: invalid JSON in contacts manifest: {exc}", file=sys.stderr)
        return 1

    contacts = manifest.get("contacts", [])
    if not contacts:
        print(f"Error: no contacts found in manifest: {input_path}", file=sys.stderr)
        return 1

    catalog = build_segment_catalog(contacts)
    segments = catalog["segments"]
    if not segments:
        print(f"Error: no segments generated from manifest: {input_path}", file=sys.stderr)
        return 1

    write_contacts_manifest(catalog, output_path)

    missing_segments = sum(1 for segment in segments if segment.get("status") == "missing")
    print(f"Contacts read: {len(contacts)}")
    print(f"Segments generated: {len(segments)}")
    print(f"Missing segments: {missing_segments}")
    print(f"Output: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

