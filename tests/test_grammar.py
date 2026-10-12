import os
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from textx.exceptions import TextXSyntaxError

from CandidateLanguage.parser import parse

DATA = os.path.join(ROOT, "tests", "data")


def read(name):
    with open(os.path.join(DATA, name), encoding="utf-8") as handle:
        return handle.read()


class GrammarTests(unittest.TestCase):
    def test_valid_profile_is_parsed_into_objects(self):
        model = parse(read("valid_full_stack_developer.cand"))
        self.assertEqual(model.name, "Wednesday Addams")
        self.assertEqual(model.contact.email, "wednesday.addams@nevermore.edu")
        self.assertEqual([j.company for j in model.experience.jobs],
                         ["Addams Family Enterprises", "Nevermore Labs"])
        self.assertEqual(model.experience.jobs[1].end_year, "present")
        self.assertEqual(len(model.education.degrees), 2)
        self.assertEqual(model.skills.names, ["JAVASCRIPT", "REACT", "NODE_JS", "POSTGRESQL", "GIT"])
        self.assertEqual([a.profile for a in model.classification.accepted], ["FULL_STACK_DEVELOPER"])

    def test_optional_and_repeated_parts_may_be_absent(self):
        model = parse(read("valid_minimal_profile.cand"))
        self.assertIsNone(model.contact.phone)
        self.assertEqual(model.experience.jobs, [])
        self.assertEqual(model.classification.accepted, [])

    def test_invalid_profiles_are_rejected(self):
        files = sorted(name for name in os.listdir(DATA) if name.startswith("invalid_"))
        self.assertTrue(files)
        for name in files:
            with self.subTest(name):
                with self.assertRaises(TextXSyntaxError):
                    parse(read(name))


if __name__ == "__main__":
    unittest.main()
