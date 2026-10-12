"""Stage 3 - classification: runs the automaton of each profile on the Stage 2 output."""

from .automaton_builder import build_profile_automaton
from .patterns import PATTERNS, pattern_alphabet

AUTOMATA = {profile: build_profile_automaton(steps) for profile, steps in PATTERNS.items()}


def classify(sorted_by_profile):
    """
    sorted_by_profile: {profile: qualifications in the order of the profile}
    (output of SkillNormalizer.sorted_by_profile).
    Returns {profile: True if the pattern is satisfied}.
    """
    result = {}
    for profile, steps in PATTERNS.items():
        alphabet = set(pattern_alphabet(steps))
        sequence = [q for q in sorted_by_profile[profile] if q in alphabet]
        result[profile] = AUTOMATA[profile].accepts(sequence)
    return result
