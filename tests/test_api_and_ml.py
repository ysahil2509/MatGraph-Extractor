"""
Unit Tests for Machine Learning Property Predictor and FastAPI Endpoints.
"""

import unittest
import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "models"))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "app"))

from train_property_predictor import MaterialPropertyPredictor

class TestMLAndAPI(unittest.TestCase):

    def setUp(self):
        self.predictor = MaterialPropertyPredictor()
        # Train or load
        self.predictor.train()

    def test_ml_prediction_yield_strength(self):
        comp = {"Ti": 90.0, "Al": 6.0, "V": 4.0}
        res = self.predictor.predict(comp, "Yield Strength")
        self.assertNotIn("error", res)
        self.assertGreater(res["predicted_value"], 500.0)
        self.assertIn("confidence_lower", res)
        self.assertIn("confidence_upper", res)

    def test_ml_prediction_density(self):
        comp = {"Ti": 90.0, "Al": 6.0, "V": 4.0}
        res = self.predictor.predict(comp, "Density")
        self.assertNotIn("error", res)
        self.assertGreater(res["predicted_value"], 0.0)

if __name__ == "__main__":
    unittest.main()
