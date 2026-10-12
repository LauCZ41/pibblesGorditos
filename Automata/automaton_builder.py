

from pyformlang.finite_automaton import DeterministicFiniteAutomaton


def build_profile_automaton(profile):
    dfa = DeterministicFiniteAutomaton()
    current = "q0"
    dfa.add_start_state(current)
    required_count = 0

    for group in profile["groups"]:
        if group["required"]:
            required_count += 1
            next_state = f"q{required_count}"
            for skill in group["tokens"]:
                dfa.add_transition(current, skill, next_state) 
                dfa.add_transition(next_state, skill, next_state)  
            current = next_state
        else:
            for skill in group["tokens"]:
                dfa.add_transition(current, skill, current)     
    dfa.add_final_state(current)
    return dfa
