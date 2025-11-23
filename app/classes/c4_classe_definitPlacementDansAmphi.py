
from classes.c2_0_classeS_etudiant_a_amphi import amphi

    
class definitPlacementDansAmphi :
    """Définit les référence des places d'un amphithéâtre uniquement
       en connaissant le nom de l'amphi et le nombre total des étudiants
       Définit la liste des places occupées , une liste de places par zone dans l'amphi.
       Cela remplit l'attribut self.placement  de la classe amphiAvecEtudiants
       Pour les zones 0 et 2  du PV le banc du bas, N°1 est tronqué.
       """
    def __init__(self, amphiPlein : amphi ):                        
                                    
        self.amphiPlein : amphi  = amphiPlein
        # calcul le nombre d'étudiant par zone pour l'amphi en cours.
        self.repartition : list[int] = self.calculeNmaxParZone()
        
        self.referencePlaces()
                  
    def __repr__(self):
        return f"{self.__class__.__name__}({self.__dict__})"
    
    def remplitColonnes(self,col1,col2,lig1,lig2,refPlace):
        """remplit de la col1 incluse à col2 incluse les rangs lig1 inclus à lig2 inclus """
        for colonne in range(col1, col2+1 ) :                    
            for nmrRang in range(lig1 , lig2 + 1 ) :                
                indiceRang = 1 + 2 * ( nmrRang - 1 )  #   varie de 1 à 1+2* (nbRangPleins-1]
                                           # si nbRangPleins=5 varie jusqu'à 9   ( 1,3,5,7,9 !!)
                refPlace.append( ( indiceRang , colonne )  )
                    
    def remplitZoneNormale(self,refPlace,indiceZone):
        nbEtudiantsDansZone : int = self.repartition[indiceZone]
        nbRangUnSurDeux     : int = self.amphiPlein.zones[indiceZone].nbRangUnSurDeux
        # calcul du nombre de colonnes remplies entièrement avec nbRangUnSurDeux étudiants
        
        nbColonnes = nbEtudiantsDansZone // nbRangUnSurDeux
        self.amphiPlein.zones[indiceZone].nbMaxEtudiantParRang =  nbColonnes # mise à jour
                          
        if nbEtudiantsDansZone %  nbRangUnSurDeux == 0 :  
            #La zone est entièrement remplie.
            self.remplitColonnes( col1 = 1   ,
                             col2 = nbColonnes ,
                             lig1 = 1,
                             lig2 = nbRangUnSurDeux ,
                             refPlace = refPlace )
        else :                      
            # il y a une colonne partiellement remplie
            nbColonnes  = nbColonnes + 1
            # calcul du nombre de places vides :
            nPlacesVides = nbColonnes*nbRangUnSurDeux - nbEtudiantsDansZone
            
            refColPartielle : int = nbColonnes//2 +1 # la ref de la col partiellement remplie.
                
            self.amphiPlein.zones[indiceZone].nbMaxEtudiantParRang =  nbColonnes # mise à jour
            
            # premieres colonnes pleines :
            self.remplitColonnes( col1 = 1 ,
                                 col2 = refColPartielle-1 , # avant dernier n° de colonne pleine.
                                 lig1 = 1,
                                 lig2 = nbRangUnSurDeux,
                                 refPlace = refPlace )                    
            # remplissage de la colonne avec places vides.
            self.remplitColonnes( col1 = refColPartielle ,    # N° col pleine.
                                 col2 = refColPartielle ,
                                 lig1 = 1,
                                 lig2 = nbRangUnSurDeux-nPlacesVides,
                                 refPlace = refPlace )
            # remplissage des dernières colonnes pleines (à partir de nbColonnes=3 !)
            if nbColonnes>2 : 
                self.remplitColonnes( col1 = refColPartielle + 1  ,
                                     col2 = nbColonnes ,
                                     lig1 = 1,
                                     lig2 = nbRangUnSurDeux ,
                                     refPlace = refPlace )                                                
        # on remplit l'attribut pour la zone    
        self.amphiPlein.zones[indiceZone].placement = refPlace
        # fin de remplitZoneNormale

    def remplitZoneTronqueePV(self,refPlace,indiceZone):
        nbEtudiantsDansZone : int = self.repartition[indiceZone]
        
        if nbEtudiantsDansZone == 0:
            self.amphiPlein.zones[indiceZone].placement = []
            return
        
        nbRangUnSurDeux     : int = self.amphiPlein.zones[indiceZone].nbRangUnSurDeux
        nbColonnes, refColPartielle, nPlacesVides, nPlacesRang1 =  self.calculColPourPvZonesSurLesCotes( nbEtudiantsDansZone )
        if nPlacesVides==8 :
            nbColonnes = nbColonnes -1 # pour le cas particulier où il y aurait 43  étudiants
                                       # cela évite d'avoir une colonne vide du rang 3 au sommet de l'amphi
        self.amphiPlein.zones[indiceZone].nbMaxEtudiantParRang =  nbColonnes # mise à jour
        
        # on remplit à partir du rang 2 colonne par colonne
        # le demi-rang 1 est rempli après
        self.remplitColonnes( col1 = 1 ,
                         col2 = refColPartielle-1 ,
                         lig1 = 2,
                         lig2 = nbRangUnSurDeux,
                         refPlace = refPlace )
            
        # remplissage de la colonne avec places vides si il y a des étudiants.
        if nPlacesVides!=8 :
            self.remplitColonnes( col1 = refColPartielle ,
                             col2 = refColPartielle ,
                             lig1 = 2,
                             lig2 = nbRangUnSurDeux-nPlacesVides ,
                             refPlace = refPlace )
        else : # recalage du numéro de colone
            refColPartielle=refColPartielle-1
        # remplissage des dernières colonnes :
        self.remplitColonnes( col1 = refColPartielle + 1  ,
                         col2 = nbColonnes ,
                         lig1 = 2,
                         lig2 = nbRangUnSurDeux ,
                         refPlace = refPlace )
        
        # remplissage du rang 1 du PV.
        # la zone en bas à Gauche :
        if indiceZone==0 : # on remplit de col = 1 à  col =  nPlacesRang1 +1
            self.remplitColonnes( col1 = nbColonnes-nPlacesRang1 +1   ,
                             col2 = nbColonnes ,
                             lig1 = 1,
                             lig2 = 1 ,
                             refPlace = refPlace )
        elif indiceZone==2 : # on remplit en symétrie de col = 1 à  col =  nPlacesRang1 +1
            self.remplitColonnes( col1 = 1  ,
                             col2 = nPlacesRang1 ,
                             lig1 = 1,
                             lig2 = 1 ,
                             refPlace = refPlace )
            
        self.amphiPlein.zones[indiceZone].placement = refPlace
        ## fin de remplitZoneTronqueePV 
        
    def referencePlaces(self):
        """renvoie une liste de référence de place pour une zone d'amphi remplie en fonction du nombre d'étudiant
        Ex : maxi  42 places pour une zone d'un amphi 2 zones (Info,Math etc)  par exemple avec
             une place vide par rang en partant du haut.
        """            
        # debut de refplacement....
        for indiceZone in range(len(self.amphiPlein.zones)) :
            
            refPlace : list [Tuple[int,int]]= [] # la liste des références des places est initialisée
                        
            if len(self.amphiPlein.zones)==3 and indiceZone in [0,2]  : # cas spécial du PV avec rang 1 tronqué !
                self.remplitZoneTronqueePV(refPlace,indiceZone)                                                                   
            else : # pour les zones standards :
                self.remplitZoneNormale(refPlace,indiceZone)
                            
    def calculeNmaxParZone(self):
        self.nbZones=len(self.amphiPlein.zones)
        self.nbTotalEtudiants= len(self.amphiPlein.listeTousLesEtudiantsDansAmphi)
        
        # testé !
        if self.nbZones==1 :
            return [self.nbTotalEtudiants] # cas trivial
        elif self.nbZones==2 :
            n1 = self.nbTotalEtudiants // 2
            n2 = self.nbTotalEtudiants - n1
            return [ n1 , n2 ]
        
        elif self.nbZones==3 :
            # voir détails dans tableur 
            n = self.nbTotalEtudiants

            nCote     = int(51/165*n) 
            nCentre   = int(63/165*n)
            
            total = nCote + nCentre + nCote
            differenceArrondi = n - total # vaut 0 pour n = 165 vaut 2 pour 163  à reporter au centre où il en manque
            nCentre = nCentre + differenceArrondi            
            return [nCote,nCentre,nCote]

    def calculColPourPvZonesSurLesCotes(self, n : int  ) -> int :
            # n est le nombre d'étudiants dans la zone latérale du PV.
            if 42 < n <= 51 :                         
                nbColonnes =6
                refColPartielle=3  # colonne avec place vide vers le haut de l'amphi
                nPlacesVide = 51 - n
                nPlacesRang1 = 3
            elif 34 < n <= 42 :
                nbColonnes = 5
                refColPartielle=3
                nPlacesVide = 42 - n
                nPlacesRang1 = 2
            elif 25 < n <= 34 :
                nbColonnes = 4
                refColPartielle=3
                nPlacesVide = 34 - n
                nPlacesRang1 = 2
            elif 17 < n <= 25 :
                nbColonnes = 3
                refColPartielle=2
                nPlacesVide = 25 - n
                nPlacesRang1 = 1 # on aurait pu écrire nbColonnes//2 .
            elif 9 < n <= 17 :
                nbColonnes = 2
                refColPartielle=2
                nPlacesVide = 17 - n
                nPlacesRang1 = 1
            elif  0 <= n <= 9 :
                nbColonnes = 1
                refColPartielle=1
                nPlacesVide = 9 - n
                nPlacesRang1 = 1

            return nbColonnes,refColPartielle,nPlacesVide,nPlacesRang1
