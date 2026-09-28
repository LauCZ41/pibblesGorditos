This document contains the explanation of the pattern for each element needed for later analysis

# Technical Skills
```
pattern = r'Technical Skills:\s*(.+?)\.?$'
```

This patterer is used to identify the technical skills of the candidates.
*  \s* = This accepts any space between "Technical Skills:" and the information, it allows having cero o more spaces
*  (.+?) = Any digit including dots. And "?" means that is not greedy, that means that 

