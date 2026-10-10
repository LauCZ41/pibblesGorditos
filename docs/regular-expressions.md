This document contains the explanation of the pattern for each element needed for later analysis

# Technical Skills
```
pattern = r'Technical Skills:\s*(.+?)\.?$'
```

This patterer is used to identify the technical skills of the candidates.
*  \s* = This accepts any whitespace between "Technical Skills:" and the information, it allows having cero o more spaces
*  (.+?) = Any character including dots. The "?" makes it not greedy, that means that it matches the shortest possible string that satisfies the pattern.
*  \.?$ = The string may end with an optional literal dot, and nothing can follow it
