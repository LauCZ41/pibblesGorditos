import itertools
import os
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from Automata.classifier import AUTOMATA, classify
from Automata.patterns import PATTERNS, pattern_alphabet
from Normalization.ordering import PROFILES, sort_for_profile
from Normalization.pipeline import SkillNormalizer
from normalize_resume import SAMPLES, normalize_resume
from resume_extractor import extract_complete_resume_info

FULL_STACK = ["JAVASCRIPT", "REACT", "NODE_JS", "POSTGRESQL", "GIT"]
ML = ["PYTHON", "PANDAS", "TENSORFLOW", "POSTGRESQL", "GIT"]


def accepted(qualifications):
    sorted_by_profile = {p: sort_for_profile(qualifications, p) for p in PROFILES}
    return {p for p, ok in classify(sorted_by_profile).items() if ok}


class AutomatonTests(unittest.TestCase):
    def test_every_automaton_is_a_dfa_over_its_pattern_alphabet(self):
        for profile, steps in PATTERNS.items():
            automaton = AUTOMATA[profile]
            required = sum(1 for _, _, is_required in steps if is_required)
            self.assertTrue(automaton.is_deterministic(), profile)
            self.assertEqual(len(automaton.states), required + 1, profile)
            self.assertEqual(
                {s.value for s in automaton.symbols}, set(pattern_alphabet(steps)), profile
            )


class ClassificationTests(unittest.TestCase):
    def test_examples_from_the_assignment(self):
        self.assertEqual(accepted(ML), {"MACHINE_LEARNING_ENGINEER"})
        self.assertEqual(accepted(FULL_STACK), {"FULL_STACK_DEVELOPER"})

    def test_result_does_not_depend_on_input_order(self):
        for order in itertools.permutations(FULL_STACK):
            self.assertEqual(accepted(list(order)), {"FULL_STACK_DEVELOPER"})

    def test_missing_required_step_is_rejected(self):
        self.assertEqual(accepted(["JAVASCRIPT", "REACT", "POSTGRESQL", "GIT"]), set())

    def test_two_qualifications_of_the_same_step_are_accepted(self):
        self.assertIn("FULL_STACK_DEVELOPER", accepted(FULL_STACK + ["TYPESCRIPT", "ANGULAR"]))

    def test_optional_steps_are_allowed_but_not_needed(self):
        self.assertIn("FULL_STACK_DEVELOPER", accepted(FULL_STACK + ["HTML", "CSS", "REST_API"]))
        self.assertIn("DATA_ENGINEER", accepted(["PYTHON", "POSTGRESQL", "SPARK", "AIRFLOW", "GIT"]))
        self.assertIn("DATA_ENGINEER", accepted(
            ["PYTHON", "POSTGRESQL", "SPARK", "AIRFLOW", "AWS", "DOCKER", "GIT"]))

    def test_qualifications_outside_the_profile_are_ignored(self):
        self.assertIn("FULL_STACK_DEVELOPER", accepted(FULL_STACK + ["DOCKER", "PYTHON", "SPLUNK"]))

    def test_each_sample_resume_satisfies_only_its_own_profile(self):
        expected = {
            "Wednesday Addams": "FULL_STACK_DEVELOPER",
            "Mary Jane Watson": "MACHINE_LEARNING_ENGINEER",
            "Laura Cardenas": "CYBERSECURITY_ANALYST",
            "Juan Rojas": "DATA_ENGINEER",
        }
        normalizer = SkillNormalizer()
        for name, profile in expected.items():
            normalized = normalize_resume(extract_complete_resume_info(SAMPLES[name]), normalizer)
            result = classify(normalized["sorted_by_profile"])
            self.assertEqual({p for p, ok in result.items() if ok}, {profile}, name)


if __name__ == "__main__":
    unittest.main()
