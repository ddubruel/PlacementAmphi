from dataclasses import  dataclass 
from tkinter import messagebox

from app.utils.utilitaire_UI_saisirDonneesEpreuve import UI_saisirDonneesEpreuve
from classes.c2_0_classeS_etudiant_a_amphi import amphi
# ────────────────────────────────────────────────────────────────────────────────
# Modèles de données
# ────────────────────────────────────────────────────────────────────────────────
@dataclass( init=False)  # parce qu'il y a un __init__
class codeEnteteApogee  :  
    annee_universitaire :str 
    date :str
    horaires :str
    duree :str
    epreuve :str

    def __init__(self, mode : str , dataBrutes : list[list[str]], listeDesAmphi : list[amphi] , nomAmphi : str, root ):
        """Crée une liste de Tuple (code, valeur) """
        # définition des paramètres communs aux pdf (un par amphi, seul le nom change)
        self.dataBrutes = dataBrutes
        self.listeDesAmphi =listeDesAmphi
        self.nomAmphi= nomAmphi
        self.root=root
        # attribut utilisés à l'extérieur de la classe :
        self.annee_universitaire  :str 
        self.date     :str 
        self.horaires   :str 
        self.duree   :str 
        self.epreuve   :str 
        self.LIB_SAL   :str 
    
        
        if mode == 'Examen':
            self.annee_universitaire = self.valeurCodeApogee(  code ='C_COD_ANU'     )
            self.date=                 self.valeurCodeApogee(  code = 'DAT_DEB_PES'  )
            self.horaires=             self.valeurCodeApogee(  code = 'HEURE_DEBUT'  )
            self.duree=                self.valeurCodeApogee(  code = 'DUREE_EXA'    )
            self.epreuve=              self.valeurCodeApogee(  code = 'COD_EPR'      )
            self.LIB_SAL = self.codeAmphiApogee()
            
    def set_valeurs(self, annee_universitaire, date, horaires,duree, epreuve, LIB_SAL):
        self.annee_universitaire  = annee_universitaire
        self.date      = date 
        self.horaires  = horaires 
        self.duree     = duree
        self.epreuve   = epreuve
        self.LIB_SAL   = LIB_SAL
    
    def set_LIB_SAL(self,nomAmphi : str ):
        self.LIB_SAL =nomAmphi
        
    def codeAmphiApogee(self )-> str :
        """ renvoie le code apogée de l'amphi lu dans le fichier apogée"""        
        positionEtuDansAmphi : int = 0        
        #nom : str= listeDesAmphi[0].nom # nom du premier amphi
        for k in range(len(self.listeDesAmphi)):
            if self.nomAmphi == self.listeDesAmphi[k].nom :
                return self.dataBrutes.apogee.data[positionEtuDansAmphi][13] # LIB_SAL ex 'Amphi d'informatique'.
            else :
                # on calcule la position de l'étudiant dans le prochain amphi.
                positionEtuDansAmphi = positionEtuDansAmphi + self.listeDesAmphi[k].get_nbEtudiantAmphi() 

    def valeurCodeApogee(self , code : str ) -> str : 
        #enteteApoge : list[str] = self.dataBrutes.apogee.entete
        #premierEtudiant : list[str] = self.dataBrutes.apogee.data[1] # pour les valeurs communes, c'est suffisant, la ligne du premier étudiant les contient.
        for k in range(len(self.dataBrutes.apogee.entete)) :
            if self.dataBrutes.apogee.entete[k] == code :
                return self.dataBrutes.apogee.data[1][k]  
      
    def __repr__(self):
        return f"{self.__class__.__name__}({self.__dict__})"
    


            