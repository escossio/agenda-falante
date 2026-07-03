from __future__ import annotations

import unittest

from agenda_falante.tts_client import execute_real_tts_request


class RealTtsGuardrailTests(unittest.TestCase):
    def test_real_execution_fails_safe_without_flag(self) -> None:
        result = execute_real_tts_request(
            {
                "request_id": "request-1",
                "segment_id": "segment-1",
                "usage_profile": "fast_name",
            }
        )
        self.assertEqual(result["status"], "not_implemented")
        self.assertIn("execute_real_tts=True", result["error"])
        self.assertEqual(result["dry_run"], False)


if __name__ == "__main__":
    unittest.main()
