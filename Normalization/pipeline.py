"""Stage 2 pipeline: raw skills (Stage 1) -> canonical, sorted qualifications.

    raw skills --(whitespace cleanup)--> tokens
               --(transducer)----------> canonical names / unrecognized
               --(profile ordering)----> sorted sequences for Stage 3

"""

from dataclasses import dataclass, field

from .builder import build_union_spec, to_word
from .ordering import PROFILES, sort_for_profile


def reference_translator(spec):
    """Translator backed by the pure-Python simulation (used by tests)."""

    def translate(token):
        output = spec.translate(to_word(token))
        return "".join(output) if output is not None else None

    return translate


def pyformlang_translator(spec=None):
    """Translator backed by pyformlang (the implementation used in production)."""
    try:
        from .fst import PyformlangTransducer
    except ImportError as error:  # pragma: no cover - depends on the environment
        raise ImportError(
            "pyformlang is required for Stage 2: pip install -r requirements.txt"
        ) from error
    return PyformlangTransducer(spec or build_union_spec()).translate


def clean_token(raw):
    """Trim and collapse runs of whitespace ('Tensor   Flow ' -> 'Tensor Flow')."""
    return " ".join(raw.split())


@dataclass
class NormalizationResult:
    # (raw skill, canonical name or None), in the order of the résumé
    mapping: list = field(default_factory=list)

    @property
    def normalized(self):
        """Canonical names in order of appearance, without duplicates."""
        seen, result = set(), []
        for _, canonical in self.mapping:
            if canonical is not None and canonical not in seen:
                seen.add(canonical)
                result.append(canonical)
        return result

    @property
    def unrecognized(self):
        """Raw skills rejected by the transducer."""
        return [raw for raw, canonical in self.mapping if canonical is None]


class SkillNormalizer:
    def __init__(self, translator=None, profiles=None):
        self.translate = translator or pyformlang_translator()
        self.profiles = PROFILES if profiles is None else profiles

    def normalize(self, raw_skills):
        result = NormalizationResult()
        for raw in raw_skills:
            token = clean_token(raw)
            if not token:
                continue
            result.mapping.append((raw, self.translate(token)))
        return result

    def sorted_by_profile(self, normalized):
        """{profile: canonical qualifications in that profile's order}."""
        return {
            profile: sort_for_profile(normalized, profile, self.profiles)
            for profile in self.profiles
        }
