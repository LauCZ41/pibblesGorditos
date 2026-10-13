from pyformlang.finite_automaton import DeterministicFiniteAutomaton


def build_profile_automaton(steps):
    dfa = DeterministicFiniteAutomaton()
    current = "q0"
    dfa.add_start_state(current)
    required = 0
    for _, qualifications, is_required in steps:
        if is_required:
            required += 1
            target = f"q{required}"
            for qualification in qualifications:
                dfa.add_transition(current, qualification, target)
                dfa.add_transition(target, qualification, target)
            current = target
        else:
            for qualification in qualifications:
                dfa.add_transition(current, qualification, current)
    dfa.add_final_state(current)
    return dfa
