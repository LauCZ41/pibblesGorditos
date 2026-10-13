def quote(text):
    return '"' + text.replace('"', "'") + '"'


def build_profile(name, result):
    info = result["info"]
    lines = [f"candidate {quote(name)} {{", "  contact {"]
    for field in ("email", "phone", "linkedin"):
        value = info["contact_information"][field]
        if value:
            lines.append(f"    {field}: {value}")
    lines += ["  }", "  experience {"]
    for job in info["professional_experience"]:
        end = job["end_year"].lower() if job["end_year"] == "Present" else job["end_year"]
        lines.append(f"    {quote(job['role'])} at {quote(job['company'])} "
                     f"from {job['start_year']} to {end}")
    lines += ["  }", "  education {"]
    for degree in info["academic_qualifications"]:
        lines.append(f"    {quote(degree['degree'])} in {quote(degree['field'])} "
                     f"at {quote(degree['institution'])} year {degree['year']}")
    lines += ["  }", "  skills: " + ", ".join(result["qualifications"]), "  classification {"]
    for profile, accepted in result["profiles"].items():
        if accepted:
            lines.append(f"    {profile} accepted")
    lines += ["  }", "}"]
    return "\n".join(lines) + "\n"
