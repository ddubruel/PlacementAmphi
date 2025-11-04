from dataclasses import dataclass
 
# ────────────────────────────────────────────────────────────────────────────────
# Modèles de données
# ────────────────────────────────────────────────────────────────────────────────

@dataclass 
class dataEpreuve :
    date : str 
    horaires : str 
    duree : str 
    epreuve : str 