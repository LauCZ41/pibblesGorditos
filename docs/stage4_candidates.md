# Stage 4 — Candidate Profile Language (Context-Free Grammar with textX)

## 1. Problem and Objective

Input: the structured information produced across the previous stages:
- Candidate contact info, academic background, and professional experience (Stage 1).
- Canonical qualifications (Stage 2).
- Profile classification results (`ACCEPTED` / `REJECTED`) (Stage 3).

Output: a validated, structured candidate specification conforming to a formally defined Domain-Specific Language (DSL).

The grammar defines how candidate data must be structurally organized and ensures syntax consistency before visualization.

---

## 2. Grammar in EBNF

Below is the formal Context-Free Grammar expressed in Extended Backus-Naur Form (EBNF):

```ebnf
Candidate         ::= 'candidate' STRING '{'
                        Contact
                        Experience
                        Education
                        Skills
                        Classification
                      '}' ;

Contact           ::= 'contact' '{'
                        'email' ':' EMAIL
                        [ 'phone' ':' PHONE ]
                        [ 'linkedin' ':' LINKEDIN ]
                      '}' ;

Experience        ::= 'experience' '{' { Job }* '}' ;

Job               ::= STRING 'at' STRING 'from' YEAR 'to' EndYear ;

Education         ::= 'education' '{' { Degree }* '}' ;

Degree            ::= STRING 'in' STRING 'at' STRING 'year' YEAR ;

Skills            ::= 'skills' ':' SKILL { ',' SKILL }* ;

Classification    ::= 'classification' '{' { AcceptedProfile }* '}' ;

AcceptedProfile   ::= PROFILE 'accepted' ;

EndYear           ::= YEAR | 'present' ;
```

---

## 3. Terminals and Non-Terminals

### Non-Terminals ($V_N$)
* `Candidate`: Root symbol representing the complete candidate profile.
* `Contact`: Contact information block.
* `Experience`: Block containing zero or more past jobs.
* `Job`: Single professional role record.
* `Education`: Block containing zero or more academic degrees.
* `Degree`: Single educational credential record.
* `Skills`: List of normalized technical competencies.
* `Classification`: Block containing the accepted professional profiles.
* `AcceptedProfile`: Record indicating an accepted profile.
* `EndYear`: End year for a job (either a 4-digit year or the literal `'present'`).

### Terminals ($V_T$)
* **Keywords & Delimiters:**
  `'candidate'`, `'{'`, `'}'`, `'contact'`, `'email'`, `':'`, `'phone'`, `'linkedin'`, `'experience'`, `'at'`, `'from'`, `'to'`, `'education'`, `'in'`, `'year'`, `'skills'`, `','`, `'classification'`, `'accepted'`, `'present'`.
* **Profiles (`PROFILE`):**
  `'FULL_STACK_DEVELOPER'`, `'MACHINE_LEARNING_ENGINEER'`, `'CYBERSECURITY_ANALYST'`, `'DATA_ENGINEER'`.
* **Lexical Tokens (Regular Expressions):**
  * `STRING`: Double-quoted text string (`"..."`).
  * `EMAIL`: `/[\w.-]+@[\w.-]+\.\w+/`
  * `PHONE`: `/(?:\(?\+?\d+\)?[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}/`
  * `LINKEDIN`: `/linkedin\.com\/in\/[\w-]+/`
  * `YEAR`: `/\d{4}(?!\d)/` (strictly 4 digits)
  * `SKILL`: `/[A-Z][A-Z0-9_]*/` (uppercase canonical identifier)

---

## 4. Modeling Decisions

| Decision | Reason |
|---|---|
| Fixed section order | Enforces a consistent, predictable structure (`contact` $\to$ `experience` $\to$ `education` $\to$ `skills` $\to$ `classification`). |
| Repetitions allowed (`*`) | A candidate may have zero, one, or multiple jobs, degrees, or accepted profiles. |
| Mandatory email, optional phone/LinkedIn | Every valid candidate requires at least one direct contact method (email); secondary links are optional. |
| Uppercase pattern for `SKILL` | Enforces that only canonical normalized skills (from Stage 2) are admitted, rejecting raw lowercase words. |
| Strict 4-digit pattern for `YEAR` | Prevents malformed dates (such as 3-digit or 5-digit inputs). |
| Finite set for `PROFILE` | Restricts classification outcomes to the four recognized professional roles. |

---

## 5. Example of Valid Candidate Profile

```cand
candidate "Wednesday Addams" {
  contact {
    email: wednesday.addams@nevermore.edu
    phone: (555) 123-4567
    linkedin: linkedin.com/in/wednesdayaddams
  }
  experience {
    "Software Engineer" at "Addams Family Enterprises" from 2020 to 2022
    "Data Analyst" at "Nevermore Labs" from 2022 to present
  }
  education {
    "Bachelor of Science" in "Computer Science" at "Nevermore Academy" year 2020
    "Master of Science" in "Data Science" at "Jericho University" year 2022
  }
  skills: JAVASCRIPT, REACT, NODE_JS, POSTGRESQL, GIT
  classification {
    FULL_STACK_DEVELOPER accepted
  }
}
```

---

## 6. Implementation and Validation

| File | Content |
|---|---|
| `CandidateLanguage/candidate.tx` | Context-free grammar definition in textX syntax |
| `CandidateLanguage/parser.py` | Metamodel loading and `parse(text)` function |
| `tests/test_grammar.py` | Unit tests for valid parsing and syntax error rejection |
| `tests/data/` | Test suite with valid profiles and invalid cases |

### Lexical and Syntactic Rejection Rules

The parser raises `TextXSyntaxError` when input violates the language rules:
* Missing mandatory sections or out-of-order blocks.
* Emails without `@` or invalid formats (`invalid_email_without_at.cand`).
* Non-canonical skills in lowercase (`invalid_skill_in_lowercase.cand`).
* Years with fewer or more than 4 digits (`invalid_year_3_digits.cand`, `invalid_year_5_digits.cand`).
* Unrecognized profile names outside the four supported roles (`invalid_unknown_profile.cand`).
