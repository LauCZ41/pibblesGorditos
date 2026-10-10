import json
from contact_information import contact_information
from academic_qualifications import academic_qualifications
from professional_experience import professional_experience
from technicalSkills import technical_skills, categorization


def extract_complete_resume_info(resume_text):
    contact = contact_information(resume_text)
    academics = academic_qualifications(resume_text)
    experience = professional_experience(resume_text)
    skills = technical_skills(resume_text)
    categorized = categorization(skills)

    extracted_info = {
        "contact_information": contact,
        "academic_qualifications": academics,
        "professional_experience": experience,
        "technical_skills": {
            "raw_skills": skills,  
            "categorized_skills": categorized,
        },
    }

    return extracted_info


def save_resume_to_json(data, filepath="extracted_resume.json"):

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"Data saved to: {filepath}")


if __name__ == "__main__":
    sample_resume = (
        "Wednesday Addams Contact Information: wednesday.addams@nevermore.edu, (555) 123-4567, linkedin.com/in/wednesdayaddams. "
        "Academic Qualifications: Bachelor of Science in Computer Science, Nevermore Academy, 2020; Master of Science in Data Science, Jericho University, 2022. "
        "Professional Experience: Software Engineer at Addams Family Enterprises (2020-2022), Data Analyst at Nevermore Labs (2022-Present). "
        "Technical Skills: JS, React.js, NodeJS, Postgres, Git."
    )

    data = extract_complete_resume_info(sample_resume)
    print(json.dumps(data, indent=4, ensure_ascii=False))
    save_resume_to_json(data, "extracted_resume.json")
