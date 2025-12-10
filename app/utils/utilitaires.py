from classes.c1_classe_chargementCsv import chargementCsv
from classes.c2_0_classeS_etudiant_a_amphi import etudiant


def decodeCodeAmphi(code: str) -> str:
    match code:
        case 'SAMPINFO': return 'Informatique'
        case 'SAMPVAL':  return 'Petit_Valrose'
        case 'SPHYS2':   return 'Physique'
        case 'SAMPBIOL': return 'Biologie'
        case 'SAMPHIM':  return 'Mathématiques'
        case 'SCHIMIE':  return 'Chimie'
        case 'SAMPGEOL': return 'Géologie'
        case 'SSNAT':    return 'Sc_Naturelles'
        case _:          raise ValueError(f"Code inconnu: {code}. Revoir le fichier Apogée.")

def reCodeAmphi(nom: str) -> str:
    match nom:
        case 'Informatique'    : return 'SAMPINFO' 
        case 'Petit_Valrose'   : return 'SAMPVAL'
        case 'Physique'    : return 'SPHYS2'
        case 'Biologie'        : return 'SAMPBIOL'
        case 'Mathématiques'   : return 'SAMPHIM'
        case 'Chimie'          : return 'SCHIMIE'
        case 'Géologie'        : return 'SAMPGEOL'
        case 'Sc_Naturelles'   : return 'SSNAT'
        case _:          raise ValueError(f"Code inconnu: {nom}. Revoir le fichier Apogée.")

def numeroEtudiant_2_etudiant(numeroEtudiant :str  , tousLesEtudiants : list[etudiant]  ):
    for  etudiant in enumerate(tousLesEtudiants) :
        if numeroEtudiant in etudiant :
            return etudiant
    raise  ValueError ("Fichiers d'entrées incorrects.")


def recupereCourrielMoodle( numeroEtuApogee : str , dataBrutes : chargementCsv) -> str:
    """ cette fonction va récupérer l'adresse de courriel dans les données Moodle
        , le numéro d'étudiant est dans moodle et apogée."""        
    for index, dataEtudiantMoodle in enumerate(dataBrutes.moodle.data):        
        if numeroEtuApogee==dataEtudiantMoodle[2]:
            return dataBrutes.moodle.data[index][3] 
    return ""

def compteEtListeAmphiApogee( dataBrutes : chargementCsv):

    nbAmphi : int = 0
    listeNomAmphi : list[str]=[]
    enteteApogee : list[str] = dataBrutes.apogee.entete
    indexAmphi : int = enteteApogee.index("COD_SAL")
    
    if dataBrutes.apogee :
        for k, dataEtu in enumerate(dataBrutes.apogee.data) :  # parcours sur la liste d'étudiant apogée.        
            codeApogeeAmphi : str = dataEtu[indexAmphi]  # le nom de l'amphi dans le fichier apogée
            nomAmphi : str = decodeCodeAmphi(codeApogeeAmphi)
            if nomAmphi not in listeNomAmphi :
                listeNomAmphi.append(nomAmphi)
                nbAmphi=nbAmphi+1
    return nbAmphi, listeNomAmphi # si test négatif, renvoie 0 et []

def filtreApogee(dataBrutes : chargementCsv , nomAmphi : 'str' ) -> list[list[str]] :
    """extrait des data apogée , tous les étudiants affectés dans un même amphi"""
    extrait : list[list[str]] = [] 
    enteteApogee : list[str] = dataBrutes.apogee.entete   
    indexAmphi : int = enteteApogee.index("COD_SAL")
    for dataEtud in dataBrutes.apogee.data :
        if dataEtud[indexAmphi] == reCodeAmphi(nomAmphi)  :
            extrait.append(dataEtud)
            
    #extrait2 = [ dataEtud for dataEtud in dataBrutes.apogee.data if dataEtud[10]== reCodeAmphi(nomAmphi) ]

    return extrait

def recupDataEpreuveApogee(dataBrutes : chargementCsv) -> tuple[str,str,str,str,str] :
    """ récupère les données de l'épreuve dans le fichier apogée
        on suppose que toutes les lignes d'étudiants ont les mêmes données d'épreuve
        on lit donc la première ligne seulement."""
    enteteApogee : list[str] = dataBrutes.apogee.entete
    indexAnneeUniversitaire : int = enteteApogee.index("C_COD_ANU")
    indexDate : int = enteteApogee.index("DAT_DEB_PES")
    indexHoraires : int = enteteApogee.index("HEURE_DEBUT")
    indexDuree : int = enteteApogee.index("DUREE_EXA")
    indexEpreuve : int = enteteApogee.index("COD_EPR")
    
    premiereLigneEtudiant : list[str] = dataBrutes.apogee.data[0]
    
    annee_universitaire : str = premiereLigneEtudiant[indexAnneeUniversitaire]
    date : str = premiereLigneEtudiant[indexDate]
    horaires : str = premiereLigneEtudiant[indexHoraires]
    duree : str = premiereLigneEtudiant[indexDuree]
    epreuve : str = premiereLigneEtudiant[indexEpreuve]
    
    return annee_universitaire, date, horaires, duree, epreuve


