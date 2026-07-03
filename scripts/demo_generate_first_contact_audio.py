#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from agenda_falante.contact_importer import import_csv, import_vcf
from agenda_falante.contact_normalizer import normalize_contacts
from agenda_falante.manifest import build_contacts_manifest, write_contacts_manifest
from agenda_falante.segment_catalog import build_segment_catalog
from agenda_falante.segment_resolver import resolve_segment_catalog, write_resolved_catalog
from agenda_falante.tts_generation_plan import build_tts_generation_plan
from agenda_falante.tts_endpoint_adapter import adapt_tts_plan_item


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the first end-to-end Agenda Falante audio demo.")
    parser.add_argument("--input", required=True, help="Input contacts file.")
    parser.add_argument("--format", required=True, choices=("vcf", "csv"), help="Input format.")
    parser.add_argument("--workdir", required=True, help="Working directory for demo artifacts.")
    parser.add_argument("--base-url", required=True, help="Base URL of the local TTS service.")
    return parser.parse_args()


def _import_contacts(input_path: Path, input_format: str) -> list[dict[str, object]]:
    if input_format == "vcf":
        return import_vcf(input_path)
    if input_format == "csv":
        return import_csv(input_path)
    raise ValueError(f"Unsupported format: {input_format}")


def _run_real_tts_single(plan_path: Path, report_path: Path, base_url: str) -> dict[str, object]:
    script_path = PROJECT_ROOT / "scripts" / "run_real_tts_single.py"
    result = subprocess.run(
        [
            sys.executable,
            str(script_path),
            "--plan",
            str(plan_path),
            "--output",
            str(report_path),
            "--base-url",
            base_url,
            "--execute-real-tts",
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip() or "Real TTS execution failed.")
    if not report_path.exists():
        raise RuntimeError("Real TTS execution did not produce a report.")
    report = json.loads(report_path.read_text(encoding="utf-8"))
    request = report.get("request", {})
    if request.get("status") != "generated":
        raise RuntimeError(f"Real TTS execution failed: {request.get('error')}")
    return report


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

    try:
        imported_contacts = _import_contacts(input_path, args.format)
        normalized_contacts = normalize_contacts(imported_contacts)
        if not normalized_contacts:
            raise ValueError("No valid contacts after normalization")

        selected_contact = normalized_contacts[0]
        selected_contacts = [selected_contact]

        contacts_manifest = build_contacts_manifest(selected_contacts)
        contacts_manifest_path = workdir / "contacts_normalized.json"
        write_contacts_manifest(contacts_manifest, contacts_manifest_path)

        segment_catalog = build_segment_catalog(selected_contacts)
        segment_catalog_path = workdir / "segment_catalog.json"
        write_resolved_catalog(segment_catalog, segment_catalog_path)

        initial_resolved = resolve_segment_catalog(segment_catalog, workdir / "output/audio")
        initial_resolved_path = workdir / "segment_catalog_resolved_initial.json"
        write_resolved_catalog(initial_resolved, initial_resolved_path)

        plan = build_tts_generation_plan(initial_resolved)
        if len(plan.get("requests", [])) != 1:
            raise ValueError("Demo must generate exactly one TTS request.")

        selected_request = plan["requests"][0]
        if selected_request.get("segment_type") != "contact_name":
            raise ValueError("Demo only supports contact_name segments.")

        adapted_request = adapt_tts_plan_item(selected_request)
        execution_plan = {
            "plan_type": "tts_generation_plan",
            "requests": [
                {
                    **selected_request,
                    **adapted_request,
                    "output_path": str(workdir / str(selected_request["output_path"])),
                }
            ],
        }
        execution_plan_path = workdir / "tts_generation_plan_execution.json"
        write_resolved_catalog(execution_plan, execution_plan_path)

        tts_report_path = workdir / "real_tts_single_execution_report.json"
        started_at = time.monotonic()
        execution_report = _run_real_tts_single(execution_plan_path, tts_report_path, args.base_url)
        elapsed_seconds = time.monotonic() - started_at

        final_resolved = resolve_segment_catalog(segment_catalog, workdir / "output/audio")
        final_resolved_path = workdir / "segment_catalog_resolved_final.json"
        write_resolved_catalog(final_resolved, final_resolved_path)

        final_segment = final_resolved.get("segments", [])[0]
        wav_path = Path(str(execution_report["request"]["output_path"]))
        if not wav_path.exists():
            raise RuntimeError(f"Generated WAV not found: {wav_path}")
        if final_segment.get("status") != "available":
            raise RuntimeError("Resolved catalog did not mark the segment as available.")

        print("Contato processado:", selected_contact.get("full_name"))
        print("Nome do contato:", selected_contact.get("full_name"))
        print("Segment ID:", selected_request.get("segment_id"))
        print("Arquivo WAV gerado:", wav_path)
        print("Tempo total:", f"{elapsed_seconds:.2f}s")
        print("Status final:", final_segment.get("status"))
        return 0
    except (ValueError, OSError, RuntimeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
