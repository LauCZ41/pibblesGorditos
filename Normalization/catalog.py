"""Catalog of canonical qualifications and their textual variants.

Each canonical qualification (e.g. ``JAVASCRIPT``) owns a set of variants
(``js``, ``javascript``, ``java script``...). Variants are written in lower
case: the transducers built from this catalog are case-insensitive.

The catalog is the single source of truth for Stage 2. Transducers, docs and
tests are all generated from it, so adding a qualification only requires
adding an entry here.
"""

# Reserved symbol appended to every token; the transducer emits the canonical
# name when it reads it (see normalization/builder.py). '#' is not used
# because skills such as C# contain it.
END_MARKER = "\u22a3"  # ⊣

# canonical name -> variants (lower case, as they may appear in a résumé)
CATALOG = {
    # --- languages -------------------------------------------------------
    "JAVASCRIPT": ["js", "javascript", "java script", "ecmascript"],
    "TYPESCRIPT": ["ts", "typescript", "type script"],
    "PYTHON": ["python", "python3", "python 3"],
    "HTML": ["html", "html5"],
    "CSS": ["css", "css3"],
    # --- frontend frameworks ---------------------------------------------
    "REACT": ["react", "react.js", "reactjs", "react js"],
    "ANGULAR": ["angular", "angular.js", "angularjs", "angular js"],
    "VUE": ["vue", "vue.js", "vuejs", "vue js"],
    # --- backend frameworks ----------------------------------------------
    "NODE_JS": ["node", "node.js", "nodejs", "node js"],
    "DJANGO": ["django"],
    "SPRING_BOOT": ["spring boot", "springboot", "spring-boot"],
    "FLASK": ["flask"],
    "FASTAPI": ["fastapi", "fast api", "fast-api"],
    "REST_API": [
        "rest", "rest api", "rest apis", "rest-api", "rest-apis",
        "restful", "restful api", "restful apis",
    ],
    # --- cybersecurity ---
    "BASH": ["bash", "bash scripting", "shell scripting"],
    "POWERSHELL": ["powershell", "power shell"],
    "KALI_LINUX": ["kali linux", "kali", "kali-linux"],
    "WIRESHARK": ["wireshark"],
    "NMAP": ["nmap"],
    "SNORT": ["snort"],
    "METASPLOIT": ["metasploit", "metasploit framework"],
    "BURP_SUITE": ["burp suite", "burpsuite", "burp"],
    "NESSUS": ["nessus"],
    "SPLUNK": ["splunk"],
    "SIEM": ["siem"],
    "OWASP": ["owasp", "owasp top 10", "owasp top ten"],
    # --- data engineering ---
    "SCALA": ["scala"],
    "SPARK": ["spark", "apache spark", "pyspark"],
    "HADOOP": ["hadoop", "apache hadoop"],
    "KAFKA": ["kafka", "apache kafka"],
    "AIRFLOW": ["airflow", "apache airflow"],
    "DBT": ["dbt", "data build tool"],
    "ETL": ["etl", "etl pipeline", "etl pipelines"],
    "SNOWFLAKE": ["snowflake"],
    "BIGQUERY": ["bigquery", "big query", "google bigquery"],
    "REDSHIFT": ["redshift", "amazon redshift"],
    # --- databases -------------------------------------------------------
    "SQL": ["sql"],
    "NOSQL": ["nosql", "no sql", "no-sql"],
    "POSTGRESQL": ["postgres", "postgresql", "postgre sql"],
    "MYSQL": ["mysql", "my sql"],
    "MONGODB": ["mongo", "mongodb", "mongo db"],
    # --- data / machine learning -----------------------------------------
    "PANDAS": ["pandas"],
    "NUMPY": ["numpy", "num py"],
    "SCIKIT_LEARN": [
        "sklearn", "scikit learn", "scikit-learn", "scikit_learn", "scikitlearn",
    ],
    "TENSORFLOW": ["tensorflow", "tensor flow", "tensor-flow", "tf"],
    "PYTORCH": ["pytorch", "py torch", "py-torch", "torch"],
    "MACHINE_LEARNING": [
        "machine learning", "machine-learning", "ml",
        "machine learning models", "machine-learning models",
    ],
    # --- tools -----------------------------------------------------------
    "GIT": ["git"],
    "DOCKER": ["docker"],
    "KUBERNETES": ["kubernetes", "k8s"],
    "AWS": ["aws", "amazon web services"],
    "LINUX": ["linux"],
}

def validate_catalog(catalog):
    """Check that a catalog defines a deterministic normalization.

    A variant that belongs to two canonical names would make the transducer
    ambiguous (one input, two possible outputs), so it is rejected. Variants
    must also be non-empty, lower case and free of the reserved end marker.

    Raises ValueError describing the first problem found.
    """
    seen = {}
    for canonical, variants in catalog.items():
        if not variants:
            raise ValueError(f"{canonical}: has no variants")
        for variant in variants:
            if not variant:
                raise ValueError(f"{canonical}: empty variant")
            if variant != variant.lower():
                raise ValueError(
                    f"{canonical}: variant {variant!r} must be lower case "
                    "(transducers are case-insensitive)"
                )
            if END_MARKER in variant:
                raise ValueError(
                    f"{canonical}: variant {variant!r} uses the reserved "
                    "end marker"
                )
            if variant in seen and seen[variant] != canonical:
                raise ValueError(
                    f"variant {variant!r} is ambiguous: it maps to both "
                    f"{seen[variant]} and {canonical}"
                )
            seen[variant] = canonical
    return True

