import re


def contact_information(text):
    r"""
    # Email pattern
    # [\w.-]+   whatever comes before the @
    # @         the @ symbol
    # [\w.-]+   whatever comes after the @ domain name
    # \.\w+     a dot followed by letters the extension

    # Phone pattern
    # \(?       maybe there's an opening parenthesis, it's optional
    # \+?       maybe there's a plus sign, it's optional
    # \d+       one or more digits, the country code
    # \)?       maybe there's a closing parenthesis
    # [-.\s]?   maybe a separator, a dash a dot or a space
    # \(?       maybe there's an opening parenthesis, it's optional
    # \d{3}     exactly 3 digits, the area code
    # \)?       maybe there's a closing parenthesis
    # [-.\s]?   maybe a separator, a dash a dot or a space
    # \d{3}     3 more digits
    # [-.\s]?   another optional separator
    # \d{4}     the last 4 digits

    # LinkedIn pattern
    # linkedin\.com/in/  this part is fixed
    # [\w-]+             after that the username
    """


    email_match = re.search(r'[\w.-]+@[\w.-]+\.\w+', text)
    phone_match = re.search(r'(?:\(?\+?\d+\)?[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', text)
    linkedin_match = re.search(r'linkedin\.com/in/[\w-]+', text, re.IGNORECASE)

    return {
        "email": email_match.group(0) if email_match else None,
        "phone": phone_match.group(0) if phone_match else None,
        "linkedin": linkedin_match.group(0) if linkedin_match else None,
    }

contact_tests = [
    (
        "Wednesday Addams Contact Information: wednesday.addams@nevermore.edu, "
        "(555) 123-4567, linkedin.com/in/wednesdayaddams",
        {"email": "wednesday.addams@nevermore.edu",
         "phone": "(555) 123-4567",
         "linkedin": "linkedin.com/in/wednesdayaddams"}
    ),
    (
        "Peter Parker Contact: peter.parker@dailybugle.com, 212-555-0199",
        {"email": "peter.parker@dailybugle.com",
         "phone": "212-555-0199",
         "linkedin": None}
    ),
]

if __name__ == "__main__":
    for data, expected in contact_tests:
        result = contact_information(data)
        print(f"Entrada: {data[:40]}...")
        print(f"Resultado: {result}")
        assert result == expected, f"Fallo: esperado {expected}, obtenido {result}"

