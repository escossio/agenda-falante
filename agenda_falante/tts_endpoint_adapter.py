from __future__ import annotations

from typing import Any


_USAGE_PROFILE_MAPPING: dict[str, dict[str, object]] = {
    "fast_name": {
        "provider": "elevenlabs",
        "speed": 1.0,
        "humanization": {"enabled": False, "preset": "natural"},
    },
    "expressive_template": {
        "provider": "elevenlabs",
        "speed": 1.0,
        "humanization": {"enabled": True, "preset": "natural"},
    },
    "notification_short": {
        "provider": "elevenlabs",
        "speed": 1.05,
        "humanization": {"enabled": False, "preset": "natural"},
    },
    "urgent_alert": {
        "provider": "elevenlabs",
        "speed": 0.95,
        "humanization": {"enabled": True, "preset": "natural"},
    },
}


def _default_humanization() -> dict[str, object]:
    return {"enabled": False, "preset": "natural"}


def resolve_tts_endpoint_mapping(usage_profile: str | None) -> dict[str, object]:
    return dict(_USAGE_PROFILE_MAPPING.get((usage_profile or "").strip(), _USAGE_PROFILE_MAPPING["fast_name"]))


def build_real_tts_payload(plan_item: dict[str, Any]) -> dict[str, Any]:
    usage_profile = str(plan_item.get("usage_profile", "")).strip() or "fast_name"
    mapping = resolve_tts_endpoint_mapping(usage_profile)
    humanization = mapping.get("humanization")
    if not isinstance(humanization, dict):
        humanization = _default_humanization()

    return {
        "text": str(plan_item.get("text", "")).strip(),
        "provider": str(mapping.get("provider", "elevenlabs")).strip() or "elevenlabs",
        "language": str(plan_item.get("language", "pt-BR")).strip() or "pt-BR",
        "voice": str(plan_item.get("voice", "")).strip(),
        "speed": float(mapping.get("speed", 1.0)),
        "humanization": dict(humanization),
    }


def adapt_tts_plan_item(plan_item: dict[str, Any]) -> dict[str, Any]:
    return {
        "request_id": plan_item.get("request_id"),
        "segment_id": plan_item.get("segment_id"),
        "usage_profile": plan_item.get("usage_profile", "fast_name"),
        "endpoint": "/api/generate-audio",
        "method": "POST",
        "payload": build_real_tts_payload(plan_item),
        "dry_run": True,
    }
