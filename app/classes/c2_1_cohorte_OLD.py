from dataclasses import dataclass

from classes.c2_0_classeS_etudiant_a_amphi import etudiant
from classes.c1_classe_chargementCsv import chargementCsv
# ────────────────────────────────────────────────────────────────────────────────
# Modèles de données
# ────────────────────────────────────────────────────────────────────────────────
            
@dataclass(init=False)  # parce qu'il y a un __init__
class cohorte :
    
    listeDesEtudiants : list[etudiant]
    
    def __init__(self,dataBrutes : chargementCsv):
        
        self.listeDesEtudiants =[]
        
        if dataBrutes.apogee :
            for k in range(len(dataBrutes.apogee.data)):
                self.listeDesEtudiants.append(etudiant(nom = dataBrutes.apogee.data[k][17],
                                                       prenom = dataBrutes.apogee.data[k][18], 
                                                       numeroEtudiant = dataBrutes.apogee.data[k][19],
                                                       courriel = "")
                                              )
            self.ajouteCourriel(dataBrutes)
        else :
            for k in range(len(dataBrutes.moodle.data)):
                self.listeDesEtudiants.append(etudiant(nom = dataBrutes.moodle.data[k][1],
                                                       prenom = dataBrutes.moodle.data[k][0], 
                                                       numeroEtudiant = dataBrutes.moodle.data[k][2],
                                                       courriel = dataBrutes.moodle.data[k][4])
                                              )
        

    def ajouteCourriel(self,dataBrutes) :
        """ cette méthode va récupérer l'adresse de courriel dans les données Moodle
         , le numéro d'étudiant est dans moodle et apogée."""
        def rechercheCourriel(liste : list[list[str]] , numeroEtuApogee):
            for index, dataEtudiantMoodle  in enumerate(liste):                
                if numeroEtuApogee in dataEtudiantMoodle:
                    return dataBrutes.moodle.data[ index ][3] 
            return ""
                                                                      
        for etudiant in self.listeDesEtudiants :            
            courriel = rechercheCourriel(dataBrutes.moodle.data , etudiant.numeroEtudiant)
            etudiant.set_courriel( courriel )                                   
            
    ### affichage 
    def __repr__(self):
        return f"{self.__class__.__name__}({self.__dict__})"            
    