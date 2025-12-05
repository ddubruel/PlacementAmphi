from dataclasses import  dataclass 

# ────────────────────────────────────────────────────────────────────────────────
# Modèles de données
# ────────────────────────────────────────────────────────────────────────────────
@dataclass
class mailConfig  :  
    SMTP_SERVER : str  = "webmail.univ-cotedazur.fr" 
    SMTP_PORT    : int = 587 
    EMAIL_SENDER :str  = ""
    EMAIL_PASSWORD :str =""
    Nom_utilisateur :str = ""
    t_tempo : int = 5
