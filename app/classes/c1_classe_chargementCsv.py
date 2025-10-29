import csv
import tkinter as tk
from tkinter import messagebox, filedialog
from dataclasses import  dataclass 
from typing import Optional
from io import TextIOWrapper

# ────────────────────────────────────────────────────────────────────────────────
# Modèles de données
# ────────────────────────────────────────────────────────────────────────────────
@dataclass( init=False)  # parce qu'il y a un __init__
class FichierCsv  :  
    formatFic : str     # Rem les arguments sans valeurs par défaut à écrire en premier ou !!
                        # ou alors écrire init=False au début.
    msgChoixFichier : str                     
    chemin: Optional[str]     # Optionnal pour dire  type None ou str (par la suite).
    entete: Optional[list[str]] 
    data: Optional[list[list[str]]] 
    valide : Optional[bool] 
       
    def __init__(self, formatFic: str, msgChoixFichier : str , parent: Optional[tk.Tk] = None):
        """Crée un objet FichierCsv et exécute automatiquement les étapes principales."""
        self.formatFic = formatFic    # contient "Moodle" ou "Apogée"
        self.msgChoixFichier =msgChoixFichier    # pour ajouter "tiers temps" si besoin.
        self.chemin = None
        self.entete = None
        self.data = None
        self.valide = False
        self.nbEtudiant : int = 0
        
        # Étapes automatiques :
        rep="."
        titre=f"Choix du fichier {self.formatFic}."
        self.choisir_fichier(parent, titre, rep )   
        if self.chemin:
            self.charger_csv()
            print(self.chemin)
            print(f"Après self.charger_csv(), il y a {len(self.data)}étudiants.")
            if self.formatFic=="Moodle" :
                self.retirerDoublonsEtEncadrants() # pour enlever les enseingnant non étudiant et les doctorant&Etudiant enregistré 2 fois/
                                                    # il reste quand même les doctorants-étudiant (mais une seule fois)
                                                    # à filtrer avant ce code
                self.nbEtudiant = len(self.data)
                print(f"Après self.retirerDoublonsEtEncadrants(), il y a {self.nbEtudiant} étudiant ou (2eme verif) {len(self.data)} étudiants. ")
                #input('1) presser entrée')
            else :
                pass # le fichier apogée est propre ! pas de doublons (...pour l'instant !!)
            self.valider_contenu()
        if self.valide :
            self.nbEtudiant = len(self.data)
        print(f"La validité du fichier {self.chemin} est  : {self.valide}")
            
    def retirerDoublonsEtEncadrants(self):
        """Retire les doublons dans self.data en se basant sur le numéro d'étudiant (colonne 2)."""
        numeros_vus: set[str] = set()
        data_filtrée: list[list[str]] = []
        
        print( f" Avant filtrage {len(self.data)} étudiants.\n")
        for etu in self.data:                
            num : str = etu[2].strip()
            if num!="" and num not in numeros_vus :
                numeros_vus.add(num)
                data_filtrée.append(etu)
        print( f" Après filtrage {len(data_filtrée)} étudiants.\n")
        print( f" {len(self.data)-len(data_filtrée)} étudiants en double + encadrant rétirés.\n")
        self.data = data_filtrée
        
            
    
    def get_nbEtudiant(self):
        self.nbEtudiant = len(self.data)
        return self.nbEtudiant
    
    def miseAJourData(self,dataFiltree : list[list[str]] ) :
        self.data=dataFiltree
        self.nbEtudiant = len(self.data or [])
                
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
            self.apogee = FichierCsv(formatFic="Apogée",msgChoixFichier="avec tous les étudiants")  # les tiers temps sont déja placé dans Apogée
            print("Le fichier apogée contient :", self.apogee.get_nbEtudiant(),'étudiants')
            #input('2) presser entrée')
            self.moodle = FichierCsv(formatFic="Moodle", msgChoixFichier="avec tous les étudiants")
            print("Le fichier apogée contient :", self.apogee.get_nbEtudiant())
            print("Le fichier moodle contient :", self.moodle.get_nbEtudiant())
            print("Le fichier moodle contient :", len(self.apogee.data))
            #input('3) presser entrée')
        else :
            self.apogee = None
            self.moodle = FichierCsv(formatFic="Moodle", msgChoixFichier="avec tous les étudiants")                        
            tiersTemps : str = messagebox.askquestion("Tiers temps ?","Avez-vous un fichier tiers temps ?",icon ='question' )
            if tiersTemps=='yes':  
                self.moodleTt = FichierCsv(formatFic="Moodle",msgChoixFichier="contenant seulement les tiers temps")                                    
            else :
                self.moodleTt = None            
            self.retirerLesTiersTempsDeMoodle()
        
                
    def retirerLesTiersTempsDeMoodle(self):
        """Retire de l'attribut moodle les étudiants tiers temps s'il y en a."""
        numeros_tt = {etu[2] for etu in self.moodleTt.data} # ensemble des numéros Tier Temps.
        print(f" Il y a {len(self.moodleTt.data)} étudiants tiers temps.")

        moodle_data_filtrée : list[list [str]]= []
        nb_suppr : int = 0
        
        avant= len(self.moodle.data)
        
        for etu in self.moodle.data:
            nmr : str = etu[2]
            if (nmr in numeros_tt) and (nmr!=""):
                nb_suppr = nb_suppr + 1
                print("retrait de ",etu,"\n")
            else:
                moodle_data_filtrée.append(etu) # on garde l'étudiant si non tiers temps.
        
        apres = len(moodle_data_filtrée)
        
        print('avant-apres =' , avant,'-',apres,'=', avant-apres)
        
        print(f"  {nb_suppr} étudiants tiers temps/doublon ont été retiré(s) de la liste principale.\n"
              f" sur {len(self.moodle.data)} étudiants au départ.\n"
              f"La liste des tiers temps est composée de {len(numeros_tt)} étudiants.\n")
        
        self.moodle.miseAJourData(moodle_data_filtrée)
        print(f"La liste néttoyée contient {self.moodle.get_nbEtudiant()} étudiants.")
            

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


  