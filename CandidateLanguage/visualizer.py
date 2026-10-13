def to_markdown(model):
    contact = model.contact
    lines = [f"# {model.name}", "", "## Contact", ""]
    lines.append(f"- Email: {contact.email}")
    if contact.phone:
        lines.append(f"- Phone: {contact.phone}")
    if contact.linkedin:
        lines.append(f"- LinkedIn: {contact.linkedin}")

    lines += ["", "## Experience", ""]
    lines += [f"- **{job.role}** at {job.company} ({job.start_year} - {job.end_year})"
              for job in model.experience.jobs] or ["- None"]

    lines += ["", "## Education", ""]
    lines += [f"- **{degree.title}** in {degree.field}, {degree.institution} ({degree.year})"
              for degree in model.education.degrees] or ["- None"]

    lines += ["", "## Skills", "", ", ".join(model.skills.names)]

    lines += ["", "## Accepted profiles", ""]
    lines += [f"- {item.profile}" for item in model.classification.accepted] or ["- None"]
    return "\n".join(lines) + "\n"
