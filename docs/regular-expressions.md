This document contains the explanation of the pattern for each element needed for later analysis

# Technical Skills
```
pattern = r'Technical Skills:\s*(.+?)\.?$'
```

This patterer is used to identify the technical skills of the candidates.
*  \s* = This accepts any whitespace between "Technical Skills:" and the information, it allows having cero o more spaces
*  (.+?) = Any character including dots. The "?" makes it not greedy, that means that it matches the shortest possible string that satisfies the pattern.
*  \.?$ = The string may end with an optional literal dot, and nothing can follow it



# Contact Information
```
email_match = re.search(r'[\w.-]+@[\w.-]+\.\w+', text)
```
Email pattern:
    # [\w.-]+   whatever comes before the @
    # @         the @ symbol
    # [\w.-]+   whatever comes after the @ domain name
    # \.\w+     a dot followed by letters the extension

```
phone_match = re.search(r'(?:\(?\+?\d+\)?[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', text)
```
Phone pattern:
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

```
linkedin_match = re.search(r'linkedin\.com/in/[\w-]+', text, re.IGNORECASE)
```
LinkedIn pattern:
    # linkedin\.com/in/  this part is fixed
    # [\w-]+             after that the username

