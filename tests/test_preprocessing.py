"""
Unit Tests for Preprocessing, Chemical Rules, and Unit Normalization.
"""

import unittest
import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "Matskraft_composition"))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "Matskraft_property"))

from composition_rules import is_chemical_component, parse_header_for_component, detect_composition_unit
from unit_normalizer import normalize_unit, extract_unit_from_text
from property_vocab import canonicalize_property

class TestPreprocessingAndRules(unittest.TestCase):

    def test_chemical_components(self):
        self.assertTrue(is_chemical_component("SiO2"))
        self.assertTrue(is_chemical_component("Al2O3"))
        self.assertTrue(is_chemical_component("Ti"))
        self.assertTrue(is_chemical_component("BaTiO3"))
        self.assertFalse(is_chemical_component("Sample_XYZ"))

    def test_header_parsing(self):
        res = parse_header_for_component("SiO2 (wt.%)")
        self.assertIsNotNone(res)
        self.assertEqual(res[0], "SiO2")
        self.assertEqual(res[1], "wt.%")

    def test_unit_normalization(self):
        self.assertEqual(normalize_unit("g/cm3"), "g/cm³")
        self.assertEqual(normalize_unit("mpa"), "MPa")
        self.assertEqual(normalize_unit("w/mk"), "W/m·K")
        self.assertEqual(extract_unit_from_text("Yield Strength (MPa)"), "MPa")

    def test_property_canonicalization(self):
        self.assertEqual(canonicalize_property("Yield Strength (MPa)"), "Yield Strength")
        self.assertEqual(canonicalize_property("HV30"), "Vickers Hardness")
        self.assertEqual(canonicalize_property("Density (g/cm3)"), "Density")

if __name__ == "__main__":
    unittest.main()
