import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from normalize_resume import SAMPLES
from main import analyze, format_report, run


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


class MenuTests(unittest.TestCase):
    def run_menu(self, answers):
        answers = iter(answers)
        output = []
        run(ask=lambda prompt: next(answers), show=output.append)
        return "\n".join(output)

    def test_analyzes_a_resume_from_a_file(self):
        with tempfile.TemporaryDirectory() as folder:
            path = os.path.join(folder, "resume.txt")
            with open(path, "w", encoding="utf-8") as handle:
                handle.write(SAMPLES["Wednesday Addams"])
            output = self.run_menu(["1", path, "0"])
        self.assertIn("FULL_STACK_DEVELOPER: ACCEPTED", output)

    def test_sample_resumes_are_analyzed_with_their_names(self):
        output = self.run_menu(["2", "0"])
        for name in SAMPLES:
            self.assertIn(name, output)
        self.assertEqual(output.count("ACCEPTED"), len(SAMPLES))

    def test_missing_file_and_invalid_option_do_not_stop_the_menu(self):
        output = self.run_menu(["1", "no_such_file.txt", "7", "0"])
        self.assertIn("File not found.", output)
        self.assertIn("Invalid option.", output)


if __name__ == "__main__":
    unittest.main()
