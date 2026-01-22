# config.py

# ===============================
# LLM CONFIG (GROQ)
# ===============================

LLM_PROVIDER = "groq"
LLM_MODEL = "llama-3.1-70b-versatile"
TEMPERATURE = 0.3
MAX_TOKENS = 2048

# ===============================
# DOMAINS CONFIG
# ===============================

DOMAINS = {
    "python": {
        "name": "Programmation Python",
        "levels": ["debutant", "intermediaire", "avance"]
    },
    "c": {
        "name": "Programmation C",
        "levels": ["debutant", "intermediaire", "avance"]
    }
}

# ===============================
# RAG CONFIG
# ===============================

CHUNK_SIZE = 800
CHUNK_OVERLAP = 100
TOP_K_DOCS = 4

# ===============================
# PEDAGOGICAL RULES
# ===============================

PEDAGOGICAL_GOALS = {
    "debutant": "Comprendre les bases et écrire des programmes simples",
    "intermediaire": "Approfondir les concepts et résoudre des problèmes",
    "avance": "Optimiser, raisonner sur les performances et les architectures"
}
