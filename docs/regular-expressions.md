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
*  [\w.-]+   whatever comes before the @
*  @         the @ symbol
*  [\w.-]+   whatever comes after the @ domain name
*  \.\w+     a dot followed by letters the extension

```
phone_match = re.search(r'(?:\(?\+?\d+\)?[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', text)
```
Phone pattern:
*   \(?       maybe there's an opening parenthesis, it's optional
*  \+?       maybe there's a plus sign, it's optional
*  \d+       one or more digits, the country code
*  \)?       maybe there's a closing parenthesis
*  [-.\s]?   maybe a separator, a dash a dot or a space
*  \(?       maybe there's an opening parenthesis, it's optional
*  \d{3}     exactly 3 digits, the area code
*  \)?       maybe there's a closing parenthesis
*  [-.\s]?   maybe a separator, a dash a dot or a space
     \d{3}     3 more digits
     [-.\s]?   another optional separator
     \d{4}     the last 4 digits

```
linkedin_match = re.search(r'linkedin\.com/in/[\w-]+', text, re.IGNORECASE)
```
LinkedIn pattern:
*  linkedin\.com/in/  this part is fixed
*  [\w-]+             after that the username


# Academic Qualifications
```
pattern = (
        r'((?:Bachelor|Master|PhD|Associate)(?: of [A-Za-z]+)?)'
        r' in ([A-Za-z\s]+?),\s*([A-Za-z0-9\s.&]+?),\s*(\d{4})'
    )
```
Academic qualifications pattern:
*  Bachelor Master PhD Associate  the degree is one of these words
*  (of [A-Za-z]+)?                  maybe "of Something" follows like "of Science", it is optional
*  in                                the literal word connecting degree and field
*  [A-Za-z\s]+?                      the field of study, just letters and spaces
*   ,\s*                              a comma, maybe followed by a space
*   [A-Za-z0-9\s.&]+?                 the institution's name
*   ,\s*                              another comma
*  \d{4}                             the year, 4 digits


# Professional Experience 
```
pattern = r'([A-Z][A-Za-z\s]+?) at ([A-Z][A-Za-z0-9\s&.,]+?)\s*\((\d{4})\s*[-–]\s*(\d{4}|Present)\)'
```
 Professional experience pattern:
*  [A-Z][A-Za-z\s]+?         the job title, starts with a capital letter
*  at                        the literal word connecting title and company
*  [A-Z][A-Za-z0-9\s&.,]+?   the company name, also starts with a capital letter
*  \(                        the opening parenthesis
*   \d{4}                     the start year
*   [-–]                      a dash, short or long
*   \d{4}|Present             the end year, or the word "Present" if still working there
*   \)                        the closing parenthesis

