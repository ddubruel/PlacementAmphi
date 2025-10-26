import csv
import tkinter as tk
from tkinter import messagebox, filedialog
from dataclasses import  dataclass 
from classes.module_classe_test import dataOK
# from classes.classe_fusionDataMoodleApogee import fusionDataMoodleApogee
# 
# from utils.chargeCsv import lit_fichier_csv_et_separe_entete
# from utils.traitementListe import majuscule
# from utils.afficheConsigne import afficheConsigne
# from classes.classe_choixAmphi import choixAmphi

# ────────────────────────────────────────────────────────────────────────────────
# Modèles de données
# ────────────────────────────────────────────────────────────────────────────────

@dataclass
class FichierCSV:
    chemin: Optional[str] = None
    entete: Optional[List[str]] = None
    data: Optional[List[List[str]]] = None
    valide : Optional[bool] = None     # validé par 'donneeValide'

    def modifier_attribut(self, nom_attribut: str, valeur) -> None:
        """
        Modifie dynamiquement un attribut de l'objet en utilisant son nom.
        Exemple : self.modifier_attribut("chemin", "data/moodle.csv")
        """
        if not hasattr(self, nom_attribut):
            raise AttributeError(f"L'attribut '{nom_attribut}' n'existe pas dans {self.__class__.__name__}")

        setattr(self, nom_attribut, valeur)
            

@dataclass
class ChargementCSV:
    mode: str                              # "Examen" ou "Partiel"
    apogee: FichierCSV                     # peut être vide en mode Partiel
    moodle: FichierCSV

    def modifier_attribut(self, nom_attribut: str, valeur) -> None:
        """
        Modifie dynamiquement un attribut de l'objet en utilisant son nom.
        Exemple : self.modifier_attribut("mode", "Examen")
        """
        if not hasattr(self, nom_attribut):
            raise AttributeError(f"L'attribut '{nom_attribut}' n'existe pas dans {self.__class__.__name__}")

        setattr(self, nom_attribut, valeur)

# ────────────────────────────────────────────────────────────────────────────────
# Fin Modèles de données
# ────────────────────────────────────────────────────────────────────────────────
def choisir_fichier_csv(tkParent ,  titre ,rep=".")-> str :
    #window : tk.Tk = tk.Toplevel(tkParent)
    #window.withdraw()  # Ne pas afficher cette fenêtre secondaire

    nom_fichier : str  = filedialog.askopenfilename(
                title=titre,
                initialdir='.',
                filetypes=[("Fichiers CSV", "*.csv")],
                        )
    if nom_fichier =="" :
        messagebox.showwarning( title="Sélection du fichier",
            message=f"Vous n'avez pas choisi de fichier !!")

    return nom_fichier


def demandeNomFichier(etape : str , choix : str ,tkParent : tk.Tk )-> str :
    # lance le selecteur de fichier et renvoie le
    messagebox.showwarning( title="Sélection du fichier",
                               message=f"{etape} :choisir un fichier issu de {choix} au format CSV (puis cliquer OK).")
    
    nomFic = choisir_fichier_csv(tkParent=tkParent , titre="{etape} : Chargement du fichier {choix}")

    return nomFic


def chargeFichierCsv(nomFic : str ) -> tuple[ list[str], list[list[str]] ]:      
    # ouverture
    fichier : TextIOWrapper = open(nomFic, "r", encoding="utf-8")
    fichier = open(nomFic, "r", encoding="utf-8")
    # recherche du séparateur
    debut = fichier.read(4096) # lit 4096 premiers caractères du fichier 
    fichier.seek(0)  # ramène le pointeur de lecture au début pour appeler csv.reader après
    dialect = csv.Sniffer().sniff(debut, delimiters=[',',';','\t','|']) # détection
    # lecture avec le délimiteur trouvé : 
    reader = csv.reader(fichier, delimiter=dialect.delimiter) # lecture du csv avec ce délimiteur
    # conversion en liste :
    lignes: list[list[str]] = []
    for ligne in reader:
        lignes.append(ligne)  # Ajouter chaque ligne à la liste
    fichier.close()    #fermeture. 
    
    entete : list[str] = lignes[0]
    data: list[list[str]] = lignes[1:]
    return entete, data


def donneeValide(nomFichier : str , entete : list[str], nature : str  , critere : str )-> bool :
    if critere not in entete :
        messagebox.showwarning( title="Erreur de fichier",
                               message=f"Erreur, vous n'avez pas choisi un fichier {nature} au format CSV (à vérifier !).")
        return False
    return True
    

def charger_depuis_csv(choix : str , root : tk.Tk ) :
    # choix contient "Examen"(pour charger apogée et Moodle) ou "Partiel" pour charger que Moodle)
    # cette fonction est appellée depuis l'UI.
    #
     # Prépare les conteneurs pour le return    
    dataApogee = FichierCSV()
    dataMoodle = FichierCSV()
    chargementDataBrut = ChargementCSV()
    
    chargementDataBrut.modifier_attribut("mode", choix)
    
    
    # Demande des noms des fichiers *.csv :
    if choix=="Examen" :
        nomFicApogee : str = demandeNomFichier(etape="Etape 1 :",  choix="Apogée" , tkParent=root)
        nomFicMoodle : str = demandeNomFichier(etape="Etape 2 :", choix="Moodle" , tkParent=root)
    else :
        nomFicMoodle : str = demandeNomFichier( etape="Etape 1 :", choix="Moodle" , tkParent=root)
    
    # maj conteneurs    
    dataApogee.modifier_attribut("chemin", nomFicApogee)
    dataMoodle.modifier_attribut("chemin", nomFicMoodle)
       
    # chargement des données :
    if choix=="Examen" :
        enteteApogee, listeApogee = chargeFichierCsv(nomFicApogee)
        enteteMoodle, listeMoodle = chargeFichierCsv(nomFicMoodle)
    else :
        enteteApogee, listeApogee = [] ,[]
        enteteMoodle, listeMoodle = chargeFichierCsv(nomFicMoodle)
    
    # maj conteneurs    
    dataApogee.modifier_attribut("entete", enteteApogee)
    dataMoodle.modifier_attribut("entete", enteteMoodle)
    
    dataApogee.modifier_attribut("data", listeApogee)
    dataMoodle.modifier_attribut("data", listeMoodle)
        
    # analyse de la validité et affichage warning si besoin
    if choix=="Examen" :
        dataOkApogee : bool = donneeValide(nomFichier =nomFicApogee,
                                          entete = enteteApogee,
                                          nature="Apogée" ,
                                          critere="COD_EPR")
    else :
        dataOkApogee : bool = False 
    # en dehors du test, à faire dans les 2 cas.
    dataOkMoodle : bool =donneeValide(nomFichier =nomFicMoodle,
                                          entete = enteteMoodle,
                                          nature="Moodle" ,
                                          critere="Nom de famille")
    
    dataApogee.modifier_attribut("valide", dataOkApogee)
    dataMoodle.modifier_attribut("valide", dataOkMoodle) 
    
    chargementDataBrut.modifier_attribut("apogee", dataApogee)
    chargementDataBrut.modifier_attribut("moodle", dataMoodle)
    
    return chargementDataBrut

####
#### Ancienne classe appellée par l'ancienne fonction  chargedonnée
####
class Examen:
    def __init__(self, parent):
        self.parent = parent  # l'instance de BoustrophedonStructure
        self.root : tk.Tk  = parent.root # pour permettre à la méthode fusionDataMoodleApogee
                                # d’utiliser cette fenêtre comme contexte graphique pour des messages
        # à récupérer depuis main après :
        self.cheminDuFichierApogee : str =""
        self.dictCheminAbsolus : dict[tuple[str, str], str] = {}  # le dictionnaire avec les chemins absolu
                                         # la clé est un tuple (nom amphi , '2_csv_out') par exemple et
                                         # la valeur une chaine avec le chemin vers le fichier
        
        # liste des étudiants répartis par amphithéâtre :
        # [ [ [Prenom, Nom, Numéro, mail, ordre VS, Amphi], ...], ... ]
        self.listeEtuRepartisDansAmphis : list[list[list[str]]] =[] # liste regroupant les listes par amphi
                # cette liste est remplie par la méthode chargement ci-après
        # fin de la recup
        self.dataMoodleEtApogee : fusionDataMoodleApogee | None  = None # None au départ seulement.

        self.chargement()
                
        
    def chargement(self):
        # charge le fichier Apogée puis le fichier Moodle
        chemin = fusionDataMoodleApogee(self.root)
        self.dataMoodleEtApogee = chemin
                                
        # les valeurs mises à jour sont passées à la classe parent (Boustrophedon)
        self.cheminDuFichierApogee      = chemin.cheminDuFichierApogee
        # dictionnaire avec l'arborescence de tous les fichiers créés.
        self.dictCheminAbsolus = chemin.dictCheminAbsolus
        
        self.parent.listeDesAmphi     = chemin.listeDesAmphi

        for nomAmphi in self.parent.listeDesAmphi:
            # rechargement du fichier contenant la liste pour un seul amphi
            #(celui de la boucle en cours ici !)
            cheminRepListeEtu : str = self.dictCheminAbsolus[(nomAmphi, '2_csv_out')]
            nomCsv : str = cheminRepListeEtu + '/' + f"liste_Etudiants_amphi_{nomAmphi}.csv"
            # on charge la liste pour l'amphi en paramètre de la boucle.
            listeEtu : list[list[str]] =[]
            entete : list[str] =[]
            listeEtu  , entete  = lit_fichier_csv_et_separe_entete(nomCsv)
            # mise en forme
            listeEtu = majuscule(listeEtu)            
            self.listeEtuRepartisDansAmphis.append(listeEtu)

    def liste_attributs(self):
        """Retourne la liste des noms d'attributs de l'objet."""
        return list(self.__dict__.keys())
    
    def __repr__(self):
        attrs = "\n  ".join(f"{k} = {v!r}" for k, v in self.__dict__.items())
        Liste_att = self.liste_attributs()
        return f"<{self.__class__.__name__}(\n  {attrs}\n Les noms des attributs sans les valeurs : \n{Liste_att})>"
    
    





def chargerDonnees(self): # méthode utilisée par interfaceChargementEtTraitement  
            if self.choix.get() == "Examen":
                self.sourceMoodle = True 
                self.sourceApogee = True 
                # Examen remplis l'attribut de la classe Boustrophedon 
                # self.listeEtuRepartisDansAmphis : list[list[list[str]]] =[]
                             # la liste des étudiants pour tous les amphi
                             # qui contient une liste par amphi
                             # chaque liste pour un amphi contient un ligne(liste)
                             # les lignes sont les data (str) d'un étudiant
                data=Examen(self)
                # récupération des attributs définis dans l'instance data d 'Examen
                self.cheminDuFichierApogee : str  = data.cheminDuFichierApogee
                self.dictCheminAbsolus : dict[str,str]  = data.dictCheminAbsolus  # a modifier pas bien !!!
                self.listeEtuRepartisDansAmphis : list[list[str]]= data.listeEtuRepartisDansAmphis
                self.dataMoodleEtApogee = data.dataMoodleEtApogee
                                                         
                # remplissage des n amphi à partir des
                # data contenues dans  self.listeEtuRepartisDansAmphis))
                # chaque zone des amphi va recevoir le nombre ad'hoc d'étudiants
                # les références des places sont aussi à jour maintenant.
                data = creeEtRemplisLesAmphis(self.listeEtuRepartisDansAmphis)
                self.listeDesAmphiPleins=data.listeAmphisAvecEtudiants                
                # la visualisation graphique des amphis rapide sans les ellipses.
                for Amphi in self.listeDesAmphiPleins :
                    trace=tracePlanAmphiEtGenerefichier(Amphi,self)  # self porte le
                                                             #root et le dico des chemins.
                    self.listeFenetreGraphiqueVisuAmphi.append(trace.window)
                    
            elif self.choix.get() == "Partiel":
                self.nomFicMoodle = choisirFichierMoodle()
                self.dataMoodle, self.enteteMoodle = lit_fichier_csv_et_separe_entete_autodelim(self.nomFicMoodle)
                
                # APPEL DE LA NOUVELLE FONCTION OU CLASSE
            
            self.root.update_idletasks()  # rafraîchit l’interface avant de lancer le traitement
            self.bouton2.config(state="normal", bg="lightgreen")
            self.bouton3.config(state="normal")
            # fin de chargerDonnees
            
            