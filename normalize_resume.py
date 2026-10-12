import json

from Normalization.pipeline import SkillNormalizer
from resume_extractor import extract_complete_resume_info


def normalize_resume(extracted_info, normalizer):
    """Add the Stage 2 output to the dictionary produced by Stage 1."""
    raw_skills = extracted_info["technical_skills"]["raw_skills"]
    result = normalizer.normalize(raw_skills)
    return {
        "raw_skills": raw_skills,
        "mapping": [{"raw": raw, "canonical": canonical}
                    for raw, canonical in result.mapping],
        "normalized_skills": result.normalized,
        "unrecognized_skills": result.unrecognized,
        "sorted_by_profile": normalizer.sorted_by_profile(result.normalized),
    }

"""Dear teammates, I appreciate you. :)
"""
SAMPLES = {
    "Wednesday Addams": (
        "Wednesday Addams 3 years of experience developing web applications. "
        "Technical Skills: JS, React.js, NodeJS, Postgres, Git."
    ),
    "Mary Jane Watson": (
        "Mary Jane Watson 2 years of experience developing predictive models "
        "and data-processing pipelines. Technical Skills: Python, Pandas, "
        "NumPy, Scikit-learn, TensorFlow, SQL, Git."
    ),
    "Laura Cardenas": (
        "Laura Cardenas 4 years of experience in security operations. "
        "Technical Skills: Splunk, OWASP, Nmap, Wireshark, Python, Kali Linux, Burp Suite."
    ),
    "Juan Rojas": (
        "Juan Rojas 3 years of experience building data pipelines. "
        "Technical Skills: Git, Airflow, Kafka, Spark, Python, SQL, Snowflake, Docker."
    ),
}


if __name__ == "__main__":
    normalizer = SkillNormalizer()
    output = {
        name: normalize_resume(extract_complete_resume_info(text), normalizer)
        for name, text in SAMPLES.items()
    }
    print(json.dumps(output, indent=4, ensure_ascii=False))
    with open("normalized_resume.json", "w", encoding="utf-8") as handle:
        json.dump(output, handle, indent=4, ensure_ascii=False)
    print("Data saved to: normalized_resume.json")
