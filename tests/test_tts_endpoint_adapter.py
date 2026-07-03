from __future__ import annotations

import unittest

from agenda_falante.tts_endpoint_adapter import adapt_tts_plan_item, build_real_tts_payload


class TtsEndpointAdapterTests(unittest.TestCase):
    def test_fast_name_maps_to_expected_payload(self) -> None:
        payload = build_real_tts_payload(
            {
                "text": "João Silva",
                "language": "pt-BR",
                "voice": "default",
                "usage_profile": "fast_name",
                "request_id": "request-1",
                "segment_id": "segment-1",
                "cache_key": "cache-1",
                "output_path": "output/audio/segments/segment-1.wav",
                "metadata": {},
            }
        )
        self.assertEqual(set(payload.keys()), {"text", "provider", "language", "voice", "speed", "humanization"})
        self.assertEqual(payload["provider"], "elevenlabs")
        self.assertEqual(payload["speed"], 1.0)
        self.assertEqual(payload["humanization"]["enabled"], False)

    def test_expressive_template_maps_to_humanized_payload(self) -> None:
        payload = build_real_tts_payload({"text": "Olá Leo.", "usage_profile": "expressive_template"})
        self.assertEqual(payload["provider"], "elevenlabs")
        self.assertEqual(payload["speed"], 1.0)
        self.assertEqual(payload["humanization"]["enabled"], True)

    def test_notification_short_maps_to_speed_105(self) -> None:
        payload = build_real_tts_payload({"text": "Nova mensagem recebida.", "usage_profile": "notification_short"})
        self.assertEqual(payload["speed"], 1.05)
        self.assertEqual(payload["humanization"]["enabled"], False)

    def test_urgent_alert_maps_to_speed_095(self) -> None:
        payload = build_real_tts_payload({"text": "Atenção.", "usage_profile": "urgent_alert"})
        self.assertEqual(payload["speed"], 0.95)
        self.assertEqual(payload["humanization"]["enabled"], True)

    def test_internal_fields_do_not_enter_payload(self) -> None:
        payload = build_real_tts_payload(
            {
                "request_id": "request-1",
                "segment_id": "segment-1",
                "text": "Maria Souza",
                "language": "pt-BR",
                "voice": "default",
                "usage_profile": "fast_name",
                "cache_key": "cache-1",
                "output_path": "output/audio/segments/segment-1.wav",
                "metadata": {"source": "agenda_falante"},
            }
        )
        self.assertNotIn("request_id", payload)
        self.assertNotIn("segment_id", payload)
        self.assertNotIn("cache_key", payload)
        self.assertNotIn("output_path", payload)
        self.assertNotIn("usage_profile", payload)
        self.assertNotIn("metadata", payload)

    def test_adapter_wraps_preview_fields(self) -> None:
        adapted = adapt_tts_plan_item(
            {
                "request_id": "request-1",
                "segment_id": "segment-1",
                "text": "João Silva",
                "language": "pt-BR",
                "voice": "default",
                "usage_profile": "fast_name",
            }
        )
        self.assertEqual(adapted["endpoint"], "/api/generate-audio")
        self.assertEqual(adapted["method"], "POST")
        self.assertTrue(adapted["dry_run"])
        self.assertEqual(adapted["usage_profile"], "fast_name")


if __name__ == "__main__":
    unittest.main()
