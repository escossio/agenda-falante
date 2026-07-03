from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any
from urllib.parse import urljoin
from urllib import request as urlrequest


def get_tts_engine_name() -> str:
    return os.getenv("AGENDA_FALANTE_TTS_ENGINE", "escossio_tts")


def preview_tts_request(plan_item: dict[str, Any]) -> dict[str, Any]:
    return {
        "request_id": plan_item.get("request_id"),
        "text": plan_item.get("text"),
        "language": plan_item.get("language"),
        "voice": plan_item.get("voice"),
        "format": plan_item.get("format"),
        "usage_profile": plan_item.get("usage_profile"),
        "output_path": plan_item.get("output_path"),
        "cache_key": plan_item.get("cache_key"),
        "metadata": dict(plan_item.get("metadata", {})),
        "tts_engine": get_tts_engine_name(),
        "dry_run": True,
    }


def execute_real_tts_request(plan_item: dict[str, Any], *, execute_real_tts: bool = False) -> dict[str, Any]:
    if execute_real_tts is not True:
        return {
            "request_id": plan_item.get("request_id"),
            "segment_id": plan_item.get("segment_id"),
            "status": "not_implemented",
            "error": "Real TTS execution requires execute_real_tts=True.",
            "tts_engine": get_tts_engine_name(),
            "usage_profile": plan_item.get("usage_profile"),
            "dry_run": False,
        }

    return {
        "request_id": plan_item.get("request_id"),
        "segment_id": plan_item.get("segment_id"),
        "status": "not_implemented",
        "error": "Real TTS integration is not implemented yet.",
        "tts_engine": get_tts_engine_name(),
        "usage_profile": plan_item.get("usage_profile"),
        "dry_run": False,
    }


def execute_real_tts_request_with_endpoint(
    *,
    plan_item: dict[str, Any],
    service_base_url: str,
    endpoint_path: str = "/api/generate-audio",
    execute_real_tts: bool = False,
) -> dict[str, Any]:
    if execute_real_tts is not True:
        return {
            "request_id": plan_item.get("request_id"),
            "segment_id": plan_item.get("segment_id"),
            "status": "not_implemented",
            "error": "Real TTS execution requires execute_real_tts=True.",
            "tts_engine": get_tts_engine_name(),
            "usage_profile": plan_item.get("usage_profile"),
            "dry_run": False,
        }

    payload = plan_item.get("payload")
    output_path = Path(str(plan_item.get("output_path", "")).strip())
    if not isinstance(payload, dict):
        return {
            "request_id": plan_item.get("request_id"),
            "segment_id": plan_item.get("segment_id"),
            "status": "error",
            "error": "Invalid payload for real TTS execution.",
            "tts_engine": get_tts_engine_name(),
            "usage_profile": plan_item.get("usage_profile"),
            "dry_run": False,
        }

    if not str(service_base_url).strip():
        return {
            "request_id": plan_item.get("request_id"),
            "segment_id": plan_item.get("segment_id"),
            "status": "error",
            "error": "Endpoint URL is required.",
            "tts_engine": get_tts_engine_name(),
            "usage_profile": plan_item.get("usage_profile"),
            "dry_run": False,
        }

    try:
        payload_bytes = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        endpoint_url = urljoin(service_base_url.rstrip("/") + "/", endpoint_path.lstrip("/"))
        req = urlrequest.Request(
            endpoint_url,
            data=payload_bytes,
            headers={"Content-Type": "application/json", "Accept": "application/json"},
            method="POST",
        )
        with urlrequest.urlopen(req, timeout=30) as response:
            response_data = json.loads(response.read().decode("utf-8"))
    except Exception as exc:
        return {
            "request_id": plan_item.get("request_id"),
            "segment_id": plan_item.get("segment_id"),
            "status": "error",
            "error": f"Failed to call real TTS endpoint: {exc}",
            "tts_engine": get_tts_engine_name(),
            "usage_profile": plan_item.get("usage_profile"),
            "dry_run": False,
        }

    audio_url = str(response_data.get("audio_url", "")).strip()
    if not audio_url:
        return {
            "request_id": plan_item.get("request_id"),
            "segment_id": plan_item.get("segment_id"),
            "status": "error",
            "error": "Real TTS endpoint did not return audio_url.",
            "tts_engine": get_tts_engine_name(),
            "usage_profile": plan_item.get("usage_profile"),
            "dry_run": False,
        }

    download_url = audio_url if audio_url.startswith("http://") or audio_url.startswith("https://") else urljoin(
        service_base_url.rstrip("/") + "/",
        audio_url.lstrip("/"),
    )
    try:
        download_req = urlrequest.Request(download_url, method="GET")
        with urlrequest.urlopen(download_req, timeout=30) as response:
            audio_bytes = response.read()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_bytes(audio_bytes)
    except Exception as exc:
        return {
            "request_id": plan_item.get("request_id"),
            "segment_id": plan_item.get("segment_id"),
            "status": "error",
            "error": f"Failed to download real TTS audio: {exc}",
            "tts_engine": get_tts_engine_name(),
            "usage_profile": plan_item.get("usage_profile"),
            "dry_run": False,
            "audio_url": audio_url,
        }

    return {
        "request_id": plan_item.get("request_id"),
        "segment_id": plan_item.get("segment_id"),
        "status": "generated",
        "error": None,
        "tts_engine": get_tts_engine_name(),
        "usage_profile": plan_item.get("usage_profile"),
        "dry_run": False,
        "audio_url": audio_url,
        "output_path": str(output_path),
    }
