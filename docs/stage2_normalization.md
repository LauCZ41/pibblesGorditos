# Stage 2 — Qualification Normalization

## Goal

Normalize different spellings, abbreviations, and supported variants of the same qualification (e.g., `JS`, `Javascript`, and `javascript`) to a single canonical name (`JAVASCRIPT`). Then, arrange the normalized qualifications in a canonical order defined for the selected professional profile.

This ensures that Stage 3 receives a consistent representation of the candidate's qualifications, independent of the spelling or capitalization used in the résumé.

## Formal Model

Stage 2 uses deterministic finite-state transducers (FSTs) of Mealy type:

\[
M = (Q, \Sigma, \Gamma, \delta, \omega, q_0, F)
\]

The formal definition of each machine is documented in [`stage2_formalization.md`](stage2_formalization.md).

| Component | Design decision | Rationale |
|---|---|---|
| \(Q\) | One state for each distinct prefix of a supported variant, plus an accepting state | The prefix-tree structure makes the machine deterministic and easy to inspect. |
| \(\Sigma\) | Uppercase and lowercase letters, digits, `.`, `-`, `_`, spaces, and the end marker `⊣` | Case handling and token recognition are performed by the transducer rather than by a separate case-normalization step. |
| \(\Gamma\) | Canonical qualification names, such as `JAVASCRIPT` and `NODE_JS`, treated as single output symbols | Each recognized qualification produces one canonical symbol instead of a sequence of output characters. |
| \(\delta\) | Input characters advance the machine through the corresponding prefix states; `⊣` completes a recognized token | The end marker distinguishes complete matches from incomplete prefixes and prevents longer variants from being confused with shorter ones. |
| \(\omega\) | Intermediate transitions output \(\varepsilon\); the transition on `⊣` emits the canonical qualification symbol | The canonical name is emitted only after the entire token has been recognized. |
| \(q_0\) | Initial state representing the empty prefix | Every token is processed from the same starting state. |
| \(F\) | A single accepting state | A token is recognized only when the machine reaches the accepting state. |

### Design alternatives considered

- **Emitting the canonical name on the final character of a variant:** rejected because variants can share prefixes. For example, `react` is a prefix of `react.js`, so emitting `REACT` immediately could produce an incorrect result for the longer variant.
- **Producing one output character per input character:** rejected because normalization can change the length and representation of the input. A qualification is mapped to a single canonical output symbol instead.

## Modules

| Module | Main functions or classes | Input → Output |
|---|---|---|
| `Normalization/catalog.py` | `validate_catalog(catalog)` | Catalog dictionary → `True` or `ValueError` for invalid entries, including ambiguous mappings, uppercase variants, empty values, or reserved markers. |
| `Normalization/spec.py` | `TransducerSpec.add_transition`, `TransducerSpec.translate` | Transition definitions → seven-component transducer specification; input word → output list or `None`. |
| `Normalization/builder.py` | `build_qualification_specs`, `build_union_spec`, `to_word` | Catalog → individual qualification specifications or a combined specification; token → input-symbol list ending in `⊣`. |
| `Normalization/fst.py` | `to_pyformlang`, `PyformlangTransducer.translate` | Transducer specification → `pyformlang.fst.FST`; token → canonical name or `None`. |
| `Normalization/formalization.py` | `generate_document` | Transducer specifications → Markdown documentation containing \(Q\), \(\Sigma\), \(\Gamma\), \(\delta\), \(\omega\), \(q_0\), and \(F\). |
| `Normalization/ordering.py` | `sort_for_profile`, `register_profile` | Canonical qualifications and a profile → deduplicated, ordered qualification list. |
| `Normalization/pipeline.py` | `SkillNormalizer.normalize`, `SkillNormalizer.sorted_by_profile` | Raw qualifications → `NormalizationResult` containing mappings, normalized qualifications, and unrecognized inputs; profile → ordered qualification list. |
| `normalize_resume.py` | `normalize_resume` | Stage 1 output dictionary → JSON containing Stage 2 results. |

## Data Flow

```text
Stage 1: extract_complete_resume_info(text)
    |
    v
technical_skills.raw_skills
["Git", "NodeJS", "JS", "Postgres", "React.js"]
    |
    v
Clean each token
(trim and collapse spaces)
    |
    v
FST translation using pyformlang
    |
    +--> Recognized qualifications
    |    ["GIT", "NODE_JS", "JAVASCRIPT",
    |     "POSTGRESQL", "REACT"]
    |
    +--> Unrecognized qualifications
         (preserved for reporting)
    |
    v
Deduplicate recognized qualifications
    |
    v
sort_for_profile(profile)
    |
    v
Profile-specific ordered sequence
    |
    v
Stage 3: Qualification Pattern Recognition
```

The recognized qualifications are normalized first and ordered afterward. Deduplication removes repeated canonical names, while unrecognized inputs are retained separately rather than being guessed or silently converted.

## Profile-Specific Ordering

Each professional profile defines groups of qualifications and the order in which those groups should appear.

| Profile | Qualification group order |
|---|---|
| Full Stack Developer | Frontend → Backend → Database → Version Control |
| Machine Learning Engineer | Programming Language → Data Processing → Machine Learning → Database → Version Control |
| Cybersecurity Analyst | Operating Systems → Scripting → Network Analysis → Pentesting and Scanning → Monitoring → Standards |
| Data Engineer | Languages → Storage → Processing → Orchestration → Cloud → Containers → Version Control |

Qualifications not explicitly listed in a profile's groups are placed at the end in alphabetical order. Additional team-defined profiles can be registered using `register_profile(name, groups)`.

This ordering provides a consistent representation for Stage 3. It does not, by itself, determine whether a candidate matches a profile; that decision is made by the recognition stage.

## Limitations

- **Catalog-dependent recognition:** Only variants explicitly listed in the catalog are recognized. For example, `Javscript` is reported as unrecognized rather than automatically corrected to `JAVASCRIPT`.
- **Ambiguous abbreviations:** Abbreviations such as `ts`, `tf`, and `ml` may refer to multiple technologies. The catalog assigns each supported abbreviation a specific meaning, typically the most common one within the supported profiles.
- **Unsupported qualifications:** Skills absent from the catalog, such as `Figma` when it has not been registered, are preserved in `unrecognized_skills` and excluded from the recognized qualification sequence passed to Stage 3.
- **Profile-dependent ordering:** The same set of recognized qualifications may appear in different orders depending on the selected professional profile. Qualifications outside a profile's defined groups are placed at the end alphabetically.

## Summary

Stage 2 converts résumé skill names into canonical qualification symbols using deterministic finite-state transducers. It then removes duplicates, records unrecognized inputs, and arranges recognized qualifications according to the selected profile. The resulting sequence provides a consistent input for Stage 3, where finite automata evaluate qualification patterns.