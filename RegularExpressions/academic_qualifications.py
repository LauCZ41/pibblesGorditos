import re


def academic_qualifications(text):
    r"""
    # Academic qualifications pattern
    # Bachelor Master PhD Associate  the degree is one of these words
    # (of [A-Za-z]+)?                  maybe "of Something" follows like "of Science", it is optional
    # in                                the literal word connecting degree and field
    # [A-Za-z\s]+?                      the field of study, just letters and spaces
    # ,\s*                              a comma, maybe followed by a space
    # [A-Za-z0-9\s.&]+?                 the institution's name
    # ,\s*                              another comma
    # \d{4}                             the year, 4 digits
    """
    pattern = (
        r'((?:Bachelor|Master|PhD|Associate)(?: of [A-Za-z]+)?)'
        r' in ([A-Za-z\s]+?),\s*([A-Za-z0-9\s.&]+?),\s*(\d{4})'
    )
    matches = re.findall(pattern, text)

    qualifications = []
    for degree, field, institution, year in matches:
        qualifications.append({
            "degree": degree.strip(),
            "field": field.strip(),
            "institution": institution.strip(),
            "year": year.strip(),
        })
    return qualifications
academic_tests = [
    (
        "Academic Qualifications: Bachelor of Science in Computer Science, "
        "Nevermore Academy, 2020; Master of Science in Data Science, "
        "Jericho University, 2022.",
        [
            {"degree": "Bachelor of Science", "field": "Computer Science",
             "institution": "Nevermore Academy", "year": "2020"},
            {"degree": "Master of Science", "field": "Data Science",
             "institution": "Jericho University", "year": "2022"},
        ]
    ),
    (
        "Education: PhD in Artificial Intelligence, MIT, 2023",
        [
            {"degree": "PhD", "field": "Artificial Intelligence",
             "institution": "MIT", "year": "2023"},
        ]
    ),
]

if __name__ == "__main__":
    for data, expected in academic_tests:
        result = academic_qualifications(data)
        print(f"Entrada: {data[:40]}...")
        print(f"Resultado: {result}")
        assert result == expected, f"Fallo: esperado {expected}, obtenido {result}"