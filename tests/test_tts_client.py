from __future__ import annotations

import os
import unittest
from unittest.mock import patch

from agenda_falante.tts_client import get_tts_engine_name, preview_tts_request


class TtsClientTests(unittest.TestCase):
    def test_preview_contains_expected_fields(self) -> None:
        plan_item = {
            "request_id": "request-1",
            "text": "João Silva",
            "language": "pt-BR",
            "voice": "default",
            "format": "wav",
            "usage_profile": "fast_name",
            "output_path": "output/audio/segments/segment-1.wav",
            "cache_key": "cache-1",
            "metadata": {"source": "agenda_falante", "purpose": "segment_generation"},
        }
        original = dict(plan_item)
        preview = preview_tts_request(plan_item)
        self.assertEqual(preview["tts_engine"], "escossio_tts")
        self.assertTrue(preview["dry_run"])
        self.assertEqual(preview["request_id"], "request-1")
        self.assertEqual(preview["usage_profile"], "fast_name")
        self.assertEqual(preview["metadata"]["source"], "agenda_falante")
        self.assertEqual(preview["metadata"]["purpose"], "segment_generation")
        self.assertEqual(plan_item, original)

    def test_default_engine_is_escossio_tts(self) -> None:
        old_value = os.environ.pop("AGENDA_FALANTE_TTS_ENGINE", None)
        try:
            self.assertEqual(get_tts_engine_name(), "escossio_tts")
        finally:
            if old_value is not None:
                os.environ["AGENDA_FALANTE_TTS_ENGINE"] = old_value

    def test_engine_can_be_read_from_environment(self) -> None:
        old_value = os.environ.get("AGENDA_FALANTE_TTS_ENGINE")
        os.environ["AGENDA_FALANTE_TTS_ENGINE"] = "test_engine"
        try:
            preview = preview_tts_request(
                {
                    "request_id": "request-1",
                    "text": "João Silva",
                    "language": "pt-BR",
                    "voice": "default",
                    "format": "wav",
                    "usage_profile": "fast_name",
                    "output_path": "output/audio/segments/segment-1.wav",
                    "cache_key": "cache-1",
                    "metadata": {"source": "agenda_falante", "purpose": "segment_generation"},
                }
            )
            self.assertEqual(preview["tts_engine"], "test_engine")
        finally:
            if old_value is None:
                os.environ.pop("AGENDA_FALANTE_TTS_ENGINE", None)
            else:
                os.environ["AGENDA_FALANTE_TTS_ENGINE"] = old_value

    def test_preview_does_not_use_network_primitives(self) -> None:
        plan_item = {
            "request_id": "request-1",
            "text": "João Silva",
            "language": "pt-BR",
            "voice": "default",
            "format": "wav",
            "usage_profile": "fast_name",
            "output_path": "output/audio/segments/segment-1.wav",
            "cache_key": "cache-1",
            "metadata": {"source": "agenda_falante", "purpose": "segment_generation"},
        }
        with patch("socket.socket", side_effect=AssertionError("network not allowed")), \
            patch("http.client.HTTPConnection", side_effect=AssertionError("network not allowed")), \
            patch("http.client.HTTPSConnection", side_effect=AssertionError("network not allowed")):
            preview = preview_tts_request(plan_item)
        self.assertTrue(preview["dry_run"])
        self.assertEqual(preview["tts_engine"], "escossio_tts")
        self.assertEqual(plan_item["request_id"], "request-1")


if __name__ == "__main__":
    unittest.main()
