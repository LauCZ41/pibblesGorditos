from Automata.classifier import classify
from Normalization.pipeline import SkillNormalizer
from normalize_resume import SAMPLES, normalize_resume
from resume_extractor import extract_complete_resume_info

NORMALIZER = SkillNormalizer()


def analyze(text):
    info = extract_complete_resume_info(text)
    normalized = normalize_resume(info, NORMALIZER)
    return {
        "info": info,
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


MENU = "\nResumeLens\n1. Analyze a résumé from a text file\n2. Analyze the sample résumés\n0. Exit"


def run(ask=input, show=print):
    while True:
        show(MENU)
        option = ask("Option: ").strip()
        if option == "0":
            return
        if option == "1":
            path = ask("File path: ").strip()
            try:
                with open(path, encoding="utf-8") as handle:
                    text = handle.read()
            except OSError:
                show("File not found.")
                continue
            show(format_report(analyze(text)))
        elif option == "2":
            for name, text in SAMPLES.items():
                show(f"\n{name}\n{format_report(analyze(text))}")
        else:
            show("Invalid option.")


if __name__ == "__main__":
    run()
