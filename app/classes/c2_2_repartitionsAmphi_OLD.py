from dataclasses import dataclass

from classes.c1_classe_chargementCsv import chargementCsv
from classes.c2_0_classeS_etudiant_a_amphi import etudiant, amphi 

from utils.utilitaires import *
# ────────────────────────────────────────────────────────────────────────────────
# Modèles de données
# ────────────────────────────────────────────────────────────────────────────────

@dataclass(init=False)  # parce qu'il y a un __init__

class repartitionAmphi:
    """Représente les répertoires d'un amphithéâtre donné."""

    listeAmphis : list[amphi]
    listeNomAmphis : list[str]
            
    def __init__(self, dataBrutes, tousLesEtudiants : list[etudiant]  ):
        
        self.listeAmphis=[]
        self.listeNomAmphi =[]
        
        if dataBrutes.apogee :            
            self.repartiApogee(dataBrutes.apogee.data , tousLesEtudiants )
        else :
            self.repartiMoodle(dataBrutes.moodle.data)
            
        
    def repartiApogee(self,data : list[list[str]] , tousLesEtudiants : list[etudiant]  ) :
                                
        for k, dataEtu in enumerate(data) :  # parcours sur la liste d'étudiant apogée.
            codeApogeeAmphi : str = dataEtu[10]            
            nomAmphi : str = decodeCodeAmphi(codeApogeeAmphi)
            if nomAmphi not in self.listeNomAmphi : # on crée une nouvelle instance
                amphiARemplir = amphi(nomAmphi)
                self.listeNomAmphi.append(nomAmphi)
                self.listeAmphis.append(amphiARemplir)                
            else :
                amphiARemplir = [ amph  for amph in self.listeAmphis if amph.nom == nomAmphi]
                
            numeroEtudiant = data[k][19]
            #etu : etudiant  =  numeroEtudiant_2_etudiant(numeroEtudiant , tousLesEtudiants)
            etu : etudiant = [ etud for etud in tousLesEtudiants if etud.numeroEtudiant==numeroEtudiant ]            
            amphiARemplir.ajouteEtudiant(etu)
            
    def repartiMoodle(self) :
        pass
    
    

        