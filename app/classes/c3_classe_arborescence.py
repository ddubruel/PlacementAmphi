from dataclasses import dataclass
from pathlib import Path
# ────────────────────────────────────────────────────────────────────────────────
# Modèles de données
# ────────────────────────────────────────────────────────────────────────────────

@dataclass(init=False)  # parce qu'il y a un __init__
class arboAmphi:
    """Représente les répertoires d'un amphithéâtre donné."""

    nom_amphi: str
    racine: str
    pngOut: str
    texOut: str
    listes_Emargement_pdf: str
    

    def __init__(self, nom_amphi: str, racine: str):
        """Construit les chemins des sous-répertoires pour un amphi."""
        self.nom_amphi = nom_amphi
        self.racine = str(Path(racine))
        base = Path(self.racine).resolve().parent / f"Amphi_{nom_amphi}"
        self.pngOut = str(base / "pngOut")
        self.texOut = str(base / "texOut")
        self.listes_Emargement_pdf = str(base / "listes_Emargement_pdf")
        
        self.creer_repertoires()

    def get(self, nom_rep: str) -> str:
        """Retourne le chemin complet d’un sous-répertoire (nom_rep dans {'pngOut', 'texOut', ...})."""
        if not hasattr(self, nom_rep):
            raise ValueError(f"Nom de répertoire inconnu : {nom_rep}")
        return getattr(self, nom_rep)

    def creer_repertoires(self):
        """Crée physiquement les répertoires (idempotent)."""
        for nom_rep in ("pngOut", "texOut", "listes_Emargement_pdf"):
            Path(self.get(nom_rep)).mkdir(parents=True, exist_ok=True)

    def __repr__(self):
        base = Path(self.racine) / f"Amphi_{self.nom_amphi}"
        return f"arboAmphi(nom_amphi='{self.nom_amphi}', base='{base}')"


@dataclass(init=False)  # parce qu'il y a un __init__
class arborescence:
    """Arborescence complète pour plusieurs amphithéâtres."""

    nomFicMoodle: str
    racine: str
    listeNomDesAmphi: list[str]
    liste_arboAmphi: list[arboAmphi]
    chemins: list[str]

    def __init__(self, nomFicMoodle: str, listeNomDesAmphi: list):
        self.nomFicMoodle = nomFicMoodle
        self.racine = str(Path(self.nomFicMoodle))
        self.listeNomDesAmphi = listeNomDesAmphi
        self.liste_arboAmphi = []
        self.chemins = []        
        self.construire_arbo() # creation des n sous répertoires

    def construire_arbo(self):
        """Construit les objets arboAmphi et crée les répertoires."""
        #self.liste_arboAmphi.clear()
        #self.chemins.clear()

        for nom in self.listeNomDesAmphi:
            aa = arboAmphi(nom_amphi=nom, racine=self.racine)
            self.liste_arboAmphi.append(aa)
       
    def get_chemin(self, nomAmphi: str, nom_rep: str):
        """Retourne le chemin complet pour un amphi et un sous-répertoire donnés ."""
        for aa in self.liste_arboAmphi:
            if aa.nom_amphi == nomAmphi:
                return aa.get(nom_rep)
        return None

    def lister_amphis(self):
        """Retourne la liste des noms d’amphis connus."""
        return [aa.nom_amphi for aa in self.liste_arboAmphi]
    
    def __repr__(self):
        attrs = "\n  ".join(f"{k} = {v!r}" for k, v in self.__dict__.items())
        Liste_att = self.liste_attributs()
        return f"<{self.__class__.__name__}(\n  {attrs}\n Les noms des attributs sans les valeurs : \n{Liste_att})>"
    
