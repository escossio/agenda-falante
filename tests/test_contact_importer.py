from __future__ import annotations

import unittest

from agenda_falante.contact_importer import import_csv, import_vcf


class ContactImporterTests(unittest.TestCase):
    def test_import_vcf(self) -> None:
        contacts = import_vcf("fixtures/sample_contacts.vcf")
        self.assertEqual(len(contacts), 2)
        self.assertEqual(contacts[0]["full_name"], "João Silva")
        self.assertEqual(contacts[0]["first_name"], "João")
        self.assertEqual(contacts[0]["last_name"], "Silva")
        self.assertEqual(contacts[0]["phones"], ["+55 11 99999-0000", "11999990000"])
        self.assertEqual(contacts[0]["emails"], ["joao.silva@example.com"])
        self.assertEqual(contacts[0]["organization"], "Escossio Labs")

    def test_import_csv(self) -> None:
        contacts = import_csv("fixtures/sample_contacts.csv")
        self.assertEqual(len(contacts), 3)
        self.assertEqual(contacts[0]["full_name"], "João Silva")
        self.assertEqual(contacts[0]["phones"], ["+55 11 99999-0000", "+55 (11) 98888-7777"])
        self.assertEqual(contacts[0]["emails"], ["joao.silva@example.com"])
        self.assertEqual(contacts[1]["full_name"], "Maria Souza")
        self.assertEqual(contacts[2]["full_name"], "Carlos Lima")


if __name__ == "__main__":
    unittest.main()
