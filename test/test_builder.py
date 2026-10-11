import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Normalization.builder import (
    build_qualification_specs,
    build_union_spec,
    to_word,
)
from Normalization.catalog import CATALOG, END_MARKER


class UnionTransducerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.union = build_union_spec()

    def test_every_variant_maps_to_its_canonical_name(self):
        for canonical, variants in CATALOG.items():
            for variant in variants:
                self.assertEqual(
                    self.union.translate(to_word(variant)), [canonical], variant
                )

    def test_assignment_examples(self):
        examples = {
            "JS": "JAVASCRIPT", "Javascript": "JAVASCRIPT",
            "React.js": "REACT", "ReactJS": "REACT",
            "NodeJS": "NODE_JS", "Node.js": "NODE_JS",
            "Postgres": "POSTGRESQL", "PostgreSQL": "POSTGRESQL",
            "pandas": "PANDAS",
            "sklearn": "SCIKIT_LEARN", "scikit learn": "SCIKIT_LEARN",
            "Scikit-learn": "SCIKIT_LEARN",
            "Tensor Flow": "TENSORFLOW", "TensorFlow": "TENSORFLOW",
            "Py Torch": "PYTORCH", "PyTorch": "PYTORCH",
        }
        for raw, canonical in examples.items():
            self.assertEqual(self.union.translate(to_word(raw)), [canonical], raw)

    def test_case_insensitive(self):
        for raw in ["javascript", "JAVASCRIPT", "JavaScript", "jAvAsCrIpT"]:
            self.assertEqual(self.union.translate(to_word(raw)), ["JAVASCRIPT"])

    def test_prefix_variants_do_not_clash(self):
        # 'react' is a prefix of 'react.js' / 'reactjs' / 'react js'
        for raw in ["react", "react.js", "reactjs", "react js"]:
            self.assertEqual(self.union.translate(to_word(raw)), ["REACT"])

    def test_unknown_tokens_are_rejected(self):
        for raw in ["rust", "jsx", "reac", "reactt", "", "java"]:
            self.assertIsNone(self.union.translate(to_word(raw)), raw)

    def test_token_without_end_marker_is_rejected(self):
        self.assertIsNone(self.union.translate(list("javascript")))

    def test_deterministic_and_single_final_state(self):
        self.assertTrue(self.union.is_deterministic())
        self.assertEqual(len(self.union.finals), 1)

    def test_output_alphabet_is_the_catalog_names(self):
        self.assertEqual(self.union.output_alphabet, set(CATALOG))

    def test_input_alphabet_contains_end_marker(self):
        self.assertIn(END_MARKER, self.union.input_alphabet)


class PerQualificationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.specs = build_qualification_specs()

    def test_one_transducer_per_qualification(self):
        self.assertEqual(set(self.specs), set(CATALOG))

    def test_each_transducer_accepts_only_its_own_variants(self):
        for canonical, spec in self.specs.items():
            for other, variants in CATALOG.items():
                for variant in variants:
                    result = spec.translate(to_word(variant))
                    if other == canonical:
                        self.assertEqual(result, [canonical])
                    else:
                        self.assertIsNone(result, f"{canonical} accepted {variant}")

    def test_small_machine_shape(self):
        # GIT has one variant 'git': q0 -g-> q1 -i-> q2 -t-> q3 -⊣-> q4
        git = self.specs["GIT"]
        self.assertEqual(len(git.states), 5)
        self.assertEqual(git.finals, {"q4"})
        self.assertEqual(git.start, "q0")


if __name__ == "__main__":
    unittest.main()
