import itertools
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Normalization.ordering import (
    PROFILES,
    group_name_of,
    register_profile,
    sort_for_profile,
    validate_profile,
)


class OrderingTests(unittest.TestCase):
    def test_builtin_profiles_are_valid(self):
        for name, groups in PROFILES.items():
            self.assertTrue(validate_profile(name, groups), name)

    def test_full_stack_example_from_the_assignment(self):
        shuffled = ["GIT", "NODE_JS", "JAVASCRIPT", "POSTGRESQL", "REACT"]
        self.assertEqual(
            sort_for_profile(shuffled, "FULL_STACK_DEVELOPER"),
            ["JAVASCRIPT", "REACT", "NODE_JS", "POSTGRESQL", "GIT"],
        )

    def test_machine_learning_example_from_the_assignment(self):
        shuffled = ["GIT", "POSTGRESQL", "TENSORFLOW", "PANDAS", "PYTHON"]
        self.assertEqual(
            sort_for_profile(shuffled, "MACHINE_LEARNING_ENGINEER"),
            ["PYTHON", "PANDAS", "TENSORFLOW", "POSTGRESQL", "GIT"],
        )

    def test_result_does_not_depend_on_input_order(self):
        base = ["GIT", "REACT", "JAVASCRIPT", "NODE_JS", "SQL"]
        results = {
            tuple(sort_for_profile(p, "FULL_STACK_DEVELOPER"))
            for p in itertools.permutations(base)
        }
        self.assertEqual(len(results), 1)

    def test_duplicates_are_removed(self):
        self.assertEqual(
            sort_for_profile(["JAVASCRIPT", "JAVASCRIPT", "GIT"], "FULL_STACK_DEVELOPER"),
            ["JAVASCRIPT", "GIT"],
        )

    def test_unlisted_qualifications_go_last_alphabetically(self):
        result = sort_for_profile(
            ["DOCKER", "GIT", "AWS", "JAVASCRIPT"], "FULL_STACK_DEVELOPER"
        )
        self.assertEqual(result, ["JAVASCRIPT", "GIT", "AWS", "DOCKER"])

    def test_empty_input(self):
        self.assertEqual(sort_for_profile([], "FULL_STACK_DEVELOPER"), [])

    def test_unknown_profile(self):
        with self.assertRaises(KeyError):
            sort_for_profile(["GIT"], "ASTRONAUT")

    def test_group_names(self):
        self.assertEqual(group_name_of("REACT", "FULL_STACK_DEVELOPER"), "Frontend")
        self.assertEqual(group_name_of("GIT", "FULL_STACK_DEVELOPER"), "Version control")
        self.assertIsNone(group_name_of("DOCKER", "FULL_STACK_DEVELOPER"))

    def test_register_profile_validates_and_adds(self):
        custom = {}
        register_profile("DEVOPS", [("Tools", ["DOCKER", "KUBERNETES"])], custom)
        self.assertEqual(
            sort_for_profile(["KUBERNETES", "DOCKER"], "DEVOPS", custom),
            ["DOCKER", "KUBERNETES"],
        )
        with self.assertRaises(ValueError):
            register_profile("BAD", [("X", ["NOT_A_SKILL"])], custom)
        with self.assertRaises(ValueError):
            register_profile("BAD", [("X", ["GIT"]), ("Y", ["GIT"])], custom)


if __name__ == "__main__":
    unittest.main()
