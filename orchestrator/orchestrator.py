# orchestrator/orchestrator.py
import os
from agents.profiling_agent import ProfilingAgent

class Orchestrator:
    """
    Orchestrator coordonne les agents :
    - Profiling Agent
    - Path Planning Agent (plus tard)
    - Content Generator (LLM + RAG)
    - XAI Agent (plus tard)
    """
    def __init__(self, corpus_path="data/corpus"):
        # Initialisation du Profiling Agent
        self.profiling_agent = ProfilingAgent(base_path=corpus_path)

    # -------------------------
    # Gestion du profil utilisateur
    # -------------------------
    def create_profile(self, domain: str, level: str, preferences=None):
        """
        Crée et normalise un profil utilisateur.
        """
        profile = self.profiling_agent.create_profile(domain, level, preferences)
        return profile

    def show_profile_summary(self, profile: dict):
        """
        Affiche un résumé du profil utilisateur.
        """
        print(self.profiling_agent.profile_summary(profile))

    # -------------------------
    # Récupération du contenu
    # -------------------------
    def get_user_documents(self, profile: dict):
        """
        Récupère tous les documents disponibles pour un profil donné.
        Retourne une liste de tuples : (nom_fichier, contenu)
        """
        documents = self.profiling_agent.get_available_documents(profile)
        if not documents:
            print(f"Aucun document disponible pour {profile['domain']}/{profile['level']}")
            return []

        contents = []
        for doc in documents:
            path = os.path.join(self.profiling_agent.base_path, profile["domain"], profile["level"], doc)
            with open(path, "r", encoding="utf-8") as f:
                contents.append((doc, f.read()))
        return contents

    def get_random_document(self, profile: dict):
        """
        Récupère un document aléatoire pour un profil donné.
        """
        doc_name = self.profiling_agent.get_random_document(profile)
        if not doc_name:
            return None, None
        path = os.path.join(self.profiling_agent.base_path, profile["domain"], profile["level"], doc_name)
        with open(path, "r", encoding="utf-8") as f:
            return doc_name, f.read()

    # -------------------------
    # Préparation pour Content Generator (LLM + RAG)
    # -------------------------
    def prepare_content_for_generator(self, domain: str, level: str, preferences=None):
        """
        Étapes complètes :
        1. Crée le profil utilisateur
        2. Récupère les documents correspondants
        3. Retourne un dictionnaire prêt pour le Content Generator
        """
        profile = self.create_profile(domain, level, preferences)
        docs = self.get_user_documents(profile)
        content_payload = {
            "profile": profile,
            "documents": docs
        }
        return content_payload

# -------------------------
# Exemple d'utilisation
# -------------------------
if __name__ == "__main__":
    orchestrator = Orchestrator()

    # Création profil utilisateur
    profile = orchestrator.create_profile(domain="python", level="debutant")
    orchestrator.show_profile_summary(profile)

    # Récupération du contenu
    content_payload = orchestrator.prepare_content_for_generator(domain="python", level="debutant")
    print(f"{len(content_payload['documents'])} document(s) récupéré(s).")
    for i, (fname, text) in enumerate(content_payload['documents'], 1):
        print(f"--- Document {i} : {fname} ---\n{text[:200]}...\n")
