import csv
import tkinter as tk
from tkinter import messagebox, filedialog
from dataclasses import  dataclass 
from typing import Optional
# ────────────────────────────────────────────────────────────────────────────────
# Modèles de données
# ────────────────────────────────────────────────────────────────────────────────
@dataclass( init=False)  # parce qu'il y a un __init__
class FichierCsv  :  
    formatFic : str     # Rem les arguments sans valeurs par défaut à écrire en premier ou !!
                        # ou alors écrire init=False au début.
    msgChoixFichier : str                     
    chemin: Optional[str] = None    # Optionnal pour dire  type None ou str (par la suite).
    entete: Optional[list[str]] = None
    data: Optional[list[list[str]]] = None
    valide : Optional[bool] = False 
       
    def __init__(self, formatFic: str, msgChoixFichier : str , parent: Optional[tk.Tk] = None):
        """Crée un objet FichierCsv et exécute automatiquement les étapes principales."""
        self.formatFic = formatFic    # contient "Moodle" ou "Apogée"
        self.msgChoixFichier =msgChoixFichier    # pour ajouter "tiers temps" si besoin.
        self.chemin = None
        self.entete = None
        self.data = None
        self.valide = False
        self.nbEtudiant : int
        
        # Étapes automatiques :
        rep="."
        titre=f"Choix du fichier {self.formatFic}."
        self.choisir_fichier(parent, titre, rep )   
        if self.chemin:
            self.charger_csv()
            self.valider_contenu()
        if self.valide :
            self.nbEtudiant = len(self.data)
        
    def get_nbEtudiant(self):
        return self.nbEtudiant
    
    
    def choisir_fichier(self,tkParent ,  titre  ,rep)-> None :
        messagebox.showwarning(
            title=f"Sélection du fichier {self.formatFic}",
            message=f"Choisir un fichier {self.formatFic} {self.msgChoixFichier} au format Csv."
        )
        
        self.chemin : str  = filedialog.askopenfilename(
                    title=titre,
                    initialdir='.',
                    filetypes=[("Fichiers csv", "*.csv")],
                            )
        if self.chemin =="" :
            messagebox.showwarning( title="Attention !!!!",
                message=f"Vous n'avez pas choisi de fichier !!")

    def charger_csv(self) -> None :
        """Lecture du fichier csv et extraction entête et données."""
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
            (self.formatFic=="Apogée"  and entete[0]!="DAT_DEB_PES")  
            or
            (self.formatFic== "Moodle" and entete[0]!="\ufeffPrénom"  )
        ):
                messagebox.showwarning( title="Erreur de fichier",
                            message=f"Erreur, vous n'avez pas choisi un fichier {self.formatFic} au format csv (à vérifier !).")
                self.valide=False                            
        else :
            self.valide=True
        
    
# ────────────────────────────────────────────────────────────────────────────────
# Fin Modèle de classe FichierCsv
# ────────────────────────────────────────────────────────────────────────────────
        
##########################
#                        #
# class chargementCsv    #
#                        #
##########################

@dataclass ( init=False)  # parce qu'il y a un __init__
class chargementCsv:
    mode: str                              # "Examen" ou "Partiel"
    apogee   : FichierCsv                     # peut être vide en mode Partiel
    moodle   : FichierCsv
    moodleTt : FichierCsv
    
    def __init__(self,mode : str ,tkparent : tk.Tk ):
        self.mode = mode   # "Examen" ou "Partiel"
        
        if self.mode == "Examen" : # chargement des 2 sources d'information
            self.apogee = FichierCsv(formatFic="Apogée")  # les tiers temps sont déja placé dans Apogée
            self.moodle = FichierCsv(formatFic="Moodle", msgChoixFichier="avec tous les étudiants")
        else :
            self.apogee = None
            self.moodle = FichierCsv(formatFic="Moodle", msgChoixFichier="avec tous les étudiants")
            tiersTemps : str = messagebox.askquestion("Tiers temps ?","Avez-vous un fichier tiers temps ?",icon ='question' )
            if tiersTemps=='yes':  
                self.moodleTt = FichierCsv(formatFic="Moodle",msgChoixFichier="contenant seulement les tiers temps")
            else :
                self.moodleT = None 
    
    def getNbmoodle(self):
        return self.moodle.get_nbEtudiant()
    
#     def __repr__(self):
#         attrs = "\n  ".join(f"{k} = {v!r}" for k, v in self.__dict__.items())
#         Liste_att = self.liste_attributs()
#         return f"<{self.__class__.__name__}(\n  {attrs}\n Les noms des attributs sans les valeurs : \n{Liste_att})>"
#     
    def __repr__(self):
        return f"{self.__class__.__name__}({self.__dict__})"
# ────────────────────────────────────────────────────────────────────────────────
# Fin Modèle de classe chargementCsv


  