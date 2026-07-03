from __future__ import annotations

import unittest

from agenda_falante.contact_normalizer import normalize_contacts
from agenda_falante.segment_catalog import build_segment_catalog


class SegmentCatalogTests(unittest.TestCase):
    def test_build_segment_catalog_creates_one_segment_per_contact(self) -> None:
        contacts = normalize_contacts(
            [
                {
                    "source": "csv",
                    "contact_id": "contact-1",
                    "full_name": "João Silva",
                    "phones": ["+5511999990000"],
                    "emails": ["joao@example.com"],
                    "organization": "Escossio",
                },
                {
                    "source": "csv",
                    "contact_id": "contact-2",
                    "full_name": "Maria Souza",
                    "phones": ["+5511988887777"],
                    "emails": ["maria@example.com"],
                    "organization": "",
                },
            ]
        )
        catalog = build_segment_catalog(contacts)
        self.assertEqual(catalog["catalog_type"], "segment_catalog")
        self.assertEqual(len(catalog["segments"]), 2)
        self.assertEqual(catalog["segments"][0]["text"], "João Silva")
        self.assertEqual(catalog["segments"][0]["segment_type"], "contact_name")
        self.assertEqual(catalog["segments"][0]["status"], "missing")

    def test_segment_id_is_stable(self) -> None:
        contact = [
            {
                "source": "csv",
                "contact_id": "contact-1",
                "full_name": "João Silva",
                "phones": ["+5511999990000"],
                "emails": ["joao@example.com"],
                "organization": "Escossio",
            }
        ]
        first = build_segment_catalog(contact)["segments"][0]["segment_id"]
        second = build_segment_catalog(contact)["segments"][0]["segment_id"]
        self.assertEqual(first, second)

    def test_catalog_does_not_include_audio_path_or_tts(self) -> None:
        catalog = build_segment_catalog(
            [
                {
                    "source": "csv",
                    "contact_id": "contact-1",
                    "full_name": "João Silva",
                    "phones": [],
                    "emails": [],
                    "organization": "",
                }
            ]
        )
        serialized = str(catalog).lower()
        self.assertNotIn("path", serialized)
        self.assertNotIn("tts", serialized)
        self.assertNotIn("audio", serialized)


if __name__ == "__main__":
    unittest.main()
