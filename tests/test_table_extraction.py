"""
Unit Tests for XML Table Extraction Module.
"""

import unittest
import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "downloading_and_preprocessing"))

from mit_table_extractor import MITTableExtractor

class TestTableExtraction(unittest.TestCase):

    def setUp(self):
        self.extractor = MITTableExtractor()
        self.sample_xml = os.path.join(PROJECT_ROOT, "data/raw_xmls/paper_01_ti_alloys.xml")

    def test_xml_parse_success(self):
        self.assertTrue(os.path.exists(self.sample_xml), "Sample XML file must exist.")
        res = self.extractor.parse_xml_file(self.sample_xml)
        self.assertTrue(res["success"])
        self.assertGreater(len(res["tables"]), 0)
        self.assertEqual(res["metadata"]["doi"], "10.1016/j.msea.2023.144890")

    def test_table_dimensions_and_cleaning(self):
        res = self.extractor.parse_xml_file(self.sample_xml)
        tbl1 = res["tables"][0]
        self.assertIn("Alloy Designation", tbl1["headers"])
        self.assertEqual(tbl1["num_rows"], 5)
        self.assertEqual(tbl1["num_cols"], 8)
        self.assertIsNotNone(tbl1["cleaned_df"])

if __name__ == "__main__":
    unittest.main()
