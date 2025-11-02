import tkinter as tk
import os
from app.utils.utilitaire_save_canvas import save_canvas

class GraphiqueUneZone:    
    def __init__(self,
                 canvas,
                 Amphi,
                 nmrZone, # 0,1,2
                 xhg, yhg,
                 longueur,
                 espace,
                 couleurZone,
                 arborescence
                 ):

        self.canvas = canvas        
        self.canvas.pack(side=tk.LEFT, padx=10, pady=10)
        self.Amphi = Amphi
        self.Nb_zones=len(self.Amphi.zones) 
        self.nb_places_par_rang_pour_cette_zone =self.Amphi.zones[nmrZone].nbMaxEtudiantParRang
        self.Nb_rang = self.Amphi.zones[nmrZone].nbRang
        self.titre = self.Amphi.zones[nmrZone].labelZone
        self.nomAmphi = self.Amphi.nom
        self.placement = self.Amphi.zones[nmrZone].placement
                
        self.nmrZone=nmrZone
        self.xhg = xhg   # abscisse coin haut à gauche
        self.yhg = yhg
 
        self.longueur =longueur
        self.espace = espace      # espace entre 2 bancs

#         print('Amphi',self.nomAmphi)
#         print('zone',self.titre)        
#         print("self.nb_places_par_rang_pour_cette_zone = ",self.nb_places_par_rang_pour_cette_zone)
#         

        self.nomAmphi =  self.nomAmphi.split()[-1]    # 'Amphithéatre Chimie' par exemple.
        self.couleurZone=couleurZone
        
        self.arborescence = arborescence
        
        self.listeDesPlaces=[] # les places codées en D-1-4 par exemple à partir de listeCasesetc...
        self.liste_nom_fic_png=[] # la liste vers les fichiers de l'amphi avec place entourée
        self.démarre()
                        
    def démarre(self) :
        self.dessine() # OK
        self.colorieZone()
        self.canvas.update_idletasks() # pour laisser le temps à la fenêtre d'etre tracée.
        largeur = self.canvas.winfo_width()
        hauteur = self.canvas.winfo_height() 
        self.canvas.create_text(largeur // 2, 25, text=f"  {self.nomAmphi}", font="arial 20", tags="nom_amphi_text")
        self.canvas.create_text(25, 25, text=f"Haut", font="arial 12")
        self.canvas.create_text(largeur-30, 25 , text=f"Haut", font="arial 12")
        
        self.canvas.create_text(25, hauteur-20, text=f"Bas", font="arial 12")
        self.canvas.create_text(largeur-30, hauteur-20 , text=f"Bas", font="arial 12")
        
        self.canvas.create_rectangle(largeur // 2 - 220, hauteur-50-20, largeur // 2 + 220, hauteur-50+20, fill="yellow", outline="", tags="bg_bas")
        self.canvas.create_text(largeur // 2, hauteur-50, text="Zone de dépôts des sacs et téléphones...", font="Arial 15", fill="red", tags="text_bas")
        
        x_milieu_zone = self.xhg + self.longueur//2
        y_bas_zone =  self.yhg + self.Nb_rang * self.espace
        self.canvas.create_text(x_milieu_zone, y_bas_zone, text=f"{self.titre}", font="arial 17")
        self.ecritLaPlace()        
#        self.entourePlaceEtSauveFicPng() 
        
        
    def dessine(self):
        """"Dessine les traits représentants les pupitres"""
        x0=self.xhg
        y0=self.yhg
        x1=x0+self.longueur
        y1=y0
        if self.Nb_zones <= 2 : # tous les amphis sauf Petit_Valrose
            for k in range(1, self.Nb_rang+1 ,1) :             
                y0=self.yhg +(k-1)* self.espace   # k=1 vaut yhg puis yhg+decalage etc...
                y1=y0
                self.canvas.create_line(x0, y0, x1, y1, width=2)
        if self.Nb_zones ==3 :
            for k in range(1, 16 ,1) :             
                y0=self.yhg +(k-1)* self.espace   # k=1 vaut yhg puis yhg+decalage etc...
                y1=y0
                self.canvas.create_line(x0, y0, x1, y1, width=2)
            # on termine pour les 2 rangs du bas en fonction des zones.
            if     self.nmrZone==0:  # la zone de gauche du PV depuis la chaire.
                x1=x0+int(self.longueur*0.65)   # on dessine les bancs plus courts.
                for k in range(16, self.Nb_rang+1 ,1) :                    
                    y0=self.yhg +(k-1)* self.espace   
                    y1=y0
                    self.canvas.create_line(x0, y0, x1, y1, width=2)
                ymin = self.yhg + 14  *  self.espace + 1
                ymax = self.yhg + 16  *  self.espace + 2  # + 2 pour effacer le trait du grand rectangle
                xmin = x0 + self.longueur//2 
                xmax = x0 + self.longueur   + 2  # + 2 pour effacer le trait du grand rectangle
                self.canvas.create_rectangle(xmin, ymin , xmax, ymax, fill='white',outline="")                                                  
            elif   self.nmrZone==2:  # la zone de droite du PV depuis la chaire.
                x0 = self.xhg  + self.longueur//2
                x1=self.xhg+self.longueur # on va au bout.
                for k in range(14, self.Nb_rang+1 ,1) :                 
                    y0=self.yhg +(k-1)* self.espace  
                    y1=y0
                    self.canvas.create_line(x0, y0, x1, y1, width=2)
                    ymin = self.yhg + 14  *  self.espace + 1
                    ymax = self.yhg + 16  *  self.espace + 2  # + 2 pour effacer le trait du grand rectangle
                    xmin = self.xhg -2  # - 2 pour effacer le trait du grand rectangle
                    xmax = self.xhg + self.longueur //2   
                    self.canvas.create_rectangle(xmin, ymin , xmax, ymax, fill='white',outline="")                                       
            else  : # zone centrale du PV
                for k in range(14, self.Nb_rang+1 ,1) :                    
                    y0=self.yhg +(k-1)* self.espace  
                    y1=y0
                    self.canvas.create_line(x0, y0, x1, y1, width=2)

            
    def colorieZone(self):
        if self.couleurZone!="":
            x0=self.xhg
            y0=self.yhg   -self.espace     
            x1=self.xhg+self.longueur
            y1=self.yhg+(self.Nb_rang-1)* self.espace            
            rect=self.canvas.create_rectangle(x0, y0 , x1, y1, fill=self.couleurZone)            
            self.canvas.lower(rect)

    def referencePlace(self,row,col):
        # le point (0,0) dans tkinter est en haut à gauche.
        # les places sont numérotée avec le premier rang en bas...
        if self.titre :  # cas avec 2 ou 3 zones
            prefixe_zone = self.titre[0]        
            reference_place = prefixe_zone+"-"+str(row) +"-"+str(col)
        else :
            reference_place = str(row) +"-"+str(col) # cas amphi 1 zone!!
            
        rang = self.Nb_rang - row         # 1 en bas et croissant vers le haut
        numero_place_inverse = self.nb_places_par_rang_pour_cette_zone -  col  
        
        if self.nb_places_par_rang_pour_cette_zone==1 :
            pas = 0
        else :
            pas = int (  0.8 * self.longueur  //   (self.nb_places_par_rang_pour_cette_zone - 1)  )
            
        xtex = self.xhg + 0.1 * self.longueur + pas * numero_place_inverse 
        ytex = self.yhg + rang * self.espace 
        return xtex,ytex, reference_place
            
    def ecritLaPlace(self) :        
        for k, (row,col) in enumerate(self.placement) :            
            xtex,ytex, reference_place = self.referencePlace(row,col)
            self.listeDesPlaces.append(reference_place)
            self.canvas.create_text(xtex, ytex-15,text=reference_place)
            self.canvas.update_idletasks() # pour laisser le temps à la fenêtre d'etre tracée.
            
                        
    def entourePlaceEtSauveFicPng(self):
        """ à utiliser en dehors sur le graphique final
        contenant toutes les instances ou zones dessinées"""                
        for k, (row,col) in enumerate(self.placement) :
            xtex,ytex, reference_place = self.referencePlace(row,col)
            
            # les fichiers à envoyer aux étudiants sont écrits directement dans l'arborscence
            # crée au début de l'instanciation de la classe de départ.
            path = self.arborescence.get_chemin(self.Amphi.nom, "pngOut")
            nomFicPng=f"{path}/{self.nomAmphi}_{reference_place}.png"
            self.liste_nom_fic_png.append(nomFicPng)
                        
            R=28
            xC=xtex
            yC=ytex-10                                                            
            self.ref = self.canvas.create_oval(xC-1.4*R,yC-R,xC+1.4*R, yC+R,  outline='red',width=3)  
            self.canvas.winfo_toplevel().update() #root.update()

            self.canvas.after(200)  # temporisation 
            save_canvas(nomFicPng, self.canvas)                    
            self.canvas.delete(self.ref) # Effacer juste le cercle après la capture
       
        
 


