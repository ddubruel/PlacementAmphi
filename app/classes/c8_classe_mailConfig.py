from dataclasses import  dataclass 

# ────────────────────────────────────────────────────────────────────────────────
# Modèles de données
# ────────────────────────────────────────────────────────────────────────────────
@dataclass
class mailConfig  :  
    SMTP_SERVER : str  = "webmail.univ-cotedazur.fr" 
    SMTP_PORT    : int = 587 
    EMAIL_SENDER :str  = "denis.dubruel@univ-cotedazur.fr"
    EMAIL_PASSWORD :str =""
    Nom_utilisateur :str = "ddubruel"
       
    
