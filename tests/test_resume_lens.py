import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from normalize_resume import SAMPLES
from resume_lens import analyze, format_report


class ResumeLensTests(unittest.TestCase):
    def test_analyze_returns_the_profiles_of_a_sample_resume(self):
        result = analyze(SAMPLES["Wednesday Addams"])
        self.assertEqual(result["qualifications"], ["JAVASCRIPT", "REACT", "NODE_JS", "POSTGRESQL", "GIT"])
        self.assertEqual([p for p, ok in result["profiles"].items() if ok], ["FULL_STACK_DEVELOPER"])

    def test_report_lists_every_profile(self):
        report = format_report(analyze(SAMPLES["Wednesday Addams"]))
        self.assertIn("FULL_STACK_DEVELOPER: ACCEPTED", report)
        self.assertIn("DATA_ENGINEER: REJECTED", report)

    def test_resume_without_skills_is_rejected_everywhere(self):
        result = analyze("Just a name and nothing else.")
        self.assertEqual(result["qualifications"], [])
        self.assertFalse(any(result["profiles"].values()))


if __name__ == "__main__":
    unittest.main()
