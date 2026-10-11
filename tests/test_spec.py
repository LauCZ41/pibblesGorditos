import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Normalization.spec import TransducerSpec


def tiny():
    spec = TransducerSpec("tiny")
    spec.add_transition("q0", "a", "q1")
    spec.add_transition("q1", "b", "q2", ["AB"])
    spec.add_final("q2")
    return spec


class SpecTests(unittest.TestCase):
    def test_components_are_collected(self):
        spec = tiny()
        self.assertEqual(spec.states, {"q0", "q1", "q2"})
        self.assertEqual(spec.input_alphabet, {"a", "b"})
        self.assertEqual(spec.output_alphabet, {"AB"})
        self.assertEqual(spec.finals, {"q2"})
        self.assertEqual(spec.start, "q0")

    def test_translate_accepts_and_outputs(self):
        self.assertEqual(tiny().translate("ab"), ["AB"])

    def test_translate_rejects_unknown_symbol(self):
        self.assertIsNone(tiny().translate("ax"))

    def test_translate_rejects_non_final_state(self):
        self.assertIsNone(tiny().translate("a"))

    def test_empty_word_rejected_when_start_not_final(self):
        self.assertIsNone(tiny().translate(""))

    def test_conflicting_transition_raises(self):
        spec = tiny()
        with self.assertRaises(ValueError):
            spec.add_transition("q0", "a", "q9")

    def test_repeating_identical_transition_is_allowed(self):
        spec = tiny()
        spec.add_transition("q0", "a", "q1")
        self.assertTrue(spec.is_deterministic())


if __name__ == "__main__":
    unittest.main()