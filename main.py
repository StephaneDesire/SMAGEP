# main.py
from orchestrator import Orchestrator
from agents.content_generator import ContentGenerator
import os

def main():
    # -------------------------
    # 1. Préparer le profil utilisateur
    # -------------------------
    domain = "python"   # ou "c"
    level = "debutant"  # débutant / intermediaire / avance

    orchestrator = Orchestrator()
    profile_payload = orchestrator.prepare_content_for_generator(domain, level)

    print(f"[Main] Profil utilisateur créé : {profile_payload['profile']}")
    print(f"[Main] {len(profile_payload['documents'])} document(s) trouvé(s) dans le corpus.\n")

    # -------------------------
    # 2. Génération de contenu
    # -------------------------
    generator = ContentGenerator()

 
    api_key = os.environ.get("GROQ_API_KEY")  # ou OPENAI_API_KEY
    if not api_key:
        print("[Main] Clé API LLM manquante, génération simulée.\n")
        for doc_name, content in profile_payload["documents"]:
            print(f"--- {doc_name} ---")
            print(content[:200] + "...\n")  # Affiche les 200 premiers caractères
    else:
        # Génération réelle via LLM + RAG
        result = generator.generate_content(profile_payload)
        print("=== Contenu généré ===")
        print(result)

if __name__ == "__main__":
    main()
