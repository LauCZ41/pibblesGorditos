import os

from textx import metamodel_from_file
from textx.exceptions import TextXSyntaxError

GRAMMAR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "candidate.tx")
metamodel = metamodel_from_file(GRAMMAR, autokwd=True)


def parse(text):
    """Parses a candidate profile. Raises textx.exceptions.TextXSyntaxError if it is invalid."""
    return metamodel.model_from_str(text)


def validate(text):
    """Returns (model, None) if the profile is valid, or (None, reason) if it is rejected."""
    try:
        return parse(text), None
    except TextXSyntaxError as error:
        return None, str(error)
