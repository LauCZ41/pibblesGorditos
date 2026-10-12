"""
Stage 3 - Classification: which profiles does a resume satisfy?

For every profile: sort the normalized skills with the order of the profile
(end of Stage 2) and run the automaton of the profile on that sequence.
The same function handles the four profiles; only the data changes.
"""

from Profiles.profiles import PROFILES
from Transducers.sorting import sort_for_profile
from Automata.automaton_builder import build_profile_automaton

AUTOMATA = {key: build_profile_automaton(profile) for key, profile in PROFILES.items()}


def missing_requirement(automaton, sequence, profile):
    """
    Explains a rejection: name of the first required group that was not
    satisfied, found by walking the automaton. Returns None if accepted.
    """
    transitions = automaton.to_dict()
    state = automaton.start_state
    for skill in sequence:
        targets = transitions.get(state, {})
        symbol = next((s for s in targets if s.value == skill), None)
        if symbol is None:
            break
        state = targets[symbol]
    if state in automaton.final_states:
        return None
    required = [g["name"] for g in profile["groups"] if g["required"]]
    return required[int(state.value[1:])]      # state "q2" -> third required group


def classify(skills, profiles=PROFILES, automata=AUTOMATA):
    """
    skills: list of canonical skills (output of Stage 2), any order.
    Returns {profile key: {"accepted": bool, "sequence": [...], "missing": str|None}}
    """
    result = {}
    for key, profile in profiles.items():
        sequence = sort_for_profile(skills, profile)
        accepted = automata[key].accepts(sequence)
        result[key] = {
            "accepted": accepted,
            "sequence": sequence,
            "missing": None if accepted else missing_requirement(automata[key], sequence, profile),
        }
    return result
