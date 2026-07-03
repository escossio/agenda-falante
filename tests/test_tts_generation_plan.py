from __future__ import annotations

import unittest

from agenda_falante.tts_generation_plan import build_tts_generation_plan


class TtsGenerationPlanTests(unittest.TestCase):
    def test_only_missing_segments_are_planned(self) -> None:
        plan = build_tts_generation_plan(
            {
                "plan_type": "segment_catalog",
                "segments": [
                    {
                        "segment_id": "segment-available",
                        "segment_type": "contact_name",
                        "text": "João Silva",
                        "language": "pt-BR",
                        "voice": "default",
                        "status": "available",
                    },
                    {
                        "segment_id": "segment-missing",
                        "segment_type": "contact_name",
                        "text": "Maria Souza",
                        "language": "pt-BR",
                        "voice": "default",
                        "status": "missing",
                    },
                ],
            }
        )
        self.assertEqual(plan["plan_type"], "tts_generation_plan")
        self.assertEqual(len(plan["requests"]), 1)
        request = plan["requests"][0]
        self.assertEqual(request["segment_id"], "segment-missing")
        self.assertEqual(request["usage_profile"], "fast_name")
        self.assertEqual(request["format"], "wav")
        self.assertEqual(request["output_path"], "output/audio/segments/segment-missing.wav")
        self.assertEqual(request["metadata"]["source"], "agenda_falante")
        self.assertEqual(request["metadata"]["purpose"], "segment_generation")

    def test_request_id_and_cache_key_are_stable(self) -> None:
        catalog = {
            "segments": [
                {
                    "segment_id": "segment-missing",
                    "segment_type": "contact_name",
                    "text": "Maria Souza",
                    "language": "pt-BR",
                    "voice": "default",
                    "status": "missing",
                }
            ]
        }
        first = build_tts_generation_plan(catalog)["requests"][0]
        second = build_tts_generation_plan(catalog)["requests"][0]
        self.assertEqual(first["request_id"], second["request_id"])
        self.assertEqual(first["cache_key"], second["cache_key"])

    def test_cache_key_depends_on_usage_profile(self) -> None:
        catalog = {
            "segments": [
                {
                    "segment_id": "segment-missing",
                    "segment_type": "notification",
                    "text": "Nova mensagem recebida",
                    "language": "pt-BR",
                    "voice": "default",
                    "usage_profile": "notification_short",
                    "status": "missing",
                }
            ]
        }
        base = build_tts_generation_plan(catalog)["requests"][0]
        catalog["segments"][0]["usage_profile"] = "urgent_alert"
        changed = build_tts_generation_plan(catalog)["requests"][0]
        self.assertNotEqual(base["cache_key"], changed["cache_key"])


if __name__ == "__main__":
    unittest.main()
