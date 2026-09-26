import re

pattern = re.compile(r'Technical Skills: \s*([a-zA-Z0-9_]*)')
#match = re.search(pattern, la, re.IGNORECASE)
#return match.groups() if match else None


test_cases1 = [
  ("alalalalal Technical Skills: python"),
  ("java Technical Skills: JS"),
  ("Technical Skills: JS"),
 ]

# test_cases1 = [
#  "Nombre: Laura",
#  "No no no Nombre:Juan",
# ]


for data in test_cases1:
    match = pattern.search(data)
    if match:
        print(f"Texto: {data}")
        print(f"Capturado: '{match.group(1)}'")
        print()