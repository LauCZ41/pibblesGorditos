import os
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from CandidateLanguage.parser import parse
from CandidateLanguage.visualizer import to_markdown


def markdown_of(file_name):
    with open(os.path.join(ROOT, "tests", "data", file_name), encoding="utf-8") as handle:
        return to_markdown(parse(handle.read()))


class VisualizerTests(unittest.TestCase):
    def test_full_profile_shows_every_section(self):
        markdown = markdown_of("valid_full_stack_developer.cand")
        self.assertIn("# Wednesday Addams", markdown)
        self.assertIn("- Email: wednesday.addams@nevermore.edu", markdown)
        self.assertIn("- **Data Analyst** at Nevermore Labs (2022 - present)", markdown)
        self.assertIn("- **Master of Science** in Data Science, Jericho University (2022)", markdown)
        self.assertIn("JAVASCRIPT, REACT, NODE_JS, POSTGRESQL, GIT", markdown)
        self.assertIn("- FULL_STACK_DEVELOPER", markdown)

    def test_empty_sections_and_missing_optional_contact(self):
        markdown = markdown_of("valid_minimal_profile.cand")
        self.assertNotIn("Phone", markdown)
        self.assertNotIn("LinkedIn", markdown)
        self.assertEqual(markdown.count("- None"), 3)


if __name__ == "__main__":
    unittest.main()
