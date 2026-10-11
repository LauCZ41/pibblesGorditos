END_MARKER = "\u22a3"  # ⊣

# canonical name -> variants (lower case, as they may appear in a résumé)
CATALOG = {
    # --- languages -------------------------------------------------------
    "JAVASCRIPT": ["js", "javascript", "java script", "ecmascript"],
    "TYPESCRIPT": ["ts", "typescript", "type script"],
    "PYTHON": ["python", "python3", "python 3"],
    "HTML": ["html", "html5"],
    "CSS": ["css", "css3"],
    # --- frontend frameworks ---------------------------------------------
    "REACT": ["react", "react.js", "reactjs", "react js"],
    "ANGULAR": ["angular", "angular.js", "angularjs", "angular js"],
    "VUE": ["vue", "vue.js", "vuejs", "vue js"],
    # --- backend frameworks ----------------------------------------------
    "NODE_JS": ["node", "node.js", "nodejs", "node js"],
    "DJANGO": ["django"],
    "SPRING_BOOT": ["spring boot", "springboot", "spring-boot"],
    "FLASK": ["flask"],
    "FASTAPI": ["fastapi", "fast api", "fast-api"],
    "REST_API": [
        "rest", "rest api", "rest apis", "rest-api", "rest-apis",
        "restful", "restful api", "restful apis",
    ],
    # --- databases -------------------------------------------------------
    "SQL": ["sql"],
    "NOSQL": ["nosql", "no sql", "no-sql"],
    "POSTGRESQL": ["postgres", "postgresql", "postgre sql"],
    "MYSQL": ["mysql", "my sql"],
    "MONGODB": ["mongo", "mongodb", "mongo db"],
    # --- data / machine learning -----------------------------------------
    "PANDAS": ["pandas"],
    "NUMPY": ["numpy", "num py"],
    "SCIKIT_LEARN": [
        "sklearn", "scikit learn", "scikit-learn", "scikit_learn", "scikitlearn",
    ],
    "TENSORFLOW": ["tensorflow", "tensor flow", "tensor-flow", "tf"],
    "PYTORCH": ["pytorch", "py torch", "py-torch", "torch"],
    "MACHINE_LEARNING": [
        "machine learning", "machine-learning", "ml",
        "machine learning models", "machine-learning models",
    ],
    # --- tools -----------------------------------------------------------
    "GIT": ["git"],
    "DOCKER": ["docker"],
    "KUBERNETES": ["kubernetes", "k8s"],
    "AWS": ["aws", "amazon web services"],
    "LINUX": ["linux"],
}
