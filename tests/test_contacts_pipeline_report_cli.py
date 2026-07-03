from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class ContactsPipelineReportCliTests(unittest.TestCase):
    def run_pipeline(self, input_path: str, input_format: str) -> dict[str, object]:
        with tempfile.TemporaryDirectory() as temp_dir:
            workdir = Path(temp_dir)
            result = subprocess.run(
                [
                    sys.executable,
                    "scripts/run_contacts_pipeline_report.py",
                    "--input",
                    input_path,
                    "--format",
                    input_format,
                    "--workdir",
                    str(workdir),
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertIn("Report:", result.stdout)
            report_path = workdir / "pipeline_report.json"
            self.assertTrue(report_path.exists())
            report = json.loads(report_path.read_text(encoding="utf-8"))
            self.assertTrue(all(Path(path).is_absolute() or str(path).startswith(str(workdir)) for path in report["artifacts"].values()))
            for path in report["artifacts"].values():
                self.assertTrue(Path(path).exists())
            return report

    def test_pipeline_report_with_vcf(self) -> None:
        report = self.run_pipeline("fixtures/sample_contacts.vcf", "vcf")
        self.assertEqual(report["input_format"], "vcf")
        self.assertIn("contacts_imported", report)
        self.assertIn("segments_total", report)
        self.assertIn("artifacts", report)
        self.assertEqual(report["segments_final_available"], report["segments_total"])
        self.assertEqual(report["segments_final_missing"], 0)

    def test_pipeline_report_with_csv(self) -> None:
        report = self.run_pipeline("fixtures/sample_contacts.csv", "csv")
        self.assertEqual(report["input_format"], "csv")
        self.assertIn("contacts_imported", report)
        self.assertIn("segments_total", report)
        self.assertIn("artifacts", report)
        self.assertEqual(report["segments_final_available"], report["segments_total"])
        self.assertEqual(report["segments_final_missing"], 0)


if __name__ == "__main__":
    unittest.main()
