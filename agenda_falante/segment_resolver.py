from __future__ import annotations

import json
from pathlib import Path
from collections.abc import Iterable


def resolve_segment_catalog(catalog: dict[str, object], audio_dir: str | Path) -> dict[str, object]:
    base_dir = Path(audio_dir)
    resolved_segments = []
    for segment in catalog.get("segments", []):
        segment_id = str(segment.get("segment_id", "")).strip()
        if not segment_id:
            continue
        expected_path = base_dir / "segments" / f"{segment_id}.wav"
        resolved_segment = dict(segment)
        if expected_path.exists():
            resolved_segment["status"] = "available"
            resolved_segment["audio_path"] = str(expected_path)
        else:
            resolved_segment["status"] = "missing"
            resolved_segment.pop("audio_path", None)
        resolved_segments.append(resolved_segment)
    return {
        **{k: v for k, v in catalog.items() if k != "segments"},
        "segments": resolved_segments,
        "catalog_type": catalog.get("catalog_type", "segment_catalog"),
    }


def write_resolved_catalog(catalog: dict[str, object], path: str | Path) -> None:
    Path(path).write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

