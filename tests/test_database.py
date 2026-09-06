"""
Unit Tests for SQLite Knowledge Base and Query Engine.
"""

import unittest
import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "app"))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "app/components"))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "scripts"))

from db_utils import get_dashboard_counts, search_knowledge, get_all_papers

class TestDatabase(unittest.TestCase):

    def test_database_connection_and_counts(self):
        counts = get_dashboard_counts()
        self.assertGreaterEqual(counts["papers"], 10)
        self.assertGreaterEqual(counts["tables"], 20)
        self.assertGreaterEqual(counts["materials"], 40)
        self.assertGreaterEqual(counts["properties"], 200)

    def test_search_knowledge(self):
        df_ti = search_knowledge(keyword="Ti-6Al-4V")
        self.assertFalse(df_ti.empty)
        self.assertTrue(any("Yield Strength" in p for p in df_ti["property_name"]))

        df_lfp = search_knowledge(keyword="LiFePO4")
        self.assertFalse(df_lfp.empty)

if __name__ == "__main__":
    unittest.main()
