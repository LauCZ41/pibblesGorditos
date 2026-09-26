import re



def technical_skills(text):
    pattern = r'Technical Skills:\s*(.+?)\.?$'
    return re.findall(pattern, text, re.IGNORECASE)

# pattern = re.compile(r'Technical Skills: \s*([a-zA-Z0-9_]*)')
#match = re.search(pattern, la, re.IGNORECASE)
#return match.groups() if match else None


test_cases1 = [
    ("Wednesday Addams 3 years of experience developing web applications. Technical Skills: JS, React.js, NodeJS, Postgres, Git.",
     ["JS, React.js, NodeJS, Postgres, Git"]),
     ("Mary Jane Watson 2 years of experience developing predictive models and data-processing pipelines. Technical Skills: Python, Pandas, NumPy, Scikit-learn, TensorFlow, SQL, Git.",
     ["Python, Pandas, NumPy, Scikit-learn, TensorFlow, SQL, Git"]),
    ("java python ruby Technical Skills: JS",
     ["JS"]),
    ("Technical Skills: JS",
     ["JS"]),
     ("name name name T T Technical Skills:Ruby",
    ["Ruby"]),
]


for data, expected in test_cases1:
    result = technical_skills(data)
    print(f"Entrada: {data[:40]}...")
    print(f"Resultado: {result}")
    assert result == expected, f"Fallo: esperado {expected}, obtenido {result}"

print("Todos los tests pasaron.")



#FALTA: explain the language or textual pattern recognized by the expression; Y Keep the extracted information in a file or a data structure