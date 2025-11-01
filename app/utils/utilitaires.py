from classes.c1_classe_chargementCsv import chargementCsv
from classes.c2_0_classeS_etudiant_a_amphi import etudiant


def decodeCodeAmphi(code: str) -> str:
    match code:
        case 'SAMPINFO': return 'Informatique'
        case 'SAMPVAL':  return 'Petit_Valrose'
        case 'SPHYS2':   return 'Sc_Physiques'
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
        case 'Sc_Physiques'    : return 'SPHYS2'
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
    if dataBrutes.apogee :
        for k, dataEtu in enumerate(dataBrutes.apogee.data) :  # parcours sur la liste d'étudiant apogée.        
            codeApogeeAmphi : str = dataEtu[10]  # le nom de l'amphi dans le fichier apogée
            nomAmphi : str = decodeCodeAmphi(codeApogeeAmphi)
            if nomAmphi not in listeNomAmphi :
                listeNomAmphi.append(nomAmphi)
                nbAmphi=nbAmphi+1
    return nbAmphi, listeNomAmphi # si test négatif, renvoie 0 et []

def filtreApogee(dataBrutes : chargementCsv , nomAmphi : 'str' ) -> list[list[str]] :
    """extrait des data apogée , tous les étudiants affectés dans un même amphi"""
    extrait : list[list[str]] = []    
    for dataEtud in dataBrutes.apogee.data :
        if dataEtud[10] == reCodeAmphi(nomAmphi)  :
            extrait.append(dataEtud)
            
    extrait2 = [ dataEtud for dataEtud in dataBrutes.apogee.data if dataEtud[10]== reCodeAmphi(nomAmphi) ]

    return extrait


