import os
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from Normalization.builder import build_union_spec
from Normalization.pipeline import (
    SkillNormalizer,
    clean_token,
    pyformlang_translator,
    reference_translator,
)
from normalize_resume import SAMPLES, normalize_resume
from resume_extractor import extract_complete_resume_info

try:
    import pyformlang  # noqa: F401

    HAS_PYFORMLANG = True
except ImportError:
    HAS_PYFORMLANG = False


def reference_normalizer():
    return SkillNormalizer(translator=reference_translator(build_union_spec()))


class PipelineTests(unittest.TestCase):
    def setUp(self):
        self.normalizer = reference_normalizer()

    def test_clean_token(self):
        self.assertEqual(clean_token("  Tensor   Flow \n"), "Tensor Flow")

    def test_assignment_sorting_example(self):
        result = self.normalizer.normalize(
            ["Git", "NodeJS", "JS", "Postgres", "React.js"]
        )
        self.assertEqual(
            self.normalizer.sorted_by_profile(result.normalized)["FULL_STACK_DEVELOPER"],
            ["JAVASCRIPT", "REACT", "NODE_JS", "POSTGRESQL", "GIT"],
        )

    def test_duplicates_and_unrecognized(self):
        result = self.normalizer.normalize(["JS", "Javascript", "Figma", "  ", "git"])
        self.assertEqual(result.normalized, ["JAVASCRIPT", "GIT"])
        self.assertEqual(result.unrecognized, ["Figma"])
        self.assertEqual(len(result.mapping), 4)  # blank entry ignored

    def test_irregular_spacing_still_normalizes(self):
        result = self.normalizer.normalize(["Tensor    Flow", " Py Torch "])
        self.assertEqual(result.normalized, ["TENSORFLOW", "PYTORCH"])

    def test_empty_input(self):
        result = self.normalizer.normalize([])
        self.assertEqual(result.normalized, [])
        self.assertEqual(result.unrecognized, [])


class IntegrationWithStage1Tests(unittest.TestCase):
    def setUp(self):
        self.normalizer = reference_normalizer()

    def run_sample(self, name):
        info = extract_complete_resume_info(SAMPLES[name])
        return normalize_resume(info, self.normalizer)

    def test_wednesday_addams(self):
        out = self.run_sample("Wednesday Addams")
        self.assertEqual(out["raw_skills"], ["JS", "React.js", "NodeJS", "Postgres", "Git"])
        self.assertEqual(
            out["sorted_by_profile"]["FULL_STACK_DEVELOPER"],
            ["JAVASCRIPT", "REACT", "NODE_JS", "POSTGRESQL", "GIT"],
        )
        self.assertEqual(out["unrecognized_skills"], [])

    def test_mary_jane_watson(self):
        out = self.run_sample("Mary Jane Watson")
        self.assertEqual(
            out["sorted_by_profile"]["MACHINE_LEARNING_ENGINEER"],
            ["PYTHON", "PANDAS", "NUMPY", "SCIKIT_LEARN", "TENSORFLOW", "SQL", "GIT"],
        )

    def test_resume_without_skills_section(self):
        info = extract_complete_resume_info("Nothing useful here.")
        out = normalize_resume(info, self.normalizer)
        self.assertEqual(out["normalized_skills"], [])
        self.assertEqual(out["sorted_by_profile"]["FULL_STACK_DEVELOPER"], [])


@unittest.skipUnless(HAS_PYFORMLANG, "pyformlang is not installed")
class DefaultPyformlangPipelineTests(unittest.TestCase):
    def test_default_normalizer_uses_pyformlang(self):
        normalizer = SkillNormalizer(translator=pyformlang_translator())
        result = normalizer.normalize(["Git", "NodeJS", "JS", "Postgres", "React.js"])
        self.assertEqual(
            normalizer.sorted_by_profile(result.normalized)["FULL_STACK_DEVELOPER"],
            ["JAVASCRIPT", "REACT", "NODE_JS", "POSTGRESQL", "GIT"],
        )


if __name__ == "__main__":
    unittest.main()