from dataclasses import dataclass

# ────────────────────────────────────────────────────────────────────────────────
# Modèles de données
# ────────────────────────────────────────────────────────────────────────────────

@dataclass(init=False)  # parce qu'il y a un __init__
class etudiant:
    nom : str 
    prenom : str 
    numeroEtudiant : str 
    courriel : str 
    
    def __init__(self,nom,prenom,numeroEtudiant,courriel):
        self.nom = nom 
        self.prenom = prenom 
        self.numeroEtudiant = numeroEtudiant
        self.courriel = courriel
        
    
    def set_courriel(self,courriel):
        self.courriel = courriel
        