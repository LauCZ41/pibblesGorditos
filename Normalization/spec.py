"""Library-independent description of a finite-state transducer.

A transducer is the 7-tuple M = (Q, Σ, Γ, δ, ω, q0, F):

    Q   set of states
    Σ   input alphabet
    Γ   output alphabet
    δ   transition function   Q x Σ -> Q
    ω   output function       Q x Σ -> Γ*   (Mealy style: output on the edge)
    q0  initial state
    F   set of accepting states

``TransducerSpec`` stores exactly these components. It is used to
  * build the pyformlang FST (normalization/pyformlang_fst.py),
  * generate the formal definition and the diagrams for the docs,
  * run a small pure-Python reference simulation that the tests use to
    cross-check the pyformlang implementation.
"""

from dataclasses import dataclass, field


@dataclass
class TransducerSpec:
    name: str
    start: str = "q0"
    states: set = field(default_factory=set)
    finals: set = field(default_factory=set)
    input_alphabet: set = field(default_factory=set)
    output_alphabet: set = field(default_factory=set)
    # (state, input symbol) -> next state
    delta: dict = field(default_factory=dict)
    # (state, input symbol) -> tuple of output symbols (empty tuple = ε)
    omega: dict = field(default_factory=dict)

    def __post_init__(self):
        self.states.add(self.start)

    def add_transition(self, source, symbol, target, output=()):
        """Add the edge source --symbol/output--> target.

        Raises ValueError if (source, symbol) already has a different edge,
        which would make the transducer nondeterministic.
        """
        output = tuple(output)
        key = (source, symbol)
        if key in self.delta and (
            self.delta[key] != target or self.omega[key] != output
        ):
            raise ValueError(f"{self.name}: conflicting transition for {key}")
        self.states.update((source, target))
        self.input_alphabet.add(symbol)
        self.output_alphabet.update(output)
        self.delta[key] = target
        self.omega[key] = output

    def add_final(self, state):
        self.states.add(state)
        self.finals.add(state)

    def is_deterministic(self):
        # delta is a dict keyed by (state, symbol), so this holds by
        # construction; kept as an explicit, testable statement.
        return len(self.delta) == len(self.omega)

    def translate(self, word):
        """Reference simulation. Returns the output list, or None if rejected."""
        state = self.start
        output = []
        for symbol in word:
            key = (state, symbol)
            if key not in self.delta:
                return None
            output.extend(self.omega[key])
            state = self.delta[key]
        return output if state in self.finals else None
