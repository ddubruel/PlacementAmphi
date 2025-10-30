import tkinter as tk
from tkinter import messagebox

from app.classes.c2_0_classeS_etudiant_a_amphi import amphi,zoneDansAmphi
import sys 
    
def cree_1_zone():
            zone  = zoneDansAmphi ( nbMaxEtuDansZone=25,
                                    nbRang = 10,
                                    nbMaxEtudiantParRang = 5 ,
                                    nbRangUnSurDeux = 5,  
                                    labelZone = ''                                
                                   )
            return [zone] # c 'est une liste de zone.

def cree_2_zones():
        # sert à créer une zone différentes à chaque appel.
        ref =['B','A']
        ListeZones= [ zoneDansAmphi(nbMaxEtuDansZone=42,
                                    nbRang = 14,
                                    nbMaxEtudiantParRang = 6 ,
                                    nbRangUnSurDeux = 7,  
                                    labelZone = chaine,
                                    )  for chaine in ref ]
        return ListeZones
    
def cree_3_zones() :
    # petit Valrose Vide.     
        zoneC = zoneDansAmphi ( nbMaxEtuDansZone=51,
                                nbRang = 17,
                                nbMaxEtudiantParRang = 6 ,
                                nbRangUnSurDeux = 9,  
                                labelZone = 'C',
                                 )  
            
        zoneB =  zoneDansAmphi (nbMaxEtuDansZone=63,
                                nbRang = 17,
                                nbMaxEtudiantParRang = 7 ,
                                nbRangUnSurDeux = 9,  
                                labelZone = 'B',
                                )

        zoneA = zoneDansAmphi ( nbMaxEtuDansZone=51,
                                nbRang = 17,
                                nbMaxEtudiantParRang = 6 ,
                                nbRangUnSurDeux = 9,  
                                labelZone = 'A',
                                )  
        ListeZones=[zoneC,zoneB,zoneA]
        return ListeZones
    

def completeDefinitionAmphi ( amphitheatre : amphi):    
    amphi1zone =['Biologie','Géologie']
    amphi2zones=['Chimie','Sc_Naturelles','Informatique','Sc_Physiques','Mathématiques']
    amphi3zones=['Petit_Valrose']
    
    if amphitheatre.nom in amphi1zone :
        L = cree_1_zone()
        
    elif amphitheatre.nom in amphi2zones :        
        L = cree_2_zones()    
    elif amphitheatre.nom in amphi3zones :
        L = cree_3_zones()
    else :
        messagebox.showinfo("Pb", "Revoir le nom des amphithéatre dans les fichiers.")
        sys.exit(1)
        
    amphitheatre.set_zones(L)

def main():
    amphi1zone =['Biologie','Géologie']
    amphi2zones=['Chimie','Sc_Naturelles','Informatique','Sc_Physiques','Mathématiques']
    amphi3zones=['Petit_Valrose']
    listeNomAmphi = amphi1zone+amphi2zones+amphi3zones


    print(listeNomAmphi)

    # instanciation des amphi
    listAmphi : list [ amphi] =[]
    for nom in  listeNomAmphi :                
         listAmphi.append( amphi(nom) )   # création des n amphis du fichier apogée...amphi à peupler.
    print( f"Création des instances amphi. Vérification des noms des amphis créés :\n"
                f"{[ amphi.nom for amphi in listAmphi ]}" )
        
    L1 = cree_1_zone()
    L2 = cree_2_zones()
    L3 = cree_3_zones()

if __name__ == "__main__":
    # rien ici (laisser vide), on exécutera depuis le lanceur
    pass    
