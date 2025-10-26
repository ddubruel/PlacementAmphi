import csv
import tkinter as tk
from tkinter import messagebox, filedialog
from dataclasses import  dataclass 
from typing import Optional

# ────────────────────────────────────────────────────────────────────────────────
# Modèles de données
# ────────────────────────────────────────────────────────────────────────────────
@dataclass( init=False)  # parce qu'il y a un __init__
class FichierCSV  :  
    formatFic : str     # Rem les arguments sans valeurs par défaut à écrire en premier ou !!
                        # ou alors écrire init=False au début.
    chemin: Optional[str] = None    # Optionnal pour dire  type None ou str (par la suite).
    entete: Optional[list[str]] = None
    data: Optional[list[list[str]]] = None
    valide : Optional[bool] = False 
       
    def __init__(self, formatFic: str, parent: Optional[tk.Tk] = None):
        """Crée un objet FichierCSV et exécute automatiquement les étapes principales."""
        self.formatFic = formatFic
        self.chemin = None
        self.entete = None
        self.data = None
        self.valide = False

        # Étapes automatiques :
        rep="."
        titre=f"Choix du fichier pour un {self.formatFic}."
        self.choisir_fichier(parent, titre, rep )   # définit
        if self.chemin:
            self.charger_csv()
            self.valider_contenu()    
        
    
    def choisir_fichier(self,tkParent ,  titre  ,rep)-> None :
        messagebox.showwarning(
            title=f"Sélection du fichier {self.formatFic}",
            message=f"Choisir un fichier {self.formatFic} au format CSV."
        )
        
        self.chemin : str  = filedialog.askopenfilename(
                    title=titre,
                    initialdir='.',
                    filetypes=[("Fichiers CSV", "*.csv")],
                            )
        if self.chemin =="" :
            messagebox.showwarning( title="Attention !!!!",
                message=f"Vous n'avez pas choisi de fichier !!")

    def charger_csv(self) -> None :
        """Lecture du fichier CSV et extraction entête et données."""
        try :
            # ouverture
            fichier : TextIOWrapper = open(self.chemin, "r", encoding="utf-8")
            # recherche du séparateur
            debut = fichier.read(4096) # lit 4096 premiers caractères du fichier 
            fichier.seek(0)  # ramène le pointeur de lecture au début pour appeler csv.reader après
            dialect = csv.Sniffer().sniff(debut, delimiters=[',',';','\t','|']) # détection du délimiteur parmi la liste
            # lecture avec le délimiteur trouvé : 
            reader = csv.reader(fichier, delimiter=dialect.delimiter) # lecture du csv avec ce délimiteur
            # conversion en liste :
            lignes: list[list[str]] = []
            for ligne in reader:
                lignes.append(ligne)  # Ajouter chaque ligne à la liste
            fichier.close()    #fermeture.
            self.entete : list[str] = lignes[0]
            self.data: list[list[str]] = lignes[1:]
        except Exception as e: 
            raise ValueError(f"Plantage dans charger_csv, voici la cause :  ({type(e).__name__}) : {e} \n\n"
                             f"Veuillez vérifier vos fichiers csv d'origine.\n"
                             f" Attention à vos modifications et vos sauvegardes.") from e
        
        
        
    def valider_contenu(self)-> None :    
        entete = self.entete or [] # pour éviter le cas None
        if (
            (self.formatFic=="Examen"  and "COD_EPR" not in entete)
            or
            (self.formatFic== "Partiel" and "Nom de famille"  not in entete )
        ):
                messagebox.showwarning( title="Erreur de fichier",
                                   message=f"Erreur, vous n'avez pas choisi un fichier {nature} au format CSV (à vérifier !).")
                self.valide=False  
        self.valide=True
# ────────────────────────────────────────────────────────────────────────────────
# Fin Modèle de classe FichierCsv
# ────────────────────────────────────────────────────────────────────────────────
        
##########################
#                        #
# class chargementCSV    #
#                        #
##########################

@dataclass ( init=False)  # parce qu'il y a un __init__
class chargementCSV:
    mode: str                              # "Examen" ou "Partiel"
    apogee: FichierCSV                     # peut être vide en mode Partiel
    moodle: FichierCSV

    def __init__(self,mode : str ,tkparent : tk.Tk ):
        self.mode = mode   # "Examen" ou "Partiel"
        
        if self.mode == "Examen" : # chargement des 2 sources d'information
            self.apogee = FichierCSV(formatFic="Apogée")
            self.moodle = FichierCSV(formatFic="Moodle")
        else :
            self.apogee = None
            self.moodle = FichierCSV(formatFic="Moodle")
    
    def __repr__(self):
        attrs = "\n  ".join(f"{k} = {v!r}" for k, v in self.__dict__.items())
        Liste_att = self.liste_attributs()
        return f"<{self.__class__.__name__}(\n  {attrs}\n Les noms des attributs sans les valeurs : \n{Liste_att})>"
  
# ────────────────────────────────────────────────────────────────────────────────
# Fin Modèle de classe chargementCsv


  