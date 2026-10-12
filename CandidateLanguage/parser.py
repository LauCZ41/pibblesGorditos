import os

from textx import metamodel_from_file

GRAMMAR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "candidate.tx")
metamodel = metamodel_from_file(GRAMMAR, autokwd=True)


def parse(text):
    """Parses a candidate profile. Raises textx.exceptions.TextXSyntaxError if it is invalid."""
    return metamodel.model_from_str(text)
