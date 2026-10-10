
 
import re
 
# Input alphabet Sigma: lowercase letters, digits, '.', '-', '_' and space.
SIGMA = frozenset(
    "abcdefghijklmnopqrstuvwxyz0123456789.-_ "
)
 
# Known categories. The order here is only a default; each profile
# defines its own category order in profiles/profiles.py.
CATEGORIES = (
    "language",
    "frontend",
    "backend",
    "api",
    "database",
    "version_control",
    "data_processing",
    "ml_framework",
    "ml_practice",
)
 
CATALOG = {
    # ---------------- Languages ----------------
    "JAVASCRIPT": {
        "category": "language",
        "variants": ["js", "javascript", "java script", "ecmascript"],
    },
    "TYPESCRIPT": {
        "category": "language",
        "variants": ["ts", "typescript", "type script"],
    },
    "PYTHON": {
        "category": "language",
        "variants": ["python", "python3", "python 3", "py"],
    },
    "JAVA": {
        "category": "language",
        "variants": ["java"],
    },
 
    # ---------------- Frontend ----------------
    "REACT": {
        "category": "frontend",
        "variants": ["react", "react.js", "reactjs", "react js"],
    },
    "ANGULAR": {
        "category": "frontend",
        "variants": ["angular", "angular.js", "angularjs", "angular js"],
    },
    "VUE": {
        "category": "frontend",
        "variants": ["vue", "vue.js", "vuejs", "vue js"],
    },
 
    # ---------------- Backend ----------------
    "NODE_JS": {
        "category": "backend",
        "variants": ["node", "nodejs", "node.js", "node js"],
    },
    "EXPRESS": {
        "category": "backend",
        "variants": ["express", "express.js", "expressjs", "express js"],
    },
    "DJANGO": {
        "category": "backend",
        "variants": ["django"],
    },
    "SPRING_BOOT": {
        "category": "backend",
        "variants": ["spring boot", "springboot", "spring-boot"],
    },
    "FLASK": {
        "category": "backend",
        "variants": ["flask"],
    },
    "FASTAPI": {
        "category": "backend",
        "variants": ["fastapi", "fast api", "fast-api"],
    },
 
    # ---------------- APIs ----------------
    "REST_API": {
        "category": "api",
        "variants": [
            "rest", "rest api", "rest apis", "rest-api",
            "restful", "restful api", "restful apis",
        ],
    },
 
    # ---------------- Databases ----------------
    "SQL": {
        "category": "database",
        "variants": ["sql"],
    },
    "POSTGRESQL": {
        "category": "database",
        "variants": ["postgres", "postgresql", "postgre sql", "postgre-sql"],
    },
    "MYSQL": {
        "category": "database",
        "variants": ["mysql", "my sql", "my-sql"],
    },
    "MONGODB": {
        "category": "database",
        "variants": ["mongo", "mongodb", "mongo db", "mongo-db"],
    },
    "REDIS": {
        "category": "database",
        "variants": ["redis"],
    },
 
    # ---------------- Version control ----------------
    # Design decision: GitHub is treated as an equivalent of Git for
    # screening purposes (document this in docs/stage2_transducers.md).
    "GIT": {
        "category": "version_control",
        "variants": ["git", "github", "git hub"],
    },
 
    # ---------------- Data processing ----------------
    "PANDAS": {
        "category": "data_processing",
        "variants": ["pandas"],
    },
    "NUMPY": {
        "category": "data_processing",
        "variants": ["numpy", "num py", "np"],
    },
 
    # ---------------- ML frameworks ----------------
    "SCIKIT_LEARN": {
        "category": "ml_framework",
        "variants": [
            "sklearn", "scikit learn", "scikit-learn",
            "scikitlearn", "sk-learn", "sk learn",
        ],
    },
    "TENSORFLOW": {
        "category": "ml_framework",
        "variants": ["tensorflow", "tensor flow", "tensor-flow", "tf"],
    },
    "PYTORCH": {
        "category": "ml_framework",
        "variants": ["pytorch", "py torch", "py-torch", "torch"],
    },
 
    # ---------------- ML practice ----------------
    "MACHINE_LEARNING": {
        "category": "ml_practice",
        "variants": [
            "machine learning", "machine-learning", "ml",
            "machine learning model development",
            "ml model development",
        ],
    },
}
 
