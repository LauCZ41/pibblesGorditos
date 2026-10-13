import os

from textx import metamodel_from_file
from textx.exceptions import TextXSyntaxError

GRAMMAR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "candidate.tx")
metamodel = metamodel_from_file(GRAMMAR, autokwd=True)


def parse(text):
    return metamodel.model_from_str(text)


def validate(text):
    try:
        return parse(text), None
    except TextXSyntaxError as error:
        return None, str(error)
