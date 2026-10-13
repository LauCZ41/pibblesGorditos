from .automaton_builder import build_profile_automaton
from .patterns import PATTERNS, pattern_alphabet

AUTOMATA = {profile: build_profile_automaton(steps) for profile, steps in PATTERNS.items()}


def classify(sorted_by_profile):
    result = {}
    for profile, steps in PATTERNS.items():
        alphabet = set(pattern_alphabet(steps))
        sequence = [q for q in sorted_by_profile[profile] if q in alphabet]
        result[profile] = AUTOMATA[profile].accepts(sequence)
    return result
