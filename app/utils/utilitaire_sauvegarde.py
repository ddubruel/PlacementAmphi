import csv
from datetime import datetime

def sauvegarde_etudiants_non_envoyes(listAmphi, chemin_dossier=""):
    """Sauvegarde dans un fichier CSV les étudiants dont le statut d'envoi est False."""
    
    # Nom de fichier avec timestamp pour éviter l'écrasement
     
    nom_fichier = f"etudiants_mail_non_envoyes.csv"

    # Si un chemin est fourni (ex : répertoire racine du projet)
    if chemin_dossier:
        nom_fichier = os.path.join(chemin_dossier, nom_fichier)

    with open(nom_fichier, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(["Nom", "Prénom", "Numéro Étudiant", "Email", "Amphi", "Place"])
        
        for amphi in listAmphi:
            for etu in amphi.get_etudiants():
                if not etu.statut:   # ❗ envoi KO
                    writer.writerow([
                        etu.nom,
                        etu.prenom,
                        etu.numeroEtudiant,
                        etu.courriel,
                        amphi.nom,
                        etu.reference_place,
                        etu.fichierPng
                    ])

    return nom_fichier
