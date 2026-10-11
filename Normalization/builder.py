"""Build transducer specifications from the qualification catalog.

Construction (a prefix tree, i.e. a trie, over characters):

* every distinct prefix of a variant is a state; the empty prefix is q0;
* reading a character moves to the state of the longer prefix and outputs
  nothing (ε). Both lower and upper case are accepted, which makes the
  transducer case-insensitive without a preprocessing step;
* every token is followed by the end marker ⊣. From the state of a complete
  variant, reading ⊣ goes to the single accepting state and outputs the
  canonical name as one symbol of the output alphabet Γ.

Emitting the output on ⊣ (instead of on the last letter) avoids a clash when
one variant is a prefix of another, e.g. ``react`` and ``react.js``.

Two kinds of machines are built:

* one transducer per canonical qualification (small, used for the formal
  definitions and diagrams);
* one union transducer for the whole catalog (used by the pipeline).
"""

from .catalog import CATALOG, END_MARKER, validate_catalog
from .spec import TransducerSpec


def to_word(token):
    """Input word for a transducer: the characters of the token plus ⊣."""
    return list(token) + [END_MARKER]


def _build_trie(name, entries):
    """entries: list of (variant, canonical). Returns a TransducerSpec."""
    prefixes = {""}
    for variant, _ in entries:
        for i in range(1, len(variant) + 1):
            prefixes.add(variant[:i])

    # Deterministic state names: shorter prefixes first, then alphabetical.
    ordered = sorted(prefixes, key=lambda p: (len(p), p))
    state_of = {p: f"q{i}" for i, p in enumerate(ordered)}
    final_state = f"q{len(ordered)}"

    spec = TransducerSpec(name=name, start=state_of[""])
    for prefix in ordered[1:]:
        char = prefix[-1]
        source, target = state_of[prefix[:-1]], state_of[prefix]
        for symbol in sorted({char, char.upper()}):
            spec.add_transition(source, symbol, target)

    for variant, canonical in entries:
        spec.add_transition(state_of[variant], END_MARKER, final_state, [canonical])
    spec.add_final(final_state)
    return spec


def build_qualification_specs(catalog=None):
    """One transducer per canonical qualification: {canonical: spec}."""
    catalog = CATALOG if catalog is None else catalog
    validate_catalog(catalog)
    return {
        canonical: _build_trie(
            f"M_{canonical}", [(variant, canonical) for variant in variants]
        )
        for canonical, variants in catalog.items()
    }


def build_union_spec(catalog=None):
    """A single transducer recognizing every variant of every qualification."""
    catalog = CATALOG if catalog is None else catalog
    validate_catalog(catalog)
    entries = [
        (variant, canonical)
        for canonical, variants in catalog.items()
        for variant in variants
    ]
    return _build_trie("M_NORMALIZER", entries)