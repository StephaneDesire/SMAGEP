# agents/profiling_agent.py
import os
import random
from typing import Dict, List

class ProfilingAgent:
    def __init__(self, base_path="data/corpus"):
        self.base_path = base_path
        # Découverte automatique des domaines
        self.allowed_domains = self._discover_domains()
        self.allowed_levels = ["debutant", "intermediaire", "avance"]

    def _discover_domains(self) -> List[str]:
        """Découvre les sous-dossiers dans data/corpus comme domaines valides"""
        if not os.path.exists(self.base_path):
            return []
        return [d.lower() for d in os.listdir(self.base_path) 
                if os.path.isdir(os.path.join(self.base_path, d))]

    def validate_domain(self, domain: str) -> bool:
        return domain.lower() in self.allowed_domains

    def validate_level(self, level: str) -> bool:
        return level.lower() in self.allowed_levels

    def normalize_text(self, text: str) -> str:
        """Nettoyage basique : minuscules, suppression espaces"""
        return text.strip().lower()

    def normalize_profile(self, profile: Dict[str, str]) -> Dict[str, str]:
        domain = self.normalize_text(profile.get("domaine", ""))
        level = self.normalize_text(profile.get("niveau", ""))

        if not self.validate_domain(domain):
            raise ValueError(f"Domaine inconnu : {domain}")
        if not self.validate_level(level):
            raise ValueError(f"Niveau inconnu : {level}")

        return {"domain": domain, "level": level}

    def create_profile(self, domain: str, level: str, preferences: Dict = None) -> Dict[str, str]:
        """Crée un profil normalisé avec options supplémentaires"""
        profile = self.normalize_profile({"domaine": domain, "niveau": level})
        profile["preferences"] = preferences or {}
        return profile

    def get_available_documents(self, profile: Dict[str, str]) -> List[str]:
        """Liste tous les documents disponibles pour un profil donné"""
        profile = self.normalize_profile(profile)
        path = os.path.join(self.base_path, profile["domain"], profile["level"])
        if not os.path.exists(path):
            return []
        return [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

    def get_random_document(self, profile: Dict[str, str]) -> str:
        """Récupère un document aléatoire du profil"""
        docs = self.get_available_documents(profile)
        return random.choice(docs) if docs else None

    def profile_summary(self, profile: Dict[str, str]) -> str:
        """Retourne un résumé lisible du profil utilisateur"""
        summary = f"Domaine: {profile['domain']}, Niveau: {profile['level']}"
        if "preferences" in profile and profile["preferences"]:
            summary += f", Préférences: {profile['preferences']}"
        return summary
