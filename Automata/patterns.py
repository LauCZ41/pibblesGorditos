PATTERNS = {
    "FULL_STACK_DEVELOPER": [
        ("Frontend language", ["JAVASCRIPT", "TYPESCRIPT"], True),
        ("Markup and styles", ["HTML", "CSS"], False),
        ("Frontend framework", ["REACT", "ANGULAR", "VUE"], True),
        ("Backend", ["NODE_JS", "DJANGO", "SPRING_BOOT", "FLASK", "FASTAPI"], True),
        ("REST API", ["REST_API"], False),
        ("Database", ["SQL", "NOSQL", "POSTGRESQL", "MYSQL", "MONGODB"], True),
        ("Version control", ["GIT"], True),
    ],
    "MACHINE_LEARNING_ENGINEER": [
        ("Language", ["PYTHON"], True),
        ("Data processing", ["PANDAS", "NUMPY"], True),
        ("Machine learning", ["SCIKIT_LEARN", "TENSORFLOW", "PYTORCH", "MACHINE_LEARNING"], True),
        ("SQL database", ["SQL", "POSTGRESQL", "MYSQL"], True),
        ("NoSQL database", ["MONGODB", "NOSQL"], False),
        ("Version control", ["GIT"], True),
    ],
    "CYBERSECURITY_ANALYST": [
        ("Operating systems", ["LINUX", "KALI_LINUX"], True),
        ("Scripting", ["PYTHON", "BASH", "POWERSHELL"], True),
        ("Network analysis", ["WIRESHARK", "NMAP", "SNORT"], True),
        ("Pentesting and scanning", ["BURP_SUITE", "METASPLOIT", "NESSUS"], False),
        ("Monitoring", ["SPLUNK", "SIEM"], True),
        ("Standards", ["OWASP"], False),
    ],
    "DATA_ENGINEER": [
        ("Languages", ["PYTHON", "SQL", "SCALA"], True),
        ("Storage", ["POSTGRESQL", "MYSQL", "MONGODB", "SNOWFLAKE", "BIGQUERY", "REDSHIFT"], True),
        ("Processing", ["SPARK", "HADOOP", "KAFKA"], True),
        ("Orchestration", ["AIRFLOW", "DBT", "ETL"], True),
        ("Cloud", ["AWS"], False),
        ("Containers", ["DOCKER"], False),
        ("Version control", ["GIT"], True),
    ],
}


def pattern_alphabet(steps):
    return [qualification for _, qualifications, _ in steps for qualification in qualifications]
