import re



def technical_skills(text):
    pattern = r'Technical Skills:\s*(.+?)\.?$'
    match = re.search(pattern, text, re.IGNORECASE)
    #return re.findall(pattern, text, re.IGNORECASE)
    if match:
        raw_skills = match.group(1).strip()
        raw_skills = re.sub(r'\.$', '', raw_skills)
        skills_list = [skill.strip() for skill in raw_skills.split(',') if skill.strip()]
        return skills_list
    return []


test_cases1 = [
    (
        "Wednesday Addams 3 years of experience developing web applications. Technical Skills: JS, React.js, NodeJS, Postgres, Git.",
        ["JS", "React.js", "NodeJS", "Postgres", "Git"]
    ),
    (
        "Mary Jane Watson 2 years of experience developing predictive models and data-processing pipelines. Technical Skills: Python, Pandas, NumPy, Scikit-learn, TensorFlow, SQL, Git.",
        ["Python", "Pandas", "NumPy", "Scikit-learn", "TensorFlow", "SQL", "Git"]
    ),
    (
        "java python ruby Technical Skills: JS",
        ["JS"]
    ),
    (
        "Technical Skills: JS",
        ["JS"]
    ),
    (
        "name name name T T Technical Skills:Ruby",
        ["Ruby"]
    ),
]


def categorization(skills_list):
    categories = {
        "programming_languages": [],
        "frameworks_and_libraries": [],
        "databases": [],
        "tools_and_technologies": [],
        "other": [],
    }

    lang_pattern = (
        r"^(?:JS|JavaScript|TypeScript|TS|Python|Java|Ruby|C\+\+|C#|Go|Rust|PHP|HTML|CSS|R)$"
    )
    framework_pattern = r"^(?:React(?:\.js)?|Angular|Vue(?:\.js)?|Node\.?js|Django|Spring Boot|Pandas|NumPy|Scikit-learn|sklearn|TensorFlow|PyTorch|Flask|FastAPI)$"
    db_pattern = r"^(?:Postgres(?:QL)?|SQL|NoSQL|MongoDB|MySQL|SQLite|Oracle)$"
    tool_pattern = r"^(?:Git|Docker|REST APIs?|Kubernetes|AWS|Linux)$"

    for skill in skills_list:
        if re.search(lang_pattern, skill, re.IGNORECASE):
            categories["programming_languages"].append(skill)
        elif re.search(framework_pattern, skill, re.IGNORECASE):
            categories["frameworks_and_libraries"].append(skill)
        elif re.search(db_pattern, skill, re.IGNORECASE):
            categories["databases"].append(skill)
        elif re.search(tool_pattern, skill, re.IGNORECASE):
            categories["tools_and_technologies"].append(skill)
        else:
            categories["other"].append(skill)

    return categories


if __name__ == "__main__":
    for data, expected in test_cases1:
        result = technical_skills(data)
        print(f"Entrada: {data[:40]}...")
        print(f"Resultado: {result}")
        assert result == expected, f"Fallo: esperado {expected}, obtenido {result}"

    test_cases_integration = [
        (
            "Wednesday Addams 3 years of experience developing web applications. Technical Skills: JS, React.js, NodeJS, Postgres, Git.",
            {
                "programming_languages": ["JS"],
                "frameworks_and_libraries": ["React.js", "NodeJS"],
                "databases": ["Postgres"],
                "tools_and_technologies": ["Git"],
                "other": [],
            }
        ),
        (
            "Mary Jane Watson 2 years of experience. Technical Skills: Python, Pandas, NumPy, Scikit-learn, TensorFlow, SQL, Git.",
            {
                "programming_languages": ["Python"],
                "frameworks_and_libraries": ["Pandas", "NumPy", "Scikit-learn", "TensorFlow"],
                "databases": ["SQL"],
                "tools_and_technologies": ["Git"],
                "other": [],
            }
        ),
        (
            "Peter Parker Technical Skills: Python, Docker, Figma.",
            {
                "programming_languages": ["Python"],
                "frameworks_and_libraries": [],
                "databases": [],
                "tools_and_technologies": ["Docker"],
                "other": ["Figma"],
            }
        ),
    ]

    print("technical_skills + categorization")
    for text, expected_categories in test_cases_integration:
        skills = technical_skills(text)
        categories = categorization(skills)
        print(f"Entrada: {text[:40]}...")
        print(f"Habilidades extraídas: {skills}")
        print(f"Categorías: {categories}")
        assert categories == expected_categories, f"Fallo: esperado {expected_categories}, obtenido {categories}"






