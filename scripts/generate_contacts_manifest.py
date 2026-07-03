#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from agenda_falante.contact_importer import import_csv, import_vcf
from agenda_falante.contact_normalizer import normalize_contacts
from agenda_falante.manifest import build_contacts_manifest, write_contacts_manifest


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a normalized contacts manifest from VCF or CSV.")
    parser.add_argument("--input", required=True, help="Path to the input file.")
    parser.add_argument("--output", required=True, help="Path to the JSON manifest output.")
    parser.add_argument("--format", required=True, choices=("vcf", "csv"), help="Input file format.")
    return parser.parse_args()


def load_contacts(input_path: Path, input_format: str) -> list[dict[str, object]]:
    if not input_path.exists():
        raise FileNotFoundError(f"Input file does not exist: {input_path}")
    if input_path.stat().st_size == 0:
        raise ValueError(f"Input file is empty: {input_path}")
    if input_format == "vcf":
        return import_vcf(input_path)
    if input_format == "csv":
        return import_csv(input_path)
    raise ValueError(f"Unsupported format: {input_format}")


def main() -> int:
    args = parse_args()
    input_path = Path(args.input)
    output_path = Path(args.output)

    try:
        imported_contacts = load_contacts(input_path, args.format)
        if not imported_contacts:
            raise ValueError(f"No valid contacts found in input file: {input_path}")
        normalized_contacts = normalize_contacts(imported_contacts)
        if not normalized_contacts:
            raise ValueError(f"No valid contacts after normalization for input file: {input_path}")
        manifest = build_contacts_manifest(normalized_contacts)
        write_contacts_manifest(manifest, output_path)
    except (FileNotFoundError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(f"Input: {input_path}")
    print(f"Format: {args.format}")
    print(f"Imported contacts: {len(imported_contacts)}")
    print(f"Normalized contacts: {len(normalized_contacts)}")
    print(f"Output: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
