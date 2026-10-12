from Automata.classifier import classify
from Normalization.pipeline import SkillNormalizer
from normalize_resume import normalize_resume
from resume_extractor import extract_complete_resume_info

NORMALIZER = SkillNormalizer()


def analyze(text):
    """Runs stages 1 to 3 on a résumé text."""
    normalized = normalize_resume(extract_complete_resume_info(text), NORMALIZER)
    return {
        "qualifications": normalized["normalized_skills"],
        "unrecognized": normalized["unrecognized_skills"],
        "profiles": classify(normalized["sorted_by_profile"]),
    }


def format_report(result):
    lines = ["Qualifications: " + (", ".join(result["qualifications"]) or "none")]
    if result["unrecognized"]:
        lines.append("Not recognized: " + ", ".join(result["unrecognized"]))
    for profile, accepted in result["profiles"].items():
        lines.append(f"{profile}: {'ACCEPTED' if accepted else 'REJECTED'}")
    return "\n".join(lines)
