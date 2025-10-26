import tkinter as tk
from tkinter import messagebox, filedialog

import os,sys
from dataclasses import dataclass,fields 


# Ajoute le dossier "app" à sys.path pour permettre les imports relatifs propres
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, 'app'))
sys.path.insert(0, project_root)

from classes.c1_classe_chargementCsv import chargementCSV

from classes.c3_classe_arborescence import arborescence
from classes.c4_classe_champsApogee import champsApogee

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
            text='Cocher une case puis "Valider"',
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
    def update_buttons_state(self):
        """Active/désactive les boutons selon l’état du projet."""
        state = tk.NORMAL if self.etat.charge else tk.DISABLED
        self.btn_png.config(state=state)
        self.btn_pdf.config(state=state)
        self.btn_mail.config(state=state)

    def chargerDonnees(self):
        # lit le mode sélectionné dans l'UI.
        self.etat.mode = self.var_mode.get() or "nil"
        # instanciation de la classe qui contient les données brutes (Moodle et Apogee si Examen)
        self.dataBrutes = chargementCSV(self.etat.mode, self.root)
        cheminFicMoodle : str = self.dataBrutes.moodle.chemin
        # dataMoodle : list =  self.dataBrutes.moodle.data  ...bref voir classe
        
        
        self.arborescence=arborescence( cheminFicMoodle, ['Titi','Toto'] )
        #print(self.AZE.get_chemin("Titi", "texOut"))
        
        if self.dataBrutes.apogee not in (None, []):
            self.dataCodeEnteteApogee = champsApogee(self.dataBrutes)        
            print('la valeur du code apogée DAT_DEB_PES  est ', self.dataCodeEnteteApogee.valeurCode('DAT_DEB_PES') )
        messagebox.showinfo("Chargement", f"Données chargées pour un {self.etat.mode}).")
        self.update_buttons_state()

    def actionsBouton2(self):
        # Générer PNG
        # >>> ICI ton code de génération des PNG <<<
        messagebox.showinfo("PNG", "Génération des images PNG terminée.")

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