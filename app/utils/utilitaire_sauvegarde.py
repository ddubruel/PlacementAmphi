import csv
from datetime import datetime
import os,sys


from dataclasses import dataclass, field

from app.classes.c2_0_classeS_etudiant_a_amphi import amphi,etudiant
from app.classes.c10_classe_compileClasseMail import compileClasseMail

from tkinter import messagebox, filedialog

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
        
        
def sauvegarde_etudiants_non_envoyes(listAmphi, chemin_dossier=""):
    """Sauvegarde dans  deux fichiers CSV (envoi réussi puis envoi en échec)"""
    

    nom_NOK = "Z_etudiants_avec_mail_NON_envoye_1.csv"  # ne pas modifier (voir definit_nom_fic_reprise_envoi)
    # Si un chemin est fourni (ex : répertoire racine du projet)
    if chemin_dossier:
        nom_NOK_path : str  = os.path.join(chemin_dossier , nom_NOK)        
    ecritFichier(listAmphi, nom_NOK_path , critere =False  )
    
    nom_OK = f"Z_etudiants_avec_mail_envoye_1.csv"
    # Si un chemin est fourni (ex : répertoire racine du projet)
    if chemin_dossier:
        nom_OK_path : str  = os.path.join(chemin_dossier, nom_OK)        
    ecritFichier(listAmphi, nom_OK_path , critere =True  )

    return nom_OK,nom_NOK
    
def definit_nom_fic_reprise_envoi( chemin_dossier=""):
    """ regarde dans le répertoire donné (ou courant si vide) les fichiers de sauvegarde
        et détermine les noms des fichiers d'entrée et de sortie pour la reprise des envois de mails.
        Renvoie : nom_fic_entrée, nom_fic_sortie_envoyé, nom_fic_sortie_non_envoyé
    """
    
    base ="Z_etudiants_avec_mail_NON_envoye_"  # reprise du nom de sauvegarde_etudiants_non_envoyes
    sortie = "Z_etudiants_avec_mail_envoye_"
    
    fichiers : list[str] = [
        f for f in os.listdir(chemin_dossier)
        if f.startswith(base) and f.endswith(".csv")
    ]
    if len(fichiers)!=0  :
        # on coupe le début (contenu de base)
        fin : list[str] =[ nom[len(base):] for nom in fichiers]
        # on coupe la fin (le ".csv")
        numeroStr : list[str] = [ nom[:-4] for nom in fin]
        numeroInt : list[int] = [ int(chaine) for chaine in numeroStr]
        maximum : int  = max(numeroInt)
        ficIn : str =f"{base}{maximum}.csv"
        ficOutEnvoye : str =f"{sortie}{maximum+1}.csv"
        ficOutNonEnvoye: str =f"{base}{maximum+1}.csv"
        return ficIn,ficOutEnvoye,ficOutNonEnvoye
        
    else :
        messagebox.showinfo("fichier", "La reprise d'envoi des mails n'est pas possible. Un fichier Z_*.csv a été effacé !")
    
    
def sauvegarder_compileClasseMail(obj: compileClasseMail,nomFichier : str,  repertoire: str):
    """
    Sauvegarde les attributs de l'objet compileClasseMail dans un fichier CSV.
    La première ligne contient les noms des attributs.
    Les lignes suivantes contiennent les valeurs indexées.
    """
    # Liste des attributs listés à sauvegarder (dans le même ordre que la classe)
    champs = [
        "nom",
        "prenom",
        "numeroEtu",
        "courriel",
        "nomAmphi",
        "referencePlace",
        "prefixeZone",
        "numeroRang",
        "numeroPlace",
        "fichierPng",
        "statutMail",
    ]
    # Construction du chemin du fichier
    chemin_csv = os.path.join(repertoire, nomFichier)

    # Ouverture du fichier CSV en écriture
    with open(chemin_csv, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, delimiter=";")

        # 1) écrire l'en-tête
        writer.writerow(champs)

        # 2) déterminer le nombre de lignes (nombre d'étudiants)
        nb_lignes = obj.nombre_etudiant()

        # 3) écrire chaque ligne
        for i in range(nb_lignes):
            ligne = [
                getattr(obj, champ)[i]  # accède à obj.nom[i], obj.prenom[i], etc.
                for champ in champs
            ]
            writer.writerow(ligne)




def charger_compileClasseMail(repertoire: str, fichier: str) -> compileClasseMail:
    """
    Recharge un fichier Z_dataMail.csv et restitue un objet compileClasseMail
    dont les listes d'attributs sont remplies.
    """
    chemin_csv = os.path.join(repertoire, fichier )

    # Vérification fichier
    if not os.path.exists(chemin_csv):
        raise FileNotFoundError(f"Fichier introuvable : {chemin_csv}")

    # Lecture du CSV
    with open(chemin_csv, "r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=";")
        lignes = list(reader)

    # La première ligne contient les noms des champs
    en_tete = lignes[0]
    corps = lignes[1:]

    # Création d’un nouvel objet vide (listAmphi n’est pas reconstruite via CSV)
    obj = compileClasseMail(listAmphi=[])

    # Pré-remplissage de toutes les listes pour éviter l'appel automatique à extraitValeur()
    for champ in en_tete:
        setattr(obj, champ, [])

    # Remplissage des listes à partir du CSV
    for ligne in corps:
        for champ, valeur in zip(en_tete, ligne):
            # Conversion du statutMail en bool
            if champ == "statutMail":
                valeur = valeur.lower() == "true"
            getattr(obj, champ).append(valeur)

    return obj

   
def main():
    
    pass

