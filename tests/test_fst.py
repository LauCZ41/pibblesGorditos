import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Normalization.builder import build_qualification_specs, build_union_spec
from Normalization.catalog import CATALOG

try:
    from Normalization.fst import PyformlangTransducer

    HAS_PYFORMLANG = True
except ImportError:  # pyformlang is not installed
    HAS_PYFORMLANG = False


@unittest.skipUnless(HAS_PYFORMLANG, "pyformlang is not installed")
class PyformlangTransducerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.spec = build_union_spec()
        cls.union = PyformlangTransducer(cls.spec)

    def test_every_variant_is_normalized(self):
        for canonical, variants in CATALOG.items():
            for variant in variants:
                self.assertEqual(self.union.translate(variant), canonical, variant)

    def test_case_insensitive(self):
        self.assertEqual(self.union.translate("JavaScript"), "JAVASCRIPT")
        self.assertEqual(self.union.translate("POSTGRES"), "POSTGRESQL")

    def test_unknown_token_is_rejected(self):
        self.assertIsNone(self.union.translate("rust"))
        self.assertIsNone(self.union.translate("reac"))

    def test_agrees_with_reference_simulation(self):
        from Normalization.builder import to_word

        probes = ["JS", "ReactJS", "node js", "Tensor Flow", "sklearn",
                  "unknown", "git", "GIT", "pyt", "springboot"]
        for token in probes:
            expected = self.spec.translate(to_word(token))
            expected = "".join(expected) if expected is not None else None
            self.assertEqual(self.union.translate(token), expected, token)

    def test_per_qualification_machines(self):
        for canonical, spec in build_qualification_specs().items():
            machine = PyformlangTransducer(spec)
            for variant in CATALOG[canonical]:
                self.assertEqual(machine.translate(variant), canonical)


if __name__ == "__main__":
    unittest.main()