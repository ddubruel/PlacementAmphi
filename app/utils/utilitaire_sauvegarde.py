import csv
from datetime import datetime
import os,sys
from classes.c2_0_classeS_etudiant_a_amphi import amphi,etudiant

def ecritFichier(listAmphi : list[amphi] , nom_fichier : str , critere : bool ) :
    
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
    
        
    nom_NOK = f"Z_etudiants_avec_mail_NON_envoyes.csv"
    # Si un chemin est fourni (ex : répertoire racine du projet)
    if chemin_dossier:
        nom_NOK_path : str  = os.path.join(chemin_dossier , nom_NOK)        
    ecritFichier(listAmphi, nom_NOK_path , critere =False  )
    
    nom_OK = f"Z_etudiants_avec_mail_envoyes.csv"
    # Si un chemin est fourni (ex : répertoire racine du projet)
    if chemin_dossier:
        nom_OK_path : str  = os.path.join(chemin_dossier, nom_OK)        
    ecritFichier(listAmphi, nom_OK_path , critere =True  )


    return nom_OK,nom_NOK

def sauveCsv(nomFic : str , entete : list[str], lignes : list[list[str]]):
    print(f"[sauveCsv] écriture dans : {nomFic}")
    try :
        with open(nomFic, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerow(entete)        
            for ligne in lignes :
                writer.writerow(ligne)
            print("[sauveCsv] OK, fichier écrit.")
    except Exception as e:
        print("[sauveCsv] ERREUR :", type(e).__name__, e)
    
     
