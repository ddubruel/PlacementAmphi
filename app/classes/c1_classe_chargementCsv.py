import csv
import tkinter as tk
import unicodedata
import sys, os

from tkinter import messagebox, filedialog
from dataclasses import  dataclass
from typing import Optional
from io import TextIOWrapper
import random
from app.utils.utilitaire_sauvegarde import  sauveCsv

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
        self.formatFic = formatFic    # contient "Moodle" ou "Apogée"  ou Ade
        self.msgChoixFichier =msgChoixFichier    # pour ajouter "tiers temps" si besoin.
        self.chemin = None
        self.repertoire = None
        self.entete = None
        self.data = None
        self.valide = False
        self.annule = False  # flag si jamais il y a déja un placement en cours et que l'utilisateur annule.
        self.nbEtudiant : int = 0

        # Étapes automatiques :
        rep="."
        titre=f"Choix du fichier {self.formatFic}."

        self.choisir_fichier(parent, titre, rep )
        if self.annule :
            return
        
        if self.chemin:
            self.valide = False
            while not self.valide and self.chemin :
                self.charger_csv()   #  on charge le fichier
                self.valider_contenu() # on regarde sa validité
                print(f"La validité du fichier {self.chemin} est  : {self.valide}")
                if not self.valide:
                    messagebox.showwarning(
                        title="Erreur de fichier",
                        message=f"Ce fichier n'est pas un {self.formatFic} valide.\n"
                        f"Veuillez en choisir un autre."
                    )
                    # redemande d'un fichier (peut devenir "")
                    self.choisir_fichier(parent, titre, rep)
            # si on sort de la boucle parce que self.chemin == ""
            if not self.chemin:
                messagebox.showwarning("Annulation", "Aucun fichier sélectionné.")
                return


            print(self.chemin)
            print(f"Après self.charger_csv(), il y a {len(self.data)}étudiants.")
            if self.formatFic=="Moodle" :
                self.trierAlphaNom()
                self.retirerDoublonsEtEncadrants() # pour enlever les enseingnant non étudiant et les doctorant&Etudiant enregistré 2 fois/
                                                    # il reste quand même les doctorants-étudiant (mais une seule fois)
                                                    # à filtrer avant ce code
                self.nbEtudiant = len(self.data)
                print(f"Après self.retirerDoublonsEtEncadrants(), il y a {self.nbEtudiant} étudiant ou (2eme verif) {len(self.data)} étudiants. ")
                #input('1) presser entrée')
            else :
                pass # le fichier apogée est propre ! pas de doublons (...pour l'instant !!)

        # mélange aléatoire de la liste dans l'amphi


    def trierAlphaNom(self):
        """Trie les lignes en place sur la 2ᵉ colonne (insensible à la casse)."""
        def cle_tri(element):
            return element[1].lower()
        self.data.sort(key=cle_tri)


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
            else :
                print( "doublon : ",etu)

        print( f" Après filtrage {len(data_filtrée)} étudiants.\n")
        print( f" {len(self.data)-len(data_filtrée)} étudiants en double ou encadrant rétirés.\n")
        self.data = data_filtrée

    def get_nbEtudiant(self):
        self.nbEtudiant = len(self.data)
        return self.nbEtudiant

    def ajouteEtudiantAde(self, dataAde : list[str] ):

        def retirer_accents(txt: str) -> str:
            resultat = ""
            for c in unicodedata.normalize('NFD', txt):
                if unicodedata.category(c) != 'Mn':   # Mn = marque d'accent
                    resultat += c
            return resultat

        nomAde : str    = dataAde[1]
        prenomAde : str = dataAde[2]
        numeroAde : str = dataAde[0]

        nom    = retirer_accents(  nomAde.replace(" ","-").lower() )
        prenom = retirer_accents( prenomAde.replace(" ","-").lower() )
        courriel=f"{prenom}.{nom}@etu.univ-cotedazur.fr"

        newData : list[list[str]] =[ prenom , nom , numeroAde , courriel , "nil"]
        print(f"Ajout de {newData} dans la liste qui contient actuellement {len(self.data)} étudiants.")
        self.data.append(newData)


    def miseAJourData(self,dataFiltree : list[list[str]] ) :
        self.data=dataFiltree
        self.nbEtudiant = len(self.data or [])

    def choisir_fichier(self, tkParent, titre, rep) -> None:
        messagebox.showwarning(
            title=f"Sélection du fichier {self.formatFic} - {self.msgChoixFichier} ",
            message=f"Choisir un fichier {self.formatFic} {self.msgChoixFichier} au format Csv."
        )
        self.chemin: str = filedialog.askopenfilename(
            title=titre + f" - {self.msgChoixFichier}",
            initialdir='.',
            filetypes=[("Fichiers csv", "*.csv")],
        )

        if self.chemin == "":
            # aucun fichier choisi
            messagebox.showwarning(
                title="Attention !!!!",
                message="Vous n'avez pas choisi de fichier !!"
            )
            self.annule = True
            return
        else:
            # on connaît le répertoire du fichier choisi
            self.repertoire = os.path.dirname(self.chemin)

            # ─────────────────────────────────────────────
            # 1) Vérifier l'existence de Z_dataMail.csv
            # ─────────────────────────────────────────────
            chemin_data_mail = os.path.join(self.repertoire, "Z_dataMail.csv")

            if os.path.exists(chemin_data_mail):
                # Une session d'envoi/placement existe déjà
                # Fenêtre de confirmation : continuer ou annuler
                reponse = messagebox.askquestion(
                    title="Placement déjà commencé",
                    message=(
                        "Un placement est déjà commencé dans ce répertoire.\n\n"
                        "Voulez-vous effacer l'ancien et effectuer le nouveau placement(cliquer OUI )\n"
                        "ou revenir à la page précédente (cliquer NON) ?"
                    ),
                    icon="warning"
                )

                if reponse == "no":
                    # Bouton 'Annuler' → on annule le choix et on 'sort de la classe'
                    # en remettant chemin à vide
                    self.chemin = ""
                    self.repertoire = None
                    self.annule = True 
                    return
                else :       # on efface le fichier Z_dataMail.csv et on continue
                        os.remove(chemin_data_mail)
                # Si reponse == "yes" → bouton 'Continuer'
                # On ne fait rien de plus : la méthode retourne,
                # et l'initialisation de la classe continue normalement.


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
        print(self.formatFic, entete[1])
        if self.formatFic=="Apogée" :
            self.valide = (entete[1] == "DHH_DEB_PES" )
            print(self.formatFic, entete[1], self.valide)
        elif self.formatFic== "Moodle" :
            self.valide = ( entete[1]=='Nom de famille')
        elif self.formatFic== "Ade" :
            self.valide = ( entete[1]=='Nom')
        else :
            self.valide=False




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
    mode: str                              # "Examen" ou "Partiel" ou "PartielAde"
    apogee   : FichierCsv                     # peut être vide en mode Partiel
    moodle   : FichierCsv
    moodleTt : FichierCsv
    ade      : FichierCsv

    def __init__(self,mode : str ,tkparent : tk.Tk ):
        self.mode = mode   # "Examen" ou "Partiel" ou "PartielAde"
        # Initialisation systématique des attributs pour éviter plantage de mainClasse2.py
        self.apogee = None
        self.moodle = None
        self.moodleTt = None
        self.ade = None

        if self.mode == "Examen" : # chargement des 2 sources d'information (Apogée et Moodle pour les mails).
            self.apogee = FichierCsv(formatFic="Apogée",msgChoixFichier="avec tous les étudiants")  # les tiers temps sont déja placé dans Apogée
            if self.apogee.annule :
                return # si annulation du choix du fichier apogée
            random.shuffle(self.apogee.data)  # mélange aléatoire de la liste des étudiants 
            print("Le fichier apogée contient :", self.apogee.get_nbEtudiant(),'étudiants')
            #input('2) presser entrée')
            self.moodle = FichierCsv(formatFic="Moodle", msgChoixFichier="avec tous les étudiants")
            print("Le fichier apogée contient :", self.apogee.get_nbEtudiant())
            print("Le fichier moodle contient :", self.moodle.get_nbEtudiant())
            
        elif self.mode == "Partiel" :
            self.apogee = None
            self.moodle = FichierCsv(formatFic="Moodle", msgChoixFichier="avec tous les étudiants")
            if self.moodle.annule :
                return # si annulation du choix du fichier moodle
            random.shuffle(self.moodle.data)  # mélange aléatoire de la liste des étudiants   
            
            tiersTemps : str = messagebox.askquestion("Tiers temps ?","Avez-vous un fichier tiers temps ?",icon ='question' )
            if tiersTemps=='yes':
                self.moodleTt = FichierCsv(formatFic="Moodle",msgChoixFichier="contenant seulement les tiers temps")
                random.shuffle(self.moodleTt.data)  # mélange aléatoire de la liste des étudiants 
                self.retirerLesTiersTempsDeMoodle()
            else :
                self.moodleTt = None

        elif self.mode == "PartielAde" :
            self.apogee = None
            self.ade = FichierCsv(formatFic="Ade", msgChoixFichier="avec uniquement les étudiants inscrits à jour dans ADE ")
            if self.ade.annule :
                return # si annulation du choix du fichier ade  

            self.moodle = FichierCsv(formatFic="Moodle", msgChoixFichier=" avec tous les étudiants, pour avoir les mails.")
            if self.moodle.annule :
                return # si annulation du choix du fichier moodle
            random.shuffle(self.moodle.data)  # mélange aléatoire de la liste des étudiants   
            
            print(f"ligne 303 ade contient :  {len(self.ade.data)}  étudiants.")
            print(f"ligne 304 moodle contient :  {len(self.moodle.data)}  étudiants.")

            numeroAde: set[str] = {etu[0] for etu in self.ade.data} # ensemble des numéros étudiant de ADE.
            # on sauvegarde dans un fichier les étudiants qui ne sont pas dans ADE.
            numeroMoodle  : set[str] = {etu[2] for etu in self.moodle.data} # ensemble des numéros étudiant de Moodle.
            numeroAEffacer = numeroMoodle - numeroAde
            listeAeffacer= [etu for etu in self.moodle.data if etu[2] in numeroAEffacer]

            print( self.moodle.repertoire+'/Z_etudiants_dans_moodle_mais_pas_dans_ADE.csv')
            sauveCsv(nomFic= self.moodle.repertoire+'/Z_etudiants_dans_moodle_mais_pas_dans_ADE.csv',
                    entete = self.moodle.entete  ,
                    lignes = listeAeffacer)


            # on ne garde que les étudiants de la liste issue de ADE
            self.gardeLesNumeros( numeroAde , self.moodle )
            print(f"ligne 235 : moodle contient :  {len(self.moodle.data)}  étudiants.")

            tiersTemps : str = messagebox.askquestion("Tiers temps ?","Avez-vous un fichier tiers temps ?",icon ='question' )

            if tiersTemps=='yes':
                self.moodleTt = FichierCsv(formatFic="Moodle",msgChoixFichier="contenant seulement les tiers temps")
                print(f"linge 241 moodleTt contient :  {len(self.moodleTt.data)}  étudiants.")
                numeroTiersTemps : set[str] =  {etu[2] for etu in self.moodleTt.data} # pour après le test
                self.gardeLesNumeros( numeroAde , self.moodleTt ) # retrait des fantômes de la liste Tiers Temps
                print(f"linge 244 moodleTt contient :  {len(self.moodleTt.data)}  étudiants.")
            else :
                self.moodleTt=None
                numeroTiersTemps : set[str] = set()
            # on retire de la liste principale les étudiants Tiers Temps
            numeroListePrincipale : set[str] = numeroAde - numeroTiersTemps
            self.gardeLesNumeros( numeroListePrincipale , self.moodle)
            print(f"ligne 252  : La liste principale après retrait des tiers temps contient {len(self.moodle.data) }étudiant(e)s")

            # cas où des étudiants sont dans ADE mais pas encore dans Moodle :
            if len(self.ade.data)> len(self.moodle.data) + len(numeroTiersTemps) :
                nManquant : int = len(self.ade.data) - len(self.moodle.data) - len(numeroTiersTemps)
                messagebox.showwarning( title="Attention !!!!",
                message=f"Il manque {nManquant} étudiant(es) dans Moodle. La liste principale va être complétée.")
                self.completeListeMoodleAvecAde()
                print(f"La liste principale après ajout des étudiants d'ADE contient {len(self.moodle.data)}étudiant(e)s")

    def completeListeMoodleAvecAde(self):
        numeroAde        : set[str] = {etu[0] for etu in self.ade.data}
        numeroMoodle     : set[str] = {etu[2] for etu in self.moodle.data}
        if self.moodleTt!=None :
            numeroTiersTemps : set[str] = {etu[2] for etu in self.moodleTt.data}
        else :
            numeroTiersTemps=set()

        numeroManquant = numeroAde - numeroMoodle - numeroTiersTemps
        listeManquant : list[list[str]] =[ etu for etu in  self.ade.data if etu[0] in numeroManquant ]
        for etu in listeManquant:
            print( f"{etu} va être ajouté à la liste principale.")
            self.moodle.ajouteEtudiantAde(etu)


    def gardeLesNumeros(self, numeroRef : set[str], ficCsv : FichierCsv ):
        data_filtrees : list[list [str]]= []
        nb_suppr : int = 0
        avant= len(ficCsv.data)
        for etu in ficCsv.data:
            nmr : str = etu[2]
            if (nmr not in numeroRef) and (nmr!=""):
                nb_suppr = nb_suppr + 1
                print("retrait de ",etu,"\n")
            else:
                data_filtrees.append(etu) # on garde l'étudiant .
        apres = len(data_filtrees)

        ficCsv.miseAJourData(data_filtrees)
        print(f" {avant-apres } étudiant(s) fantômes retirés la liste  qui contient maintenant {ficCsv.get_nbEtudiant()} étudiants.")


    def retirerLesTiersTempsDeMoodle(self):
        """Retire de l'attribut moodle les étudiants tiers temps s'il y en a.
        à faire en dehors de la classe fichierCsv car il faut les données moodle et moodle Tiers Temps."""
        numeros_tt : set[str] = {etu[2] for etu in self.moodleTt.data} # ensemble des numéros Tier Temps.
        print(f"\n\n Pour le retrait des tiers temps de la liste principale, il y a {len(self.moodleTt.data)} étudiants tiers temps.")

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
        print(f"La liste principale contient {self.moodle.get_nbEtudiant()} étudiants.")
        print(f"Il y a en plus {self.moodleTt.get_nbEtudiant()} Tiers Temps.\n")
        print(f"Soit un total de {self.moodle.get_nbEtudiant()}+{self.moodleTt.get_nbEtudiant()}"
              f" ={self.moodle.get_nbEtudiant() + self.moodleTt.get_nbEtudiant() } ")

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
