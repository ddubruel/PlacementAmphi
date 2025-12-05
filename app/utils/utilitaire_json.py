import os
import json
from tkinter import messagebox, filedialog


def sauvegarder_donnees_message(repertoire: str, sujet: str, corps: str):   
    """Sauvegarde les données du message dans un fichier JSON."""
    donnees = {
        "sujet": sujet,
        "corps": corps
    }         
    # sauvegarde dans un fichier JSON dans le répertoire des CSV
    chemin_json = os.path.join(repertoire, "Z_data_message.json")
    with open(chemin_json, "w", encoding="utf-8") as f:
        json.dump(donnees, f, ensure_ascii=False, indent=4)
        
def charger_donnees_message(repertoire: str):
    """Charge les données du message depuis un fichier JSON.
    Retourne un dict avec 'titre' et 'corps', ou None si le fichier n'existe pas.
    """
    chemin_json = os.path.join(repertoire, "Z_data_message.json")

    if not os.path.exists(chemin_json):
        return None

    with open(chemin_json, "r", encoding="utf-8") as f:
        donnees = json.load(f)

    return donnees

def recupJson(repertoire) :
    # récupération des données de l'épreuve déja saisies et stockées dans le json.
    ficEpreuve = repertoire+'/'+"Z_data_epreuve.json"
    with open(ficEpreuve, "r", encoding="utf-8") as f:
        donnees = json.load(f)
    annee_universitaire = donnees["annee_universitaire"]
    date = donnees["date"]
    horaires = donnees["horaires"]
    duree = donnees["duree"]
    epreuve = donnees["epreuve"]
    return annee_universitaire,date,horaires,duree,epreuve

    ### fin recup

def sauvegarderJson(repertoire: str,annee_universitaire : str,  date: str, horaires: str, duree: str, epreuve: str):
    """Sauvegarde les données de l'épreuve dans un fichier JSON."""

    donnees = {
        "annee_universitaire": annee_universitaire,
        "date": date,
        "horaires": horaires,
        "duree": duree,
        "epreuve": epreuve
    }

    # Chemin de sauvegarde du fichier JSON
    chemin_json = os.path.join(repertoire, "Z_data_epreuve.json")

    # Écriture du fichier JSON
    with open(chemin_json, "w", encoding="utf-8") as f:
        json.dump(donnees, f, ensure_ascii=False, indent=4)
        

def choisirFichierPoursuite ( )-> str  :
    """ renvoie le répertoire où se trouve le fichier Z_dataMail.csv
    pour poursuivre l'envoi des mails."""
    messagebox.showwarning(
        title=f"Sélection du fichier pour poursuivre l'envoi des mails",
        message=f"Chercher le fichier Z_dataMail.csv de votre projet à finir."
    )

    chemin : str  = filedialog.askopenfilename(
                title=  "Choisir le répertoire contenant le fichier Z_dataMail.csv",
                initialdir='.',
                filetypes=[("Fichiers csv", "Z_dataMail.csv")],
                        )
    if chemin =="" :
        messagebox.showwarning( title="Attention !!!!",
            message=f"Vous n'avez pas choisi de fichier !!")
    else :
        return  os.path.dirname(chemin)