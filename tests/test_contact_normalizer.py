from __future__ import annotations

import unittest

from agenda_falante.contact_normalizer import normalize_contacts, normalize_name, normalize_phone, split_first_last_name


class ContactNormalizerTests(unittest.TestCase):
    def test_normalize_name_preserves_accentuation(self) -> None:
        self.assertEqual(normalize_name("  João   da   Silva  "), "João da Silva")

    def test_split_first_last_name(self) -> None:
        first_name, last_name = split_first_last_name("Maria de Fátima Souza")
        self.assertEqual(first_name, "Maria")
        self.assertEqual(last_name, "de Fátima Souza")

    def test_normalize_phone(self) -> None:
        self.assertEqual(normalize_phone("(11) 98888-7777"), "+5511988887777")
        self.assertEqual(normalize_phone("+55 11 99999-0000"), "+5511999990000")

    def test_normalize_contacts_removes_duplicates_and_ignores_empty_names(self) -> None:
        contacts = normalize_contacts(
            [
                {
                    "source": "csv",
                    "full_name": " João Silva ",
                    "phones": ["(11) 98888-7777", "+55 11 98888-7777"],
                    "emails": ["JOAO.SILVA@example.com", "joao.silva@example.com"],
                    "organization": " Escossio Labs ",
                },
                {
                    "source": "csv",
                    "full_name": "",
                    "phones": ["111"],
                    "emails": ["empty@example.com"],
                    "organization": "",
                },
            ]
        )
        self.assertEqual(len(contacts), 1)
        self.assertEqual(contacts[0]["full_name"], "João Silva")
        self.assertEqual(contacts[0]["first_name"], "João")
        self.assertEqual(contacts[0]["last_name"], "Silva")
        self.assertEqual(contacts[0]["phones"], ["+5511988887777"])
        self.assertEqual(contacts[0]["emails"], ["joao.silva@example.com"])


if __name__ == "__main__":
    unittest.main()
