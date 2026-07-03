from __future__ import annotations

import unittest
from unittest.mock import patch

from agenda_falante.tts_client import preview_tts_request


class TtsClientNoNetworkTests(unittest.TestCase):
    def test_preview_survives_network_blocks(self) -> None:
        plan_item = {
            "request_id": "request-2",
            "text": "Maria Souza",
            "language": "pt-BR",
            "voice": "default",
            "format": "wav",
            "usage_profile": "fast_name",
            "output_path": "output/audio/segments/segment-2.wav",
            "cache_key": "cache-2",
            "metadata": {"source": "agenda_falante", "purpose": "segment_generation"},
        }
        with patch("socket.socket", side_effect=AssertionError("network not allowed")), \
            patch("urllib.request.urlopen", side_effect=AssertionError("network not allowed")), \
            patch("http.client.HTTPConnection", side_effect=AssertionError("network not allowed")), \
            patch("http.client.HTTPSConnection", side_effect=AssertionError("network not allowed")):
            preview = preview_tts_request(plan_item)
        self.assertTrue(preview["dry_run"])
        self.assertEqual(preview["tts_engine"], "escossio_tts")
        self.assertEqual(preview["request_id"], "request-2")
        self.assertEqual(plan_item["request_id"], "request-2")


if __name__ == "__main__":
    unittest.main()
