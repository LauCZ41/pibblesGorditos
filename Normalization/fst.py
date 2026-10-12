"""pyformlang implementation of the Stage 2 transducers.

This is the only module that imports pyformlang. A ``TransducerSpec`` (the
7-tuple) is converted into a ``pyformlang.fst.FST`` and every translation in
the pipeline is executed by ``FST.translate``.
"""

from pyformlang.fst import FST

from .builder import to_word


def to_pyformlang(spec):
    """Convert a TransducerSpec into a pyformlang FST."""
    fst = FST()
    fst.add_start_state(spec.start)
    for state in spec.finals:
        fst.add_final_state(state)
    for (source, symbol), target in spec.delta.items():
        fst.add_transition(source, symbol, target, list(spec.omega[(source, symbol)]))
    return fst


class PyformlangTransducer:
    """Wraps an FST so that a token (string) can be translated directly."""

    def __init__(self, spec):
        self.spec = spec
        self.fst = to_pyformlang(spec)

    def translate(self, token):
        """Return the canonical name for ``token`` or None if it is rejected.

        Raises ValueError if the machine produced several different outputs
        (it never should: the transducers are deterministic).
        """
        outputs = {
            tuple(str(symbol) for symbol in result)
            for result in self.fst.translate(to_word(token))
        }
        if not outputs:
            return None
        if len(outputs) > 1:
            raise ValueError(f"{self.spec.name}: ambiguous translation of {token!r}")
        (output,) = outputs
        return "".join(output)