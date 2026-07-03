from __future__ import annotations

import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path


PACKAGE_TYPE = "experience_package"
PACKAGE_VERSION = "0.1.0-alpha"


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def export_experience_package(
    resolved_segment_catalog: dict[str, object],
    audio_dir: str | Path,
    output_dir: str | Path,
    package_id: str,
) -> dict[str, object]:
    base_audio_dir = Path(audio_dir)
    package_dir = Path(output_dir) / package_id
    segments_dir = package_dir / "segments"
    announcements_dir = package_dir / "announcements"
    package_dir.mkdir(parents=True, exist_ok=True)
    segments_dir.mkdir(parents=True, exist_ok=True)
    announcements_dir.mkdir(parents=True, exist_ok=True)

    available_segments: list[dict[str, object]] = []
    ignored_missing: list[str] = []
    copied_files: list[Path] = []

    for segment in resolved_segment_catalog.get("segments", []):
        segment_id = str(segment.get("segment_id", "")).strip()
        status = str(segment.get("status", "")).strip()
        if not segment_id:
            continue
        if status != "available":
            ignored_missing.append(segment_id)
            continue

        source_audio = segment.get("audio_path")
        if source_audio:
            source_path = Path(str(source_audio))
        else:
            source_path = base_audio_dir / "segments" / f"{segment_id}.wav"
        if not source_path.exists():
            ignored_missing.append(segment_id)
            continue

        destination_path = segments_dir / f"{segment_id}.wav"
        shutil.copy2(source_path, destination_path)
        copied_files.append(destination_path)

        exported_segment = dict(segment)
        exported_segment["audio_path"] = str(destination_path)
        available_segments.append(exported_segment)

    manifest = {
        "package_id": package_id,
        "package_type": PACKAGE_TYPE,
        "segments": available_segments,
    }
    metadata = {
        "package_id": package_id,
        "package_type": PACKAGE_TYPE,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "version": PACKAGE_VERSION,
        "source": {
            "resolved_segment_catalog": str(resolved_segment_catalog.get("source", "resolved_segment_catalog")),
            "audio_dir": str(base_audio_dir),
        },
    }

    checksums = {
        "package_id": package_id,
        "package_type": PACKAGE_TYPE,
        "files": {
            str(path.relative_to(package_dir)): _sha256(path) for path in copied_files
        },
    }

    (package_dir / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (package_dir / "metadata.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (package_dir / "checksums.json").write_text(json.dumps(checksums, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    return {
        "package_dir": str(package_dir),
        "package_id": package_id,
        "available_segments": [str(segment["segment_id"]) for segment in available_segments],
        "ignored_missing": ignored_missing,
    }
