import tkinter as tk
from tkinter import messagebox, filedialog

import os,sys
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

from utils.utilitaires import *
from utils.utilitaire_UI_amphiMoodle import definitRemplissage
from utils.utilitaire_completeDefAmphi import completeDefinitionAmphi
from utils.utilitaires_bouton2 import *
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
        
        self.listeFenetreGraphiqueVisuAmphi = []
        
        # Construire l'UI
        self.build_header()
        self.build_controls()
        self.build_buttons()
        self.update_buttons_state()

        # Boucle principale
        self.root.mainloop()

    # ----- Vue : entête -----
    def build_header(self):
        tk.Label(
            self.root,
            text  ="Étape 1 : Chargement des données.",
            font =("Arial", 11, "bold")
        ).pack(pady=10)

    # ----- Vue : contrôles (radio) -----
    def build_controls(self):
        frame_radio = tk.Frame(self.root)
        frame_radio.pack(pady=10)

        tk.Label(
            frame_radio,
            text='Cocher une case puis cliquer sur "Chargement ..."',
            font=("Arial", 11)
        ).pack(side="left", padx=10)

        self.var_mode = tk.StringVar(value=self.etat.mode)
        tk.Radiobutton(
            frame_radio, text="Examen",
            variable=self.var_mode, value="Examen"
        ).pack(side="left", padx=10)
        tk.Radiobutton(
            frame_radio, text="Partiel",
            variable=self.var_mode, value="Partiel"
        ).pack(side="left", padx=10)

    # ----- Vue : boutons d’actions -----
    def build_buttons(self):
        self.btn_load = tk.Button(
            self.root,
            text="Chargement des données et visualisation des amphis remplis",
            command=self.chargerDonnees
        )
        self.btn_load.pack(pady=10)

        self.btn_png = tk.Button(
            self.root,
            text=("Générer les fichiers *.png des places individuelles.\n"
                  "Cette opération peut être longue.\n"
                  "ÉTAPE NON OBLIGATOIRE"),
            command=self.actionsBouton2,
            state=tk.DISABLED
        )
        self.btn_png.pack(pady=10)

        self.btn_pdf = tk.Button(
            self.root,
            text="Générer les fichiers PDF des listes d'émargement",
            command=self.actionsBouton3,
            state=tk.DISABLED
        )
        self.btn_pdf.pack(pady=10)

        self.btn_mail = tk.Button(
            self.root,
            text="Envoyer les fichiers individuels aux étudiants par mail",
            command=self.envoyerMails,
            state=tk.DISABLED
        )
        self.btn_mail.pack(pady=10)
        tk.Button(self.root, text="Quitter  ", command=self.root.destroy).pack(pady=10)
        tk.Button(self.root, text="Quitter (quit et pas destroy pour le dev)", command=self.root.quit).pack(pady=10)

    # ----- Contrôleur : logique -----
    def update_buttons_state(self, etape="initial"):
        if etape == "initial":
            self.btn_png.config(state=tk.DISABLED)
            self.btn_pdf.config(state=tk.DISABLED)
            self.btn_mail.config(state=tk.DISABLED)
        elif etape == "donnees_chargees":
            self.btn_png.config(state=tk.NORMAL)
        elif etape == "png_genere":
            self.btn_pdf.config(state=tk.NORMAL)
        elif etape == "pdf_genere":
            self.btn_mail.config(state=tk.NORMAL)
    
    def exploiteApogee(self):
        """ configure les données d'Apogée dans les classe Amphi (y dépose la liste des étudiants)"""
        # Fais le compte des amphi vides et  de la liste de nom des amphis
        self.nbAmphiApogee ,  self.listeNomAmphi  = compteEtListeAmphiApogee(self.dataBrutes)
        print(f" Le fichier apogée contient {self.nbAmphiApogee} amphi(s) dont les noms sont {self.listeNomAmphi}.\n ") 

        # création de l'arborescence des fichiers à partir de l'emplacement du fichier moodle            
        self.arborescence = arborescence( self.dataBrutes.apogee.chemin, self.listeNomAmphi )
        print(f"L'arborescence des fichiers est créée.\n Les fichiers de sortie se "
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
            for dataEtu in extraitApogee :
                amphitheatre.ajouteEtudiant(etudiant(nom = dataEtu[17] ,
                                                     prenom = dataEtu[18],
                                                     numeroEtudiant = dataEtu[19],
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
        allocationAmphi : list[Tuple[str,int]] = definitRemplissage(nb_etudiants= len(self.dataBrutes.moodle.data),nb_tiers_temps = 12, parent=self.root)    
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
        # affectation des étudiants dans les amphi : avec moodle, on pioche le nombre dans allocationAMphi et les étudiants
        #dans dataBrutes.moodle.data
        decalage : int =0 # pour récupér la tranche suivante dans la liste d'étudiant
        for amphitheatre in self.listAmphi :
            listeValeursUniques  : list[Tuple[int,bool]] = [(nomAmphi,valeur, boolTT)  for (nomAmphi, valeur ,boolTT) in allocationAmphi if nomAmphi==amphitheatre.nom ]
            nomAmphi : str = listeValeursUniques[0][0]
            nbEtudiantAPlacer : int = listeValeursUniques[0][1]
            TT : bool =  listeValeursUniques[0][2]
            print("Valeur bool" , TT)
            if not TT : # si pas tiers temps
                print('branche not TT du test ok')
                etudiantsAPlacer : list[list[str]] = self.dataBrutes.moodle.data[decalage:(decalage+nbEtudiantAPlacer)]
                decalage = decalage+nbEtudiantAPlacer # pour placer le pointeur sur le prochain étudiant dans la liste Moodle.
                for dataEtu in etudiantsAPlacer :
                    amphitheatre.ajouteEtudiant(etudiant(nom = dataEtu[1] ,
                                                         prenom = dataEtu[0],
                                                         numeroEtudiant = dataEtu[2],
                                                         courriel=dataEtu[3]
                                                        ) 
                                                )
            else : # si tiers temps...
                etudiantsAPlacer : list[list[str]] = self.dataBrutes.moodleTt.data # on pioche dans la liste Tiers Temps.
                nb_tiers : int = len(etudiantsAPlacer)
                # pas de décalage car on parcourt pas la liste moodle.
                for dataEtu in etudiantsAPlacer :
                    amphitheatre.ajouteEtudiant(etudiant(nom = dataEtu[1] ,
                                                         prenom = dataEtu[0],
                                                         numeroEtudiant = dataEtu[2],
                                                         courriel=dataEtu[3]
                                                        ) 
                                                )
                print('branche  TT du test ok')
                
                # le complément dans l'amphi
                nbEtudiantAPlacer=nbEtudiantAPlacer- len(etudiantsAPlacer) # on calcule les places restantes pour la liste Moodle.
                etudiantsAPlacer : list[list[str]] = self.dataBrutes.moodle.data[decalage:(decalage+nbEtudiantAPlacer)]
                decalage = decalage+nbEtudiantAPlacer # pour placer le pointeur sur le prochain étudiant dans la liste Moodle.
                for dataEtu in etudiantsAPlacer :
                    amphitheatre.ajouteEtudiant(etudiant(nom = dataEtu[1] ,
                                                         prenom = dataEtu[0],
                                                         numeroEtudiant = dataEtu[2],
                                                         courriel=dataEtu[3]
                                                        ) 
                                                )            
                print(f"{nbEtudiantAPlacer} étudiants dont {nb_tiers} étudiants ont été placés dans l'amphi {nomAmphi}.") 
            
            print(f"L'AAAAmphithéatre {amphitheatre.nom} a reçu {len(amphitheatre.listeTousLesEtudiantsDansAmphi)} instances d'étudiants.\n")
            #input("4) taper entrée")
        # fin exploiteMoodle(self)                
    
    
    
    def chargerDonnees(self):
        # lit le mode sélectionné dans l'UI.
        self.etat.mode = self.var_mode.get() or "nil"
        # instanciation de la classe qui contient les données brutes (Moodle et Apogee si Examen)
        self.dataBrutes = chargementCsv(self.etat.mode, self.root)
        
        
        print(f"Le fichier Moodle contient : {self.dataBrutes.getNbmoodle()} étudiants.\n")
        
        
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
        

        #input("entrée")
        self.update_buttons_state("donnees_chargees")
         

    def actionsBouton2(self):
        if len(self.listeFenetreGraphiqueVisuAmphi) !=0 :
            for fenetre in self.listeFenetreGraphiqueVisuAmphi:
                fenetre.destroy()
           
        for amphi in self.listAmphi :  
            genererLesPngPlacesIndividuelles(amphi,self.arborescence,self.root,self.listeFenetreGraphiqueVisuAmphi)
            
            remplitRangCompleteEtudiant(amphi)
            
        messagebox.showinfo("PNG", "Génération des images PNG terminée.")
        self.update_buttons_state("png_genere")
        
    def actionsBouton3(self):
        # Générer PDF
        # >>> ICI ton code de génération des PDF <<<
        messagebox.showinfo("PDF", "Génération des PDF terminée.")

    def envoyerMails(self):
        # Envoi des mails
        # >>> ICI ton code d’envoi <<<
        messagebox.showinfo("Mail", "Envoi des emails terminé.")
    ### affichage 
    def __repr__(self):
        return f"{self.__class__.__name__}({self.__dict__})"
        
   
if __name__ == '__main__':
    root: tk.Tk = tk.Tk()
    # Assure une fermeture propre via la croix de la fenêtre (Thonny-friendly) A METTRE A LA FIN
    # root.protocol('WM_DELETE_WINDOW', root.destroy)
    # Fermer via la croix = juste quitter la boucle (CONSERVE les variables et widgets)
    root.protocol("WM_DELETE_WINDOW", root.quit)
    app = Boustrophedon(root)    
    root.mainloop()
    print(">>> Retour console. Variables disponibles : root, app \n"
          " et les variables de la classe en self.qqch")
    print(">>> Pour relancer l’UI, taper : root.mainloop()")
    
    print(vars(app))