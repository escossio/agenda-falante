#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from agenda_falante.experience_package import export_experience_package


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Export a local Experience Package from a resolved segment catalog.")
    parser.add_argument("--resolved-segment-catalog", required=True, help="Path to the resolved segment catalog JSON.")
    parser.add_argument("--audio-dir", required=True, help="Base directory for audio assets.")
    parser.add_argument("--output-dir", required=True, help="Directory where the Experience Package will be created.")
    parser.add_argument("--package-id", required=True, help="Identifier of the exported package.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    catalog_path = Path(args.resolved_segment_catalog)
    try:
        resolved_segment_catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
        result = export_experience_package(resolved_segment_catalog, args.audio_dir, args.output_dir, args.package_id)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(f"package_id: {result['package_id']}")
    print(f"segmentos disponíveis exportados: {', '.join(result['available_segments']) or '(nenhum)'}")
    print(f"segmentos ignorados por missing: {', '.join(result['ignored_missing']) or '(nenhum)'}")
    print(f"diretório final: {result['package_dir']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
