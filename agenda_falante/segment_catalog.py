from __future__ import annotations

import hashlib
from collections.abc import Iterable


def _stable_segment_id(contact_id: str, segment_type: str, text: str, language: str, voice: str) -> str:
    payload = "|".join([contact_id.strip(), segment_type.strip(), text.strip().lower(), language.strip(), voice.strip()])
    return hashlib.sha1(payload.encode("utf-8")).hexdigest()


def build_segment_catalog(contacts: Iterable[dict[str, object]]) -> dict[str, object]:
    segments = []
    for contact in contacts:
        full_name = str(contact.get("full_name", "")).strip()
        if not full_name:
            continue
        contact_id = str(contact.get("contact_id", "")).strip()
        segment_type = "contact_name"
        language = "pt-BR"
        voice = "default"
        segment = {
            "segment_id": _stable_segment_id(contact_id, segment_type, full_name, language, voice),
            "segment_type": segment_type,
            "text": full_name,
            "language": language,
            "voice": voice,
            "source_contact_id": contact_id,
            "status": "missing",
        }
        segments.append(segment)
    return {"catalog_type": "segment_catalog", "segments": segments}

