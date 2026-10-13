import os

from Automata.classifier import classify
from CandidateLanguage.generator import build_profile
from CandidateLanguage.parser import validate
from CandidateLanguage.visualizer import to_markdown
from Normalization.pipeline import SkillNormalizer
from normalize_resume import SAMPLES, normalize_resume
from resume_extractor import extract_complete_resume_info

NORMALIZER = SkillNormalizer()
OUTPUT_DIR = "output"


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


def screen(name, text, show, folder):
    result = analyze(text)
    show(format_report(result))
    model, reason = validate(build_profile(name, result))
    if model is None:
        show(f"Profile REJECTED: {reason}")
        return
    markdown = to_markdown(model)
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, name.lower().replace(" ", "_") + ".md")
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(markdown)
    show(f"Profile VALID. Saved to {path}\n\n{markdown}")


def run(ask=input, show=print, folder=OUTPUT_DIR):
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
            screen(ask("Candidate name: ").strip(), text, show, folder)
        elif option == "2":
            for name, text in SAMPLES.items():
                show(f"\n{name}")
                screen(name, text, show, folder)
        else:
            show("Invalid option.")


if __name__ == "__main__":
    run()
