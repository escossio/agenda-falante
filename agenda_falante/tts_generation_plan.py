from __future__ import annotations

import hashlib
from collections.abc import Iterable
from pathlib import Path


def _stable_request_id(segment_id: str, segment_type: str, text: str, language: str, voice: str, output_path: str) -> str:
    payload = "|".join([segment_id.strip(), segment_type.strip(), text.strip().lower(), language.strip(), voice.strip(), output_path.strip()])
    return hashlib.sha1(payload.encode("utf-8")).hexdigest()


def _stable_cache_key(text: str, language: str, voice: str, output_format: str, usage_profile: str) -> str:
    payload = "|".join([text.strip().lower(), language.strip(), voice.strip(), output_format.strip(), usage_profile.strip()])
    return hashlib.sha1(payload.encode("utf-8")).hexdigest()


def build_tts_generation_plan(resolved_catalog: dict[str, object]) -> dict[str, object]:
    requests = []
    for segment in resolved_catalog.get("segments", []):
        if str(segment.get("status", "")).strip() != "missing":
            continue
        segment_id = str(segment.get("segment_id", "")).strip()
        segment_type = str(segment.get("segment_type", "")).strip()
        text = str(segment.get("text", "")).strip()
        language = str(segment.get("language", "pt-BR")).strip() or "pt-BR"
        voice = str(segment.get("voice", "default")).strip() or "default"
        usage_profile = "fast_name" if segment_type == "contact_name" else str(segment.get("usage_profile", "")).strip()
        output_format = "wav"
        output_path = f"output/audio/segments/{segment_id}.wav"
        request = {
            "request_id": _stable_request_id(segment_id, segment_type, text, language, voice, output_path),
            "segment_id": segment_id,
            "segment_type": segment_type,
            "text": text,
            "language": language,
            "voice": voice,
            "format": output_format,
            "usage_profile": usage_profile,
            "output_path": output_path,
            "cache_key": _stable_cache_key(text, language, voice, output_format, usage_profile),
            "metadata": {
                "source": "agenda_falante",
                "purpose": "segment_generation",
            },
        }
        requests.append(request)
    return {
        "plan_type": "tts_generation_plan",
        "requests": requests,
    }
