import csv
from datetime import datetime
import os,sys
from classes.c2_0_classeS_etudiant_a_amphi import amphi,etudiant

def envoi(listAmphi : list[amphi] , nom_fichier : str , critere : bool ) :
    
    with open(nom_fichier, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(["Nom", "Prénom", "Numéro Étudiant", "Email", "Amphi", "Place"])
        
        for amphi in listAmphi:
            for etu in amphi.get_etudiants():
                if  etu.statut == critere :   #choix des étudiants si envoi OK ou pas.
                    writer.writerow([
                        etu.nom,
                        etu.prenom,
                        etu.numeroEtudiant,
                        etu.courriel,
                        amphi.nom,
                        etu.reference_place,
                        etu.fichierPng
                    ])

def sauvegarde_etudiants_non_envoyes(listAmphi, chemin_dossier=""):
    """Sauvegarde dans  deux fichiers CSV (envoi réussi puis envoi en échec)"""
    
        
    nom_NOK = f"etudiants_avec_mail_NON_envoyes.csv"
    # Si un chemin est fourni (ex : répertoire racine du projet)
    if chemin_dossier:
        nom_NOK = os.path.join(chemin_dossier , nom_NOK)        
    envoi(listAmphi, nom_NOK , critere =False  )
    
    nom_OK = f"etudiants_avec_mail_envoyes.csv"
    # Si un chemin est fourni (ex : répertoire racine du projet)
    if chemin_dossier:
        nom_OK = os.path.join(chemin_dossier, nom_OK)        
    envoi(listAmphi, nom_OK , critere =True  )


    return nom_OK,nom_NOK
