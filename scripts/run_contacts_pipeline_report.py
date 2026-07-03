#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from agenda_falante.contact_importer import import_csv, import_vcf
from agenda_falante.contact_normalizer import normalize_contacts
from agenda_falante.fake_tts_executor import run_fake_tts_executor, write_execution_report
from agenda_falante.manifest import build_contacts_manifest, write_contacts_manifest
from agenda_falante.segment_catalog import build_segment_catalog
from agenda_falante.segment_resolver import resolve_segment_catalog, write_resolved_catalog
from agenda_falante.tts_generation_plan import build_tts_generation_plan


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the initial Agenda Falante pipeline and generate a consolidated report.")
    parser.add_argument("--input", required=True, help="Input contacts file.")
    parser.add_argument("--format", required=True, choices=("vcf", "csv"), help="Input format.")
    parser.add_argument("--workdir", required=True, help="Working directory for temporary artifacts and reports.")
    return parser.parse_args()


def _import_contacts(input_path: Path, input_format: str) -> list[dict[str, object]]:
    if input_format == "vcf":
        return import_vcf(input_path)
    if input_format == "csv":
        return import_csv(input_path)
    raise ValueError(f"Unsupported format: {input_format}")


def main() -> int:
    args = parse_args()
    input_path = Path(args.input)
    workdir = Path(args.workdir)
    workdir.mkdir(parents=True, exist_ok=True)

    if not input_path.exists():
        print(f"Error: input file does not exist: {input_path}", file=sys.stderr)
        return 1
    if input_path.stat().st_size == 0:
        print(f"Error: input file is empty: {input_path}", file=sys.stderr)
        return 1

    artifacts = {}
    try:
        imported_contacts = _import_contacts(input_path, args.format)
        normalized_contacts = normalize_contacts(imported_contacts)
        if not normalized_contacts:
            raise ValueError("No valid contacts after normalization")

        contacts_manifest = build_contacts_manifest(normalized_contacts)
        contacts_manifest_path = workdir / "contacts_normalized.json"
        write_contacts_manifest(contacts_manifest, contacts_manifest_path)

        segment_catalog = build_segment_catalog(normalized_contacts)
        segment_catalog_path = workdir / "segment_catalog.json"
        write_resolved_catalog(segment_catalog, segment_catalog_path)

        initial_resolved = resolve_segment_catalog(segment_catalog, workdir / "output/audio")
        initial_resolved_path = workdir / "segment_catalog_resolved_initial.json"
        write_resolved_catalog(initial_resolved, initial_resolved_path)

        plan = build_tts_generation_plan(initial_resolved)
        plan_path = workdir / "tts_generation_plan.json"
        write_resolved_catalog(plan, plan_path)

        execution_plan = json.loads(json.dumps(plan))
        for request in execution_plan.get("requests", []):
            request["output_path"] = str(workdir / request["output_path"])
        execution_plan_path = workdir / "tts_generation_plan_execution.json"
        write_resolved_catalog(execution_plan, execution_plan_path)

        execution_report = run_fake_tts_executor(execution_plan)
        execution_report_path = workdir / "fake_tts_execution_report.json"
        write_execution_report(execution_report, execution_report_path)

        final_resolved = resolve_segment_catalog(segment_catalog, workdir / "output/audio")
        final_resolved_path = workdir / "segment_catalog_resolved_final.json"
        write_resolved_catalog(final_resolved, final_resolved_path)

        report = {
            "input_file": str(input_path),
            "input_format": args.format,
            "contacts_imported": len(imported_contacts),
            "contacts_normalized": len(normalized_contacts),
            "segments_total": len(segment_catalog.get("segments", [])),
            "segments_initial_available": sum(1 for segment in initial_resolved.get("segments", []) if segment.get("status") == "available"),
            "segments_initial_missing": sum(1 for segment in initial_resolved.get("segments", []) if segment.get("status") == "missing"),
            "tts_requests_created": len(plan.get("requests", [])),
            "fake_tts_generated": sum(1 for item in execution_report.get("requests", []) if item.get("status") == "generated"),
            "fake_tts_failed": sum(1 for item in execution_report.get("requests", []) if item.get("status") == "failed"),
            "segments_final_available": sum(1 for segment in final_resolved.get("segments", []) if segment.get("status") == "available"),
            "segments_final_missing": sum(1 for segment in final_resolved.get("segments", []) if segment.get("status") == "missing"),
            "artifacts": {
                "contacts_manifest": str(contacts_manifest_path),
                "segment_catalog": str(segment_catalog_path),
                "segment_catalog_resolved_initial": str(initial_resolved_path),
                "tts_generation_plan": str(plan_path),
                "tts_generation_plan_execution": str(execution_plan_path),
                "fake_tts_execution_report": str(execution_report_path),
                "segment_catalog_resolved_final": str(final_resolved_path),
            },
        }
    except (ValueError, OSError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    report_path = workdir / "pipeline_report.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Report: {report_path}")
    print(f"Contacts imported: {report['contacts_imported']}")
    print(f"Contacts normalized: {report['contacts_normalized']}")
    print(f"Segments total: {report['segments_total']}")
    print(f"Segments final available: {report['segments_final_available']}")
    print(f"Segments final missing: {report['segments_final_missing']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
