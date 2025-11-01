from dataclasses import dataclass
from typing import Tuple

# ────────────────────────────────────────────────────────────────────────────────
# Modèles de données
# ────────────────────────────────────────────────────────────────────────────────

@dataclass(init=False)  # parce qu'il y a un __init__
class etudiant:
    nom : str 
    prenom : str 
    numeroEtudiant : str 
    courriel : str 
    
    numeroPlace : int 
    numeroRang :  int 
    fichierPng :  str 
        
    def __init__(self,nom,prenom,numeroEtudiant,courriel):
        self.nom = nom 
        self.prenom = prenom 
        self.numeroEtudiant = numeroEtudiant
        self.courriel = courriel
        
        self.numeroPlace = 0
        self.numeroRang  = 0
        self.fichierPng  = ""
            
    def set_courriel(self,courriel):
        self.courriel = courriel
        
    def set_numeroPlace(self,col : int ) -> None :
        """ col est le numero de la colonne dans la grille de placement"""
        self.numeroPlace = col
        
    def set_numeroRang(self,row : int ) -> None :
        """ row est le numero de la ligne dans la grille de placement (commence à 1 !!)
            ce qui correspond au numéro du rang dans l'amphi à partir du bas.      """        
        self.numeroRang = row
        
    def set_fichierPng(self, fichierPng  : str ) -> None :
        """ row est le numero de la ligne dans la grille de placement (commence à 1 !!)
            ce qui correspond au numéro du rang dans l'amphi à partir du bas.      """        
        self.fichierPng  = fichierPng

@dataclass(init=False)  # parce qu'il y a un __init__
class rangDansZoneAmphi :
    numeroRang : int
    listeEtudiant : list[etudiant]
        
    def __init__(self, numeroRang : int ,listeEtudiant : list[etudiant] ):
        self.numeroRang : int = numeroRang        
        self.listeEtudiant : list[etudiant] = listeEtudiant 
        
    def ajouterEtudiant(self, etudiant):
        """Ajoute un étudiant à la liste du rang."""
        self.listeEtudiant.append(etudiant)
        
    def __repr__(self):
        return f"{self.__class__.__name__}({self.__dict__})"
    

@dataclass(init=False)  # parce qu'il y a un __init__
class zoneDansAmphi :
    """classe pour définir une zone dans un amphi"""
    nbMaxEtuDansZone : int      # capacité de la zone.
    nbRang : int                # nombre de rang ex 10 en bio 14 en Chimie et 17 au PV.
    nbMaxEtudiantParRang : int  # nombre ajusté par amphi en fonction du nombre d'étudiants.
    nbRangUnSurDeux : int       #    ex 7  pour 7 rangs sur les 14 dispo en 'Chimie'
    labelZone : str             #  ex 'C','B' ou 'A' pour le PV
    placement : list[Tuple[int,int]]
    listeRangDansZoneAmphi : list [ rangDansZoneAmphi]
    listeDesEtudiantDansLaZone : list[list[str]]
    liste_nom_fic_png : list [str]  # la liste des fichiers de places individuelles (plan de l'amphi avec la place entourée!)

    def __init__(self,nbMaxEtuDansZone : int ,
                 nbRang : int ,
                 nbMaxEtudiantParRang : int , 
                 nbRangUnSurDeux : int , 
                 labelZone : str  ):             
        self.nbMaxEtuDansZone : int = nbMaxEtuDansZone
        self.nbRang : int = nbRang    # 14 pour Chimie par exemple, utilisé pour les graphiques.
        self.nbMaxEtudiantParRang : int = nbMaxEtudiantParRang # est utilisé par GraphiqueUneZone après.
        self.nbRangUnSurDeux : int = nbRangUnSurDeux #
        self.labelZone : str = labelZone
        
        self.placement : list[Tuple[int,int]] = [] # les références des places occupées à remplir plus tard.
                                            # une liste de Tuple par zone!
                                            # un Tuple est le couple des indice (rang,colonne)
                                            # avec le (1,1) en bas à gauche pour la zone.
                                                               
        self.listeRangDansZoneAmphi : list [ rangDansZoneAmphi] =[]
        self.listeDesEtudiantDansLaZone = []
        self.liste_nom_fic_png = []
    
    def set_listeDesEtudiantDansLaZone(self,liste : list[list[str]]) -> None :
        self.listeDesEtudiantDansLaZone = liste
        
    def ajouterRang(self,rang : rangDansZoneAmphi )-> None:
        self.listeRangDansZoneAmphi.append(rang)
        
    def set_liste_nom_fic_png(self,liste : list[str] ) -> None:
        self.liste_nom_fic_png=liste
        

    def __repr__(self):
        return f"{self.__class__.__name__}({self.__dict__})"


@dataclass(init=False)  # parce qu'il y a un __init__
class amphi :
    nom : str =""
    listeTousLesEtudiantsDansAmphi : list[etudiant]
    zones : list[zoneDansAmphi]
    
    def __init__(self, nom ) :
        self.nom = nom
        self.listeTousLesEtudiantsDansAmphi =[]
        self.entourePlace : bool = False 
        self.zones = []
        self.nomFicPlanAmphiPng  = "" # le chemin absolu vers le fichier png avec la géométrie de l'amphi et les place

    def set_nomFicPlanAmphiPng(self,fichierPng):
        """Définit le chemin du fichier png dela géométrie de l'amphi."""
        print('ecriture de ',fichierPng)
        self.nomFicPlanAmphiPng = fichierPng
        
    def set_listeTousLesEtudiantsDansAmphi(self,listeEtu : list[etudiant] ):
        shuffle(listeEtu)
        self.listeTousLesEtudiantsDansAmphi =  listeEtu
        
        
    def ajouteEtudiant(self, Etudiant) :
        self.listeTousLesEtudiantsDansAmphi.append(Etudiant)
        
    def set_zones(self,listeZones : list[zoneDansAmphi] ) -> None  :
        self.zones = listeZones
        
    def get_nbEtudiantAmphi(self) -> int  :
        return len(self.listeTousLesEtudiantsDansAmphi) 
    
    def __repr__(self):
        return f"{self.__class__.__name__}({self.__dict__})"   