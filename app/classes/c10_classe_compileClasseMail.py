from dataclasses import dataclass, field
from classes.c2_0_classeS_etudiant_a_amphi import amphi

@dataclass 
class compileClasseMail:
    """ Cette classe compile toutes les données nécessaires 
    à l'envoi des mails aux étudiants."""
    
    # ce qui est passé à l'instance
    listAmphi: list[amphi]
    
    # les listes de données extraites :
    nom             : list[str] = field(default_factory=list)  # à utiliser sinon toutes les listes partagent la même référence !!
    prenom          : list[str] = field(default_factory=list)
    numeroEtu       : list[str] = field(default_factory=list)
    courriel        : list[str] = field(default_factory=list)    
    nomAmphi        : list[str] = field(default_factory=list) 
    referencePlace  : list[str] = field(default_factory=list) 
    prefixeZone     : list[str]= field(default_factory=list) 
    numeroRang      : list[str]= field(default_factory=list) 
    numeroPlace     : list[str]= field(default_factory=list) 
    fichierPng      : list[str]= field(default_factory=list) 
    statutMail      : list[str]= field(default_factory=list)   # "envoyé" ou "non envoyé"
    
    def __post_init__(self):
        self.extraitValeur()
    
    def extraitValeur(self) -> None :
        for amphiObj in self.listAmphi :             
            for zone in amphiObj.zones  :
                for rang in zone.listeRangDansZoneAmphi :
                    for etu in rang.listeEtudiant :
                        self.nom.append(etu.nom)
                        self.prenom.append(etu.prenom)
                        self.numeroEtu.append(etu.numeroEtudiant)
                        self.courriel.append(etu.courriel)
                        self.nomAmphi.append(amphiObj.nom)
                        self.referencePlace.append(etu.reference_place)
                        self.prefixeZone.append(etu.prefixe_zone)
                        self.numeroRang.append(etu.numeroRang)
                        self.numeroPlace.append(etu.numeroPlace)
                        self.fichierPng.append(etu.fichierPng)
                        self.statutMail.append(False)  # initialement non envoyé !!
    
    def reinitialiser_statut_k(self, k: int) -> None:
        """passe le statutMail de l'étudiant d'indice k à True."""
        if 0 <= k < len(self.statutMail):
            self.statutMail[k] = True
        else:
            raise IndexError(f"Indice k hors limites : {k}. Taille = {len(self.statutMail)}")
    
    def nombre_etudiant(self) -> int:
        """Renvoie le nombre d'éléments stockés (nombre d'étudiants)."""
        return len(self.nom)
    
    def nombre_mail_envoye(self) -> int:
        """Renvoie le nombre d'étudiants dont le statutMail est True."""
        return sum(1 for s in self.statutMail if s is True)