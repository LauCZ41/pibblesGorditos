from .catalog import CATALOG
PROFILES = {
    "FULL_STACK_DEVELOPER": [
        ("Frontend", ["JAVASCRIPT", "TYPESCRIPT", "HTML", "CSS",
                      "REACT", "ANGULAR", "VUE"]),
        ("Backend", ["NODE_JS", "DJANGO", "SPRING_BOOT", "FLASK",
                     "FASTAPI", "REST_API"]),
        ("Database", ["SQL", "NOSQL", "POSTGRESQL", "MYSQL", "MONGODB"]),
        ("Version control", ["GIT"]),
    ],
    "MACHINE_LEARNING_ENGINEER": [
        ("Language", ["PYTHON"]),
        ("Data processing", ["PANDAS", "NUMPY"]),
        ("Machine learning", ["SCIKIT_LEARN", "TENSORFLOW", "PYTORCH",
                              "MACHINE_LEARNING"]),
        ("Database", ["SQL", "POSTGRESQL", "MYSQL", "MONGODB", "NOSQL"]),
        ("Version control", ["GIT"]),
    ],
     "CYBERSECURITY_ANALYST": [
        ("Operating systems", ["LINUX", "KALI_LINUX"]),
        ("Scripting", ["PYTHON", "BASH", "POWERSHELL"]),
        ("Network analysis", ["WIRESHARK", "NMAP", "SNORT"]),
        ("Pentesting and scanning", ["BURP_SUITE", "METASPLOIT", "NESSUS"]),
        ("Monitoring", ["SPLUNK", "SIEM"]),
        ("Standards", ["OWASP"]),
    ],
    "DATA_ENGINEER": [
        ("Languages", ["PYTHON", "SQL", "SCALA"]),
        ("Storage", ["POSTGRESQL", "MYSQL", "MONGODB", "SNOWFLAKE", "BIGQUERY", "REDSHIFT"]),
        ("Processing", ["SPARK", "HADOOP", "KAFKA"]),
        ("Orchestration", ["AIRFLOW", "DBT", "ETL"]),
        ("Cloud", ["AWS"]),
        ("Containers", ["DOCKER"]),
        ("Version control", ["GIT"]),
    ],
}


def validate_profile(name, groups, catalog=None):
    """Every listed qualification must exist in the catalog and appear once."""
    catalog = CATALOG if catalog is None else catalog
    seen = set()
    for group_name, qualifications in groups:
        for qualification in qualifications:
            if qualification not in catalog:
                raise ValueError(
                    f"{name}/{group_name}: unknown qualification {qualification}"
                )
            if qualification in seen:
                raise ValueError(f"{name}: {qualification} is listed twice")
            seen.add(qualification)
    return True


def register_profile(name, groups, profiles=None):
    """Add a profile (used for the team's two additional profiles)."""
    profiles = PROFILES if profiles is None else profiles
    validate_profile(name, groups)
    profiles[name] = groups


def _position_table(groups):
    return {
        qualification: (group_index, item_index)
        for group_index, (_, items) in enumerate(groups)
        for item_index, qualification in enumerate(items)
    }


def sort_for_profile(qualifications, profile, profiles=None):
    """Deduplicate and sort normalized qualifications for ``profile``."""
    profiles = PROFILES if profiles is None else profiles
    if profile not in profiles:
        raise KeyError(f"unknown profile {profile!r}")
    positions = _position_table(profiles[profile])
    unique = set(qualifications)
    return sorted(
        unique,
        key=lambda q: (positions.get(q, (len(profiles[profile]), 0)), q),
    )


def group_name_of(qualification, profile, profiles=None):
    """Name of the group a qualification belongs to in a profile (or None)."""
    profiles = PROFILES if profiles is None else profiles
    for group_name, items in profiles[profile]:
        if qualification in items:
            return group_name
    return None
