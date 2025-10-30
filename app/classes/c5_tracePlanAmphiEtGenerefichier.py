import tkinter as tk

#from classes.classe_instanceSurNomAmphi import instanceSurNomAmphi
#from classes.class_definitPlacementDansAmphi import definitPlacementDansAmphi

from classes.c2_0_classeS_etudiant_a_amphi import amphi

from app.utils.utilitaire_save_canvas import save_canvas
from classes.c6_classe_graphiqueUneZone import GraphiqueUneZone


class tracePlanAmphiEtGenerefichier :
    """classe pour afficher le plan de l'amphi et générer les fichiers
       de placement individuels.
       
        parent : l'instance 'BoustrophedonStructure' 
        parent.root : fenêtre Tk  pour les fenêtres à venir.
        parent.dictCheminAbsolus : dispo ici
    """

    def __init__(self,Amphi,arborescence,root ):
        """parent est la fenêtre tk avec les boutons"""

        self.Amphi = Amphi
        self.arborescence=arborescence
        self.root = root
        self.chemin_png = self.arborescence.get_chemin(self.Amphi.nom, "pngOut")
        self.chemin_tex = self.arborescence.get_chemin(self.Amphi.nom, "texOut")
        self.chemin_pdf = self.arborescence.get_chemin(self.Amphi.nom, "listes_Emargement_pdf")

        
        self.Nb_zones=len(self.Amphi.zones)
        # en fonction du nb de zones les paramêtre géométriques sont définis.
        self.definitParamGeometriqueAmphi()
        # recupere dans une liste le nombre de rang dans chaque zone
        self.recupereNbRang()
        # initialisation de la liste de fichiers png des places individuelles.
        self.listeNomsFichiersPng : list[str] =[]  # liste des chemins vers les fichier png individuels
        # lancement de la fenêtre:
        
        self.lanceFenetreTkinter()

    def lanceFenetreTkinter(self):
        # Crée une nouvelle fenêtre secondaire
        self.window = tk.Toplevel(self.root)

        self.window.geometry(f"{self.largeur}x{self.hauteur}")
        self.canvas = tk.Canvas(self.window,bg="white")

        self.scrollbar = tk.Scrollbar(self.window, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scroll_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window = self.scroll_frame, anchor="nw")
        self.scroll_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.grilles_frame = tk.Frame(self.scroll_frame)
        self.grilles_frame.pack()

        self.graphZone=[]
        for nmrZone in range(self.Nb_zones) :
            self.graphZone.append(GraphiqueUneZone(
                    self.canvas,
                    self.Amphi ,
                    nmrZone,
                    self.xhg[nmrZone], self.yhg,
                    self.longueur[nmrZone],
                    self.espace,                    
                    self.couleurZone[nmrZone],
                    self.arborescence
                     ) # pour Graphique...
                     ) # pour le append
        
        # sauvegarde du fichier géométrie 
        self.canvas.winfo_toplevel().update() #root.update()    # utile ???pas sûr.
        self.canvas.after(200)
        chemin_png = self.arborescence.get_chemin(self.Amphi.nom, "pngOut")
        nomFicAmphiPng=f"{chemin_png}/{self.Amphi.nom}_plan_general.png"
        self.nomFicPlanAmphiPng = nomFicAmphiPng        
        save_canvas(self.nomFicPlanAmphiPng, self.canvas)
        # on définit l'attribut d'Amphi
        self.Amphi.set_nomFicPlanAmphiPng(self.nomFicPlanAmphiPng)
                                
        # maintenant que les graphiques des amphis sont tracés,
        # on peut génèrer  les places individuelles si le booléen l'autorise  (cas du 3eme bouton)    
        if   self.Amphi.entourePlace  : 
            for nmrZone in range(self.Nb_zones) :
                self.graphZone[nmrZone].entourePlaceEtSauveFicPng()  # sauve les fichier et crée la liste des fichiers dans l'instance.
                listeNomsFichiersPng = self.graphZone[nmrZone].liste_nom_fic_png # recup  de la liste des fichiers png de l'instance.
                # placer cette liste dans l'attribut de la zone de l'amphi.
                self.Amphi.zones[nmrZone].set_liste_nom_fic_png(listeNomsFichiersPng)
                self.listeNomsFichiersPng.append(listeNomsFichiersPng)
                
    def definitParamGeometriqueAmphi(self):
        #recherche du nombre de zone dans l'amphi
        if self.Nb_zones == 1:
            self.largeur, self.hauteur = 550, 700
            self.longueur = [400 ]
            self.espace =  40
            self.xhg = [50]
            self.yhg = 100
            self.couleurZone = ['lightyellow','honeydew', 'mistyrose']

        elif self.Nb_zones == 2:
            self.largeur, self.hauteur = 1000, 800
            self.longueur = [400 , 400 ]
            self.espace =  40
            self.yhg = 100
            self.largeur_escalier = 75
            self.x_hg_0 = 50
            self.x_hg_1 = 50 + self.largeur_escalier + self.longueur[0]
            self.xhg=[self.x_hg_0 , self.x_hg_1 ]
            self.couleurZone = ['lightyellow','honeydew' ]

        elif self.Nb_zones == 3:
            self.largeur, self.hauteur = 1450, 800
            self.longueur =[400 , 500, 400]
            self.espace =  35
            self.yhg = 75
            self.largeur_escalier = 10
            self.x_hg_0 = 50
            self.x_hg_1 = 50 + self.largeur_escalier + self.longueur[0]
            self.x_hg_2 = 50 + self.largeur_escalier + self.longueur[0] + self.largeur_escalier + self.longueur[1]
            self.xhg = [ self.x_hg_0  ,  self.x_hg_1  , self.x_hg_2 ]
            self.couleurZone = ['lightyellow','honeydew', 'mistyrose']

    def recupereNbRang(self) :
        self.Nb_rang=[]

        for nmrZone in range(self.Nb_zones) :
            nbDeRangDansLaZone = self.Amphi.zones[nmrZone].nbRang
            self.Nb_rang.append(nbDeRangDansLaZone)
            #print("nbDeRangDansLaZone ", nbDeRangDansLaZone)
