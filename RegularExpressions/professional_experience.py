import re


def professional_experience(text):
    r"""
    #  Professional experience pattern
    # [A-Z][A-Za-z\s]+?         the job title, starts with a capital letter
    # at                        the literal word connecting title and company
    # [A-Z][A-Za-z0-9\s&.,]+?   the company name, also starts with a capital letter
    # \(                        the opening parenthesis
    # \d{4}                     the start year
    # [-–]                      a dash, short or long
    # \d{4}|Present             the end year, or the word "Present" if still working there
    # \)                        the closing parenthesis
    """
    pattern = r'([A-Z][A-Za-z\s]+?) at ([A-Z][A-Za-z0-9\s&.,]+?)\s*\((\d{4})\s*[-–]\s*(\d{4}|Present)\)'
    matches = re.findall(pattern, text)

    experience = []
    for role, company, start, end in matches:
        experience.append({
            "role": role.strip(),
            "company": company.strip(),
            "start_year": start.strip(),
            "end_year": end.strip(),
        })
    return experience
experience_tests = [
    (
        "Professional Experience: Software Engineer at Addams Family "
        "Enterprises (2020-2022), Data Analyst at Nevermore Labs (2022-Present).",
        [
            {"role": "Software Engineer", "company": "Addams Family Enterprises",
             "start_year": "2020", "end_year": "2022"},
            {"role": "Data Analyst", "company": "Nevermore Labs",
             "start_year": "2022", "end_year": "Present"},
        ]
    ),
    (
        "Experience: Web Developer at Oscorp (2018-2019)",
        [
            {"role": "Web Developer", "company": "Oscorp",
             "start_year": "2018", "end_year": "2019"},
        ]
    ),
]

if __name__ == "__main__":
    for data, expected in experience_tests:
        result = professional_experience(data)
        print(f"Input: {data[:40]}...")
        print(f"Result: {result}")
        assert result == expected, f"FAIL: waiting {expected}, obtained {result}"

