import os
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from CandidateLanguage.generator import build_profile
from CandidateLanguage.parser import validate
from resume_lens import analyze

DATA = os.path.join(ROOT, "tests", "data")

# file -> (candidate name, must the generated profile be valid?)
RESUMES = {
    "resume_full_stack_with_contact.txt": ("Wednesday Addams", True),
    "resume_data_engineer_with_email_only.txt": ("Juan Rojas", True),
    "resume_without_email.txt": ("Laura Cardenas", False),
    "resume_without_skills_section.txt": ("Mary Jane Watson", False),
}


def generated_profile(file_name):
    name = RESUMES[file_name][0]
    with open(os.path.join(DATA, file_name), encoding="utf-8") as handle:
        return build_profile(name, analyze(handle.read()))


class GeneratorTests(unittest.TestCase):
    def test_each_generated_profile_is_validated_or_rejected(self):
        for file_name, (_, valid) in RESUMES.items():
            with self.subTest(file_name):
                model, reason = validate(generated_profile(file_name))
                self.assertEqual(model is not None, valid)
                self.assertEqual(reason is None, valid)

    def test_valid_profile_keeps_the_extracted_information(self):
        model, _ = validate(generated_profile("resume_full_stack_with_contact.txt"))
        self.assertEqual(model.name, "Wednesday Addams")
        self.assertEqual(model.contact.email, "wednesday.addams@nevermore.edu")
        self.assertEqual(model.experience.jobs[1].end_year, "present")
        self.assertEqual(len(model.education.degrees), 2)
        self.assertEqual(model.skills.names, ["JAVASCRIPT", "REACT", "NODE_JS", "POSTGRESQL", "GIT"])
        self.assertEqual([a.profile for a in model.classification.accepted], ["FULL_STACK_DEVELOPER"])


if __name__ == "__main__":
    unittest.main()
