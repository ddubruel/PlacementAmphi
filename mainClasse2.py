import tkinter as tk
from tkinter import messagebox, filedialog

import os,sys

import time

from dataclasses import dataclass,fields 

# Ajoute le dossier "app" à sys.path pour permettre les imports relatifs propres
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, 'app'))
sys.path.insert(0, project_root)

from classes.c1_classe_chargementCsv import chargementCsv
from classes.c2_0_classeS_etudiant_a_amphi import amphi,etudiant
from classes.c3_classe_arborescence import arborescence
from classes.c4_classe_definitPlacementDansAmphi import definitPlacementDansAmphi
from classes.c5_tracePlanAmphiEtGenerefichier import tracePlanAmphiEtGenerefichier
from classes.c7_classe_codeEnteteApoge import codeEnteteApogee
from classes.c8_classe_mailConfig import mailConfig
from classes.c9_classe_dataEpreuve import dataEpreuve
from classes.c10_classe_compileClasseMail import compileClasseMail
#from classes.c11_classe_compilClasseMailAvecReprise import compilClasseMailAvecReprise


from utils.utilitaires import *
from utils.utilitaire_UI_amphiMoodle import definitRemplissage
from utils.utilitaire_completeDefAmphi import completeDefinitionAmphi
from utils.utilitaires_bouton2 import *
from utils.utilitaire_generer_et_compiler_fichier_tex import genererPdf
from utils.utilitaire_UI_saisirDonneesEpreuve import UI_saisirDonneesEpreuve
from utils.utilitaire_UI_mail import UI_mail
from utils.UI_preparation_message import UI_preparation_message
from utils.UI_confirmationEnvoi import UI_confirmationEnvoi
from utils.utilitaire_sauvegarde import charger_compileClasseMail
from utils.utilitaire_json import charger_donnees_message, choisirFichierPoursuite, sauvegarderJson
from utils.utilitaire_sauvegarde import sauvegarder_compileClasseMail



from utils.utilitaire_reprise_envoi_mail import envoiMailauxEtudiants


# ---------- Modèle ----------
@dataclass
class EtatProjet:
    charge: bool = False           # données chargées ?
    mode: str = "nil"              # "Examen" ou "Partiel"

# ---------- Application ----------
class Boustrophedon:
    def __init__(self,root):
        # état (modèle)
        self.etat : EtatProjet = EtatProjet()

        # Vue (fenêtre)
        self.root = root
        self.root.title("Boustrophedon")

        # variables :
        self.dataBrutes : chargementCsv = None
        self.nbAmphiApogee : int = 0
        self.listeNomAmphi : list[amphi]=[]
        self.listeDesRepartitions : list =[]
        self.listAmphi : list[amphi] = [] 
        
        self.listeFenetreGraphiqueVisuAmphi = []
        
        # Construire l'UI
        self.build_header1()
        self.build_controls_part1()
        
        self.build_header2()
        self.build_controls_part2()
        self.build_buttons()
        
        
        self.update_buttons_state("initial")

        # Boucle principale
        self.root.mainloop()

    # ----- Vue : entête -----
    def build_header1(self):
        tk.Label(
            self.root,
            text  ="Choisissez vos données de référence pour un nouveau projet :",
            font =("Arial", 11, "bold")
        ).pack(pady=10)
        tk.Label(
            text  ="APOGÉE (fournit par la scolarité avant un examen).",
            font =("Arial", 10)
        ).pack(pady=10)
        tk.Label(
            text  ="ADE (liste filtrée par Olivier avec la liste à jour des étudiants).",
            font =("Arial", 10)
        ).pack(pady=10)
        tk.Label(
            text  ="MOODLE (Il peut y avoir des doctorants ou des étudiants désinscrits d'ADE).",
            font =("Arial", 10)
        ).pack(pady=10)
        
    def build_header2(self):
        tk.Label(
            self.root,
            text  ="ou : Poursuivez un projet existant",
            font =("Arial", 11, "bold")
        ).pack(pady=10)
        tk.Label(
            text  ="Vous voulez poursuivre l'envoi des courriels aux étudiants.",
            font =("Arial", 10)
        ).pack(pady=10)
        
        
    # ----- Vue : contrôles (radio) -----
    def build_controls_part1(self):
        frame_radio = tk.Frame(self.root)
        frame_radio.pack(pady=10)

        self.var_mode = tk.StringVar(value=self.etat.mode)
        # nouvelle variable dédiée au bouton "Poursuite"
        self.var_poursuite = tk.BooleanVar(value=False)

        # Radiobuttons "classiques" (APOGÉE / ADE / MOODLE)
        tk.Radiobutton(
            frame_radio, text="APOGÉE (examen)",
            variable=self.var_mode, value="Examen",
            command=self.on_mode_clicked           
        ).pack(side="left", padx=10)

        tk.Radiobutton(
            frame_radio, text="ADE (partiel)",
            variable=self.var_mode, value="PartielAde",
            command=self.on_mode_clicked           
        ).pack(side="left", padx=10)

        tk.Radiobutton(
            frame_radio, text="MOODLE (partiel)",
            variable=self.var_mode, value="Partiel",
            command=self.on_mode_clicked           
        ).pack(side="left", padx=10)

    # ----- Vue : contrôles (radio) -----
    def build_controls_part2(self):
        # Bouton "Poursuite d'un projet existant"
        frame_radio2 = tk.Frame(self.root)
        frame_radio2.pack(pady=10)

        tk.Radiobutton(
            frame_radio2,
            text="Poursuite d'un projet existant",
            variable=self.var_poursuite,
            value=True,
            command=self.on_poursuite_clicked      
        ).pack(side="bottom", pady=10)

        

    # ----- Vue : boutons d’actions -----
    def build_buttons(self):
        self.btn_load = tk.Button(
            self.root,
            text="Chargement des données et visualisation des amphis remplis",
            command=self.chargerDonnees
        )
        self.btn_load.pack(pady=10)

        self.btn_pdf = tk.Button(
            self.root,
            text="Générer les fichiers PDF des listes d'émargement",
            command=self.actionsBouton3,
            state=tk.DISABLED
        )
        self.btn_pdf.pack(pady=10)

        self.btn_png = tk.Button(
            self.root,
            text=("Générer les fichiers *.png \n (pièces joîntes des mails) \n des places individuelles.\n"
                    "Cette opération peut être longue(1 min pour 120 étudiants ).\n"),
            command=self.actionsBouton2,
            state=tk.DISABLED
        )
        self.btn_png.pack(pady=10)

        self.btn_sauvegarde = tk.Button(
            self.root,
            text="Sauvegarder la répartition ",
            command=self.actionsBoutonSauvegarde,
            state=tk.DISABLED
        )
        self.btn_sauvegarde.pack(pady=10)

        self.btn_mail = tk.Button(
            self.root,
            text="Envoyer les fichiers individuels aux étudiants par mail",
            command=self.prepareEnvoiMailsAvecClasses,
            state=tk.DISABLED
        )
        self.btn_mail.pack(pady=10)
        
        
        self.btn_poursuite = tk.Button(
            self.root,
            text="Poursuivre l'envoi des courriels.",
            command=self.prepareRepriseEnvoiMailsAvecFichier,
            state=tk.DISABLED
        )
        self.btn_poursuite.pack(pady=10)
        
        tk.Button(self.root, text="Quitter  ", command=self.root.destroy).pack(pady=10)
        
    # ----- Contrôleur : logique -----
    def on_mode_selected(self):
        # Met à jour l'état interne
        self.etat.mode = self.var_mode.get()        
        # Exécute l'action demandée
        self.update_buttons_state("choixModeFait")

    def on_mode_clicked(self):
        """
        Appelé quand on clique sur APOGÉE / ADE / MOODLE.
        - Décoche 'Poursuite'
        - Puis applique la logique habituelle (on_mode_selected).
        """
        self.var_poursuite.set(False)   # décocher le bouton 'Poursuite'
        self.on_mode_selected()         # garde votre logique existante

    def on_poursuite_clicked(self):
        """
        Appelé quand on clique sur 'Poursuite d'un projet existant'.
        - Décoche les trois autres Radiobuttons (APOGÉE / ADE / MOODLE)
        - Ne touche PAS à l'état des boutons de chargement.
        """
        # Met la variable des 3 radios sur une valeur qui ne correspond à aucun d’eux
        # ils se retrouvent tous décochés
        self.var_mode.set("nil")
        self.update_buttons_state(etape="poursuite")


    
    def update_buttons_state(self, etape="initial"):
        if etape == "initial":
            self.btn_load.config(state=tk.DISABLED)
            self.btn_png.config(state=tk.DISABLED)
            self.btn_pdf.config(state=tk.DISABLED)
            self.btn_mail.config(state=tk.DISABLED)
            self.btn_poursuite.config(state=tk.DISABLED)
        elif etape== "choixModeFait":
            self.btn_load.config(state=tk.NORMAL)
            self.btn_png.config(state=tk.DISABLED)
            self.btn_pdf.config(state=tk.DISABLED)
            self.btn_mail.config(state=tk.DISABLED)
            self.btn_poursuite.config(state=tk.DISABLED)
        elif etape=="poursuite":
            self.btn_load.config(state=tk.DISABLED)
            self.btn_png.config(state=tk.DISABLED)
            self.btn_pdf.config(state=tk.DISABLED)
            self.btn_mail.config(state=tk.DISABLED)
            self.btn_poursuite.config(state=tk.NORMAL)                      
        elif etape == "donnees_chargees":
            self.action2finie : bool = False  # pour pouvoir zapper la gnération des png.
            
            self.btn_pdf.config(state=tk.NORMAL)
        elif etape == "png_genere":
            self.btn_pdf.config(state=tk.NORMAL)
            self.action2finie : bool = True # pour ne pas re instancier les rangs. Cela vient d'être fait.
            self.btn_sauvegarde.config(state=tk.NORMAL)
            self.btn_mail.config(state=tk.DISABLED)
        elif  etape== "sauvegarde_faite":
            self.btn_mail.config(state=tk.NORMAL)
        elif etape == "pdf_generes": 
            self.btn_png.config(state=tk.NORMAL)
            
    
    def exploiteApogee(self):
        """ configure les données d'Apogée dans les classe Amphi (y dépose la liste des étudiants)"""
        # Fais le compte des amphi vides et  de la liste de nom des amphis
        self.nbAmphiApogee ,  self.listeNomAmphi  = compteEtListeAmphiApogee(self.dataBrutes)
        print(f" Le fichier apogée contient {self.nbAmphiApogee} amphi(s) dont les noms sont {self.listeNomAmphi}.\n ") 

        # création de l'arborescence des fichiers à partir de l'emplacement du fichier moodle            
        self.arborescence = arborescence( self.dataBrutes.apogee.chemin, self.listeNomAmphi )
        print(  f"L'arborescence des fichiers est créée.\n Les fichiers de sortie se "
                f"trouvent dans le répertoire :\n {self.dataBrutes.apogee.chemin}.\n"
                f"Chaque répertoire porte le nom de l'amphithéatre utilisé.\n")
        
        # utilisation : chemin_png = self.arborescence.get_chemin(nom_amphi, "pngOut")
    
        # instanciation des amphi
        self.listAmphi : list [ amphi] =[] 
        for nom in  self.listeNomAmphi :                
            self.listAmphi.append( amphi(nom) )   # création des n amphis du fichier apogée...amphi à peupler.
        print( f"Création des instances amphi. Vérification des noms des amphis créés :\n {[ amphi.nom for amphi in self.listAmphi ]}\n\n" )
        
        # affectation des étudiants dans les amphi : avec apogee, recherche des étudiants par amphi
        for amphitheatre in self.listAmphi :
                            
            extraitApogee : list[list[str]] = filtreApogee(dataBrutes = self.dataBrutes , nomAmphi = amphitheatre.nom )
            print(f"L'amphithéatre {amphitheatre.nom} contient  {len(extraitApogee)} étudiants d'après les données apogée.\n"  )
            
            enteteApogee : list[str] = self.dataBrutes.apogee.entete
            try :
                indexNomEtu : int = enteteApogee.index("LIB_NOM_PAT_IND")
                indexPrenomEtu : int = enteteApogee.index("LIB_PR1_IND")
                indexNumEtu : int = enteteApogee.index("COD_ETU") 
            except :
                raise ValueError("Le fichier Apogée ne contient pas les bons en-têtes. Revoir le fichier Apogée.")
            
            for dataEtu in extraitApogee :                                
                nomEtu  : str = dataEtu[indexNomEtu]
                prenomEtu : str = dataEtu[indexPrenomEtu]
                numeroEtu : str = dataEtu[indexNumEtu]                                     
                amphitheatre.ajouteEtudiant(etudiant(nom = nomEtu ,
                                                    prenom = prenomEtu,
                                                    numeroEtudiant = numeroEtu,
                                                    courriel=""
                                                    ) 
                                            )
            
            print(f"L'amphithéatre {amphitheatre.nom} a reçu {len(amphitheatre.listeTousLesEtudiantsDansAmphi)} instances d'étudiants.\n")
            
            # les étudiants issus de apogee n'ont pas de courriel (à récupérer dans les data Moodle).
            for etu in amphitheatre.listeTousLesEtudiantsDansAmphi :
                courriel : str  = recupereCourrielMoodle( numeroEtuApogee = etu.numeroEtudiant
                                                        , dataBrutes =   self.dataBrutes )                    
                etu.set_courriel(courriel)
            print(f"Affichage du premier étudiant de l'amphi : {amphitheatre.nom}. \n"
                    f"{[etud for etud in amphitheatre.listeTousLesEtudiantsDansAmphi[:1] ] } \n" )
        # fin exploiteApogee(self)
        
    def exploiteMoodle(self):
        """configure les données Moodle dans les classe Amphi (y dépose la liste des étudiants)"""
        if   self.dataBrutes.moodleTt != None :
            nb_TT : int = len(self.dataBrutes.moodleTt.data)
        else :
            nb_TT: int = 0 
        # on place la totalité des étudiant en liste moodle+ le nb de tiers Temps. Il faut cocher la case Amphi pour les TT
        nbTotalEtudiant : int =  len(self.dataBrutes.moodle.data)+nb_TT
        allocationAmphi : list[tuple[str,int]] = definitRemplissage(nb_etudiants= nbTotalEtudiant,nb_tiers_temps = nb_TT, parent=self.root)    
        print(f"Vous avez choisi la répartition suivante dans les amphithéatres :\n {allocationAmphi}")
        # création de la liste des amphi :
        self.listeNomAmphi = [nom for (nom,nb,boolTT) in allocationAmphi ]
        # création de l'arborescence des fichiers à partir de l'emplacement du fichier moodle            
        self.arborescence = arborescence( self.dataBrutes.moodle.chemin, self.listeNomAmphi )
        print(f"L'arborescence des fichiers est créée.\n Les fichiers de sortie se "
                f"trouvent dans le répertoire :\n {self.dataBrutes.moodle.chemin}.\n"
                f"Chaque répertoire porte le nom de l'amphithéatre utilisé.\n")
        # instanciation des amphi
        self.listAmphi =[] 
        for nom in  self.listeNomAmphi :                
            self.listAmphi.append( amphi(nom) )   # création des n amphis du fichier apogée...amphi à peupler.
        print( f"Création des instances amphi. Vérification des noms des amphis créés :\n {[ amphi.nom for amphi in self.listAmphi ]}\n\n" )
        # affectation des étudiants dans les amphi :
        # pour un amphi sans tiers temps, on prend le nombre allouté (dans allocationAMphi )et les étudiants dans .moodle.data
        # pour un amphi avec tiers temps, on prend le nombre alloué auquel on retire le nombre de tiers temps
        #                                       on pioche la première partie dans  dataBrutes.moodle.data (Nalloué-Ntiers)
        #                                       et la deuxieme partie dans   dataBrutes.moodleTt.data (Ntiers) !!!
        #                                       on remplit ainsi l'amphi avec Nalloué-Ntiers + Ntiers = Nalloué 
        decalage : int =0 # pour récupérer la tranche suivante dans la liste dataBrutes.moodle.data
        for amphitheatre in self.listAmphi :
            listeValeursUniques  : list[tuple[int,bool]] = [(nomAmphi,valeur, boolTT)  for (nomAmphi, valeur ,boolTT) in allocationAmphi if nomAmphi==amphitheatre.nom ]
            nomAmphi : str = listeValeursUniques[0][0]
            nbEtudiantAPlacer : int = listeValeursUniques[0][1]
            TT : bool =  listeValeursUniques[0][2]
            if not TT : # si pas de tiers temps on place directement Nalloué soit nbEtudiantAPlacer depuis moodle.data
                dataEtudiantsAPlacer : list[list[str]] = self.dataBrutes.moodle.data[decalage:(decalage+nbEtudiantAPlacer)]
                decalage = decalage+nbEtudiantAPlacer # pour placer le pointeur sur le prochain étudiant dans la liste Moodle.
                for dataEtu in dataEtudiantsAPlacer :
                    amphitheatre.ajouteEtudiant(etudiant(nom = dataEtu[1] ,
                                                        prenom = dataEtu[0],
                                                        numeroEtudiant = dataEtu[2],
                                                        courriel=dataEtu[3]
                                                        ) 
                                                )
            else : # si tiers temps :
                dataEtudiantsAPlacer : list[list[str]] = self.dataBrutes.moodleTt.data # on prend toute la liste Tiers Temps.
                nb_tiersTemps : int = len(dataEtudiantsAPlacer)
                
                for dataEtu in dataEtudiantsAPlacer :
                    amphitheatre.ajouteEtudiant(etudiant(nom = dataEtu[1] ,
                                                        prenom = dataEtu[0],
                                                        numeroEtudiant = dataEtu[2],
                                                        courriel=dataEtu[3]
                                                        ) 
                                                )
                print(f"La liste de tiers temps est placée dans l'amphi {amphitheatre.nom}")
                
                # le complément dans l'amphi qui est pris dans la liste moodle.
                nb_complement = nbEtudiantAPlacer- nb_tiersTemps # on calcule les places restantes pour la liste Moodle.
                etudiantsAPlacer : list[list[str]] = self.dataBrutes.moodle.data[decalage:(decalage+nb_complement)]
                decalage = decalage+nb_complement # pour placer le pointeur sur le prochain étudiant dans la liste moodle.data
                for dataEtu in etudiantsAPlacer :
                    amphitheatre.ajouteEtudiant(etudiant(nom = dataEtu[1] ,
                                                        prenom = dataEtu[0],
                                                        numeroEtudiant = dataEtu[2],
                                                        courriel=dataEtu[3]
                                                        ) 
                                                )            
                print(f"{nbEtudiantAPlacer} étudiants dont {nb_tiersTemps} étudiants ont été placés dans l'amphi {nomAmphi}.") 
            
            print(f"L'Amphithéatre {amphitheatre.nom} a reçu {len(amphitheatre.listeTousLesEtudiantsDansAmphi)} instances d'étudiants.\n")
            #input("4) taper entrée")
        # fin exploiteMoodle(self)                
    
    
    
    def chargerDonnees(self):
        # lit le mode sélectionné dans l'UI.
        self.etat.mode = self.var_mode.get() or "nil"
        # instanciation de la classe qui contient les données brutes (Moodle et Apogee si Examen)
        self.dataBrutes = chargementCsv(self.etat.mode, self.root)
        # Si l'utilisateur a annulé dans choisir_fichier(), on arrête tout.
        if self.dataBrutes.apogee and self.dataBrutes.apogee.annule:
            return
        if self.dataBrutes.moodle and self.dataBrutes.moodle.annule:
            return
        if self.dataBrutes.ade and self.dataBrutes.ade.annule:
            return

        self.repertoire : str = (
                        self.dataBrutes.apogee.repertoire
                        if self.etat.mode == "Examen"
                        else self.dataBrutes.moodle.repertoire
                            )
        
        if self.dataBrutes.apogee : # exploitation des data apogee si Examen :
            self.exploiteApogee()
        else : # exploitation des data moodle si Partiel :
            self.exploiteMoodle()
        # A ce stade les amphi ont chacun leur liste d'étudiants non placés.
        
        for amphiEtu in  self.listAmphi :
            # on définit les zones de l'amphi 
            completeDefinitionAmphi(amphiEtu)
            # calcul des répartitions par amphi
            placement = definitPlacementDansAmphi(amphiEtu)
            repartition = placement.repartition
            #remplissage des zones de l'amphi
            indiceEtuDebut : int = 0
            listeARepartir=amphiEtu.listeTousLesEtudiantsDansAmphi
            for indiceZone , zone in enumerate(amphiEtu.zones) :
                indiceEtuFin : int = indiceEtuDebut + repartition[indiceZone]
                zone.set_listeDesEtudiantDansLaZone(listeARepartir[indiceEtuDebut:indiceEtuFin])
                indiceEtuDebut = indiceEtuFin                
            trace=tracePlanAmphiEtGenerefichier(amphiEtu,self.arborescence,self.root)                  
            self.listeFenetreGraphiqueVisuAmphi.append(trace.window)
        # A ce stade les zones des amphi ont chacune leur liste d'étudiants non placés.
        self.update_buttons_state("donnees_chargees")         


    def actionsBouton2(self):
        if len(self.listeFenetreGraphiqueVisuAmphi) !=0 :
            for fenetre in self.listeFenetreGraphiqueVisuAmphi:
                fenetre.destroy()

        for amphi in self.listAmphi :  
            genererLesPngPlacesIndividuelles(amphi,self.arborescence,self.root,self.listeFenetreGraphiqueVisuAmphi)
            
            remplitRangCompleteEtudiant(amphi) # voir utilitaries bouton 2.
            
        messagebox.showinfo("PNG", "Génération des images PNG terminée.")
        
        self.update_buttons_state("png_genere")
        
    def actionsBouton3(self):
        
        if len(self.listeFenetreGraphiqueVisuAmphi) !=0 :
            for fenetre in self.listeFenetreGraphiqueVisuAmphi:
                fenetre.destroy()
        
        if not(self.action2finie) : # si l'étape 2 , longue a été zappée.
            for amphi in self.listAmphi :
                remplitRangCompleteEtudiant(amphi)            
        # Générer PDF   LIB_SAL = self.nomAmphi                  
        if  self.etat.mode in ['Partiel' ,'PartielAde'] :
            entetePdf : list[str] = codeEnteteApogee(  self.etat.mode   , self.dataBrutes , self.listAmphi , "Nom provisoire", self.root )                                 
            
            annee_universitaire, date, horaires, duree, epreuve= UI_saisirDonneesEpreuve(self.root, self.repertoire )
            entetePdf.set_valeurs( annee_universitaire, date, horaires,duree, epreuve,  LIB_SAL="Nom provisoire")
            # on remplit les data à réutiliser pour envoyer le mail plus tard.
            self.dataEpreuvePourMail : dataEpreuve = dataEpreuve(date ,horaires ,duree ,epreuve)
        if self.etat.mode == 'Examen' : # écriture du json avec les données de l'épreuve pour un Examen 
                                        # UI_saisirDonneesEpreuve n'est pas utilisé car les données sont dans Apogée.
            annee_universitaire, date, horaires, duree, epreuve= recupDataEpreuveApogee( self.dataBrutes )
            sauvegarderJson(self.repertoire, annee_universitaire , date , horaires  , duree ,epreuve )
                    
        for Amphi in self.listAmphi :
            CheminRepTex : str  = self.arborescence.get_chemin(Amphi.nom, "texOut")
            CheminRepPdf : str = self.arborescence.get_chemin(Amphi.nom, "listes_Emargement_pdf")
            if self.etat.mode=='Examen' :# le LIB_SAL de l'amphi change à chaque amphi !!
                entetePdf : list[str] = codeEnteteApogee(  self.etat.mode   , self.dataBrutes , self.listAmphi , Amphi.nom, self.root )                                                
            else :
                entetePdf.set_LIB_SAL(Amphi.nom)
            # on remplit les data à réutiliser pour envoyer le mail plus tard.
            self.dataEpreuvePourMail : dataEpreuve = dataEpreuve(entetePdf.date ,entetePdf.horaires ,entetePdf.duree ,entetePdf.epreuve)
            genererPdf(Amphi , CheminRepTex , CheminRepPdf , entetePdf, self.root)                
        messagebox.showinfo("PDF", "Génération des PDF terminée.")
        self.update_buttons_state("pdf_generes")
        
    def actionsBoutonSauvegarde(self):
        # on instancie la classe de compilation des données pour l'envoi des mails
        # cette classe contient toutes les données nécessaires à l'envoi des mails.
        dataMail : compileClasseMail = compileClasseMail(self.listAmphi)
        # première sauvegarde de la classe dans le csv "Z_dataMail.csv" et "Z_dataMailEnvoiReel.csv"
        # qui seront chargés en cas de reprise.
        sauvegarder_compileClasseMail( dataMail,"Z_dataMail.csv", self.repertoire)   
        sauvegarder_compileClasseMail( dataMail,"Z_dataMailEnvoiReel.csv", self.repertoire)
        messagebox.showinfo("Répartition des étudiants",
                            f"La répartition est sauvegardée,\n"
                            f"vous pouvez quitter et reprendre plus tard.\n"
                            f"Sinon pouvez poursuive en cliquant sur \"Envoyer les fichiers\".")
        self.update_buttons_state("sauvegarde_faite")
        
    def prepareEnvoiMailsAvecClasses(self):
        """ Action du bouton 4 : envoi des mails aux étudiants."""
        # on instancie la classe de compilation des données pour l'envoi des mails
        # cette classe contient toutes les données nécessaires à l'envoi des mails.
        dataMail : compileClasseMail = compileClasseMail(self.listAmphi)
        # première sauvegarde de la classe dans le csv "Z_dataMail.csv" et "Z_dataMailEnvoiReel.csv"
        # qui seront chargés en cas de reprise.
        sauvegarder_compileClasseMail( dataMail,"Z_dataMail.csv", self.repertoire)   
        sauvegarder_compileClasseMail( dataMail,"Z_dataMailEnvoiReel.csv", self.repertoire)
        
        # definition du sujet et du corps commun du message
        # le fichier   Z_data_message.json avec le sujet et le corps du message sera créé à cette étape.
        sujet: str
        corpsDuMessageCommun: str
        sujet, corpsDuMessageCommun  = UI_preparation_message(self.root , self.dataEpreuvePourMail,self.repertoire )
        
        # pour le mot de passe et autres paramètres de connexion SMTP.
        setUpMail   = UI_mail(self.root) 
        # interface graphique pour savoir si envoi réel ou test à blanc...
        envoiReel : bool  = UI_confirmationEnvoi(self.root)                       
        # lancer la fonction d'envoi des mails avec reprise possible
        envoiMailauxEtudiants(self.root,self.repertoire,dataMail,setUpMail,sujet,corpsDuMessageCommun,envoiReel)
        
    def prepareRepriseEnvoiMailsAvecFichier(self):   
        """ Action du bouton  reprise envoi mail : envoi des mails aux étudiants.
        il faut d'avoir chargé le fichier de reprise avant."""
        self.repertoire = choisirFichierPoursuite (  )
        # charge le json avec le sujet et le corps du message sauvegardé au premier envoi.
        donnees = charger_donnees_message(self.repertoire)
        sujet= donnees["sujet"]
        corpsDuMessageCommun= donnees["corps"]
        # interface graphique pour savoir si envoi réel ou test à blanc...
        envoiReel : bool  = UI_confirmationEnvoi(self.root)
        if envoiReel :
            dataMail = charger_compileClasseMail(self.repertoire, "Z_dataMailEnvoiReel.csv")
        else :
            dataMail = charger_compileClasseMail(self.repertoire, "Z_dataMail.csv")
        # pour le mot de passe et autres paramètres de connexion SMTP.
        setUpMail   = UI_mail(self.root)
        
        # lancer la fonction d'envoi des mails avec reprise possible
        envoiMailauxEtudiants(self.root,self.repertoire,dataMail,setUpMail,sujet,corpsDuMessageCommun,envoiReel)
        
    

    ### affichage 
    def __repr__(self):
        return f"{self.__class__.__name__}({self.__dict__})"

    def ouvrir_fenetre_interruption(self):
        """Ouvre une petite fenêtre avec 'Interuption des envoi' et un bouton 'interuption'."""
        self.controleur_ok = True  # réinitialise le contrôleur à OK

        self._win_interruption = tk.Toplevel(self.root)
        self._win_interruption.title("Interuption des envoi")
        self._win_interruption.resizable(False, False)
        self._win_interruption.transient(self.root)
        self._win_interruption.grab_set()

        frm = tk.Frame(self._win_interruption, padx=12, pady=12)
        frm.pack(fill="both", expand=True)

        tk.Label(
            frm,
            text="Interuption des envois.",
            font=("Arial", 12, "bold")
        ).pack(pady=(0, 10))

        tk.Button(
            frm,
            text="interuption",
            width=14,
            command=self._declencher_interuption
        ).pack()

        # Si on ferme la fenêtre avec la croix, on laisse l'envoi continuer
        self._win_interruption.protocol("WM_DELETE_WINDOW", self._fermer_sans_interrompre)

    def _declencher_interuption(self):
        """Appelé quand on clique sur le bouton 'interuption'."""
        self.controleur_ok = False
        if hasattr(self, "_win_interruption") and self._win_interruption.winfo_exists():
            self._win_interruption.destroy()

    def _fermer_sans_interrompre(self):
        """Fermeture de la mini-fenêtre sans stopper l'envoi."""
        if hasattr(self, "_win_interruption") and self._win_interruption.winfo_exists():
            self._win_interruption.destroy()


if __name__ == '__main__':
    root: tk.Tk = tk.Tk()
    # Assure une fermeture propre via la croix de la fenêtre (Thonny-friendly) A METTRE A LA FIN
    # root.protocol('WM_DELETE_WINDOW', root.destroy)
    # Fermer via la croix = juste quitter la boucle (CONSERVE les variables et widgets)
    root.protocol("WM_DELETE_WINDOW", root.quit)
    app = Boustrophedon(root)    
    root.mainloop()
    print(  ">>> Retour console. Variables disponibles : root, app \n"
            " et les variables de la classe en self.qqch")
    print(">>> Pour relancer l’UI, taper : root.mainloop()")
    
app