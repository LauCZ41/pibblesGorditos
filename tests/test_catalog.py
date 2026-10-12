import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Normalization.catalog import CATALOG, END_MARKER, validate_catalog


class CatalogTests(unittest.TestCase):
    def test_default_catalog_is_valid(self):
        self.assertTrue(validate_catalog(CATALOG))

    def test_assignment_examples_are_covered(self):
        expected = {
            "JAVASCRIPT": ["js", "javascript"],
            "REACT": ["react.js", "reactjs"],
            "NODE_JS": ["nodejs", "node.js"],
            "POSTGRESQL": ["postgres", "postgresql"],
            "PANDAS": ["pandas"],
            "SCIKIT_LEARN": ["sklearn", "scikit learn", "scikit-learn"],
            "TENSORFLOW": ["tensor flow", "tensorflow"],
            "PYTORCH": ["py torch", "pytorch"],
        }
        for canonical, variants in expected.items():
            for variant in variants:
                self.assertIn(variant, CATALOG[canonical])

    def test_ambiguous_variant_is_rejected(self):
        bad = {"A": ["x"], "B": ["x"]}
        with self.assertRaises(ValueError):
            validate_catalog(bad)

    def test_upper_case_variant_is_rejected(self):
        with self.assertRaises(ValueError):
            validate_catalog({"A": ["JS"]})

    def test_reserved_marker_is_rejected(self):
        with self.assertRaises(ValueError):
            validate_catalog({"A": ["c" + END_MARKER]})

    def test_empty_entries_are_rejected(self):
        with self.assertRaises(ValueError):
            validate_catalog({"A": []})
        with self.assertRaises(ValueError):
            validate_catalog({"A": [""]})


if __name__ == "__main__":
    unittest.main()
