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
        # --- nouvelle logique : N réel vs capacité pédagogique ---
        # capacité "normale" (1 rang sur 2) : somme des capacités de zones
        self.capaciteMax : int = sum(zone.nbMaxEtuDansZone for zone in self.amphiPlein.zones)
        self.nbTotalEtudiantsReel : int  = len(self.amphiPlein.listeTousLesEtudiantsDansAmphi)
        # nombre d'étudiants pris en compte pour le placement standard
        self.nbTotalEtudiants : int = min(self.nbTotalEtudiantsReel, self.capaciteMax)
        # calcul du nombre d'étudiant par zone pour le placement standard
        self.repartition : list[int] = self.calculeNmaxParZone()
        # placement standard (rangs 1,3,5,...)
        self.referencePlaces()
        # si on a du surnombre, on le place sur les rangs intermédiaires 2,4,6,...
        surplus = self.nbTotalEtudiantsReel - self.capaciteMax
        if surplus > 0:
            self.placeSurplusSurRangsIntermediaires(surplus)
                
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
        une place vide par rang en partant du haut."""            
        # debut de refplacement....
        for indiceZone in range(len(self.amphiPlein.zones)) :
            
            refPlace : list [tuple[int,int]]= [] # la liste des références des places est initialisée
                        
            if len(self.amphiPlein.zones)==3 and indiceZone in [0,2]  : # cas spécial du PV avec rang 1 tronqué !
                self.remplitZoneTronqueePV(refPlace,indiceZone)                                                                   
            else : # pour les zones standards :
                self.remplitZoneNormale(refPlace,indiceZone)
                            
    def calculeNmaxParZone(self):
        self.nbZones=len(self.amphiPlein.zones)
        n: int = self.nbTotalEtudiants # La valeur tronquée du nombre total d'étudiants        
        
        if self.nbZones==1 :
            return [n] # cas trivial
        
        elif self.nbZones==2 :
            n1 = n // 2
            n2 = n - n1
            return [ n1 , n2 ]
        
        elif self.nbZones==3 :
            # voir détails dans tableur             
            nCote     = int(51/165*n) 
            nCentre   = int(63/165*n)
            
            total = nCote + nCentre + nCote
            differenceArrondi = n - total # vaut 0 pour n = 165 vaut 2 pour 163  à reporter au centre où il en manque
            nCentre = nCentre + differenceArrondi            
            return [nCote,nCentre,nCote]

    def placeSurplusSurRangsIntermediaires(self, surplus: int) -> None:
        """
        Place les étudiants en surnombre sur les rangs intermédiaires (2,4,6,…)
        en conservant le nombre d'étudiants par rang déjà placé.

        - 1 zone  : tout le surplus va dans la seule zone
        - 2 zones : surplus//2 dans la 1re, le reste dans la 2e
        - 3 zones : surplus réparti en 30% / 40% / 30%
                    (zones gauche / centre / droite)
        """
        nbZones = len(self.amphiPlein.zones)
        if surplus <= 0:
            return

        # copie de la répartition standard que l'on va enrichir
        repartition_finale = list(self.repartition)

        # --- helper UNIQUE pour toutes les zones ---
        def genere_places(zone, nb_a_ajouter: int, rangDep : int ) -> list[tuple[int, int]]:
            """
            Génère nb_a_ajouter couples (rang, col) sur les rangs 2,4,6,...
            en utilisant les colonnes 1..nbMaxEtudiantParRang et les
            rangs intermédiaires entre les rangs occupés (1,3,5,...).
            """
            nouvelles_places: list[tuple[int, int]] = []
            nbColonnes = zone.nbMaxEtudiantParRang
            # il y a nbRangUnSurDeux rangs pleins (1,3,5,...),
            # donc nbRangUnSurDeux-1 rangs intermédiaires (2,4,6,...)
            nbRangIntermediaires = max(zone.nbRangUnSurDeux - 1, 0)

            if nbColonnes <= 0 or nbRangIntermediaires <= 0 or nb_a_ajouter <= 0:
                return nouvelles_places
            index_dep : int = rangDep //2 
            for i in range(index_dep, nbRangIntermediaires + 1):
                rang_intermediaire = 2 * i  # 2,4,6,...
                for col in range(1, nbColonnes + 1):
                    if len(nouvelles_places) >= nb_a_ajouter:
                        break
                    nouvelles_places.append((rang_intermediaire, col))
                if len(nouvelles_places) >= nb_a_ajouter:
                    break

            return nouvelles_places

        # --- 1 zone ---
        if nbZones == 1:
            zone = self.amphiPlein.zones[0]
            capacite_sup = zone.nbMaxEtudiantParRang * max(zone.nbRangUnSurDeux - 1, 0)
            a_ajouter = min(surplus, capacite_sup)
            nouvelles_places = genere_places(zone, a_ajouter,rangDep=2)# démarre au rang 2
            zone.placement.extend(nouvelles_places)
            repartition_finale[0] += len(nouvelles_places)
            surplus_restant = surplus - len(nouvelles_places)
            if surplus_restant > 0:
                print(
                    f"[AVERTISSEMENT] Surplus de {surplus_restant} étudiant(s) "
                    f"non placé(s) en rangs intermédiaires."
                )

        # --- 2 zones ---
        elif nbZones == 2:
            zone0, zone1 = self.amphiPlein.zones

            capacite_sup_0 = zone0.nbMaxEtudiantParRang * max(zone0.nbRangUnSurDeux - 1, 0)
            capacite_sup_1 = zone1.nbMaxEtudiantParRang * max(zone1.nbRangUnSurDeux - 1, 0)

            # partage théorique  : moitié / moitié
            surplus_z0_theorique = surplus // 2
            surplus_z0 = min(surplus_z0_theorique, capacite_sup_0)
            surplus_restant = surplus - surplus_z0
            surplus_z1 = min(surplus_restant, capacite_sup_1)
            surplus_restant_final = surplus_restant - surplus_z1

            # zone 0
            if surplus_z0 > 0:
                nouvelles_places_0 = genere_places(zone0, surplus_z0,rangDep=2)# démarre au rang 2
                zone0.placement.extend(nouvelles_places_0)
                repartition_finale[0] += len(nouvelles_places_0)

            # zone 1
            if surplus_z1 > 0:
                nouvelles_places_1 = genere_places(zone1, surplus_z1,rangDep=2)# démarre au rang 2
                zone1.placement.extend(nouvelles_places_1)
                repartition_finale[1] += len(nouvelles_places_1)

            if surplus_restant_final > 0:
                print(
                    f"[AVERTISSEMENT] Surplus de {surplus_restant_final} étudiant(s) "
                    f"non placé(s) en rangs intermédiaires."
                )

        # --- 3 zones (Petit Valrose, par ex.) ---
        elif nbZones == 3:
            zone_gauche, zone_centre, zone_droite = self.amphiPlein.zones

            # Répartition théorique du surplus : 30% / 40% / 30%
            n_cote = int(0.3 * surplus)
            n_centre = int(0.4 * surplus)

            somme = n_cote + n_centre + n_cote
            diff = surplus - somme
            # on met la différence au centre (zone la plus grande)
            n_centre += diff

            repart_surplus = [n_cote, n_centre, n_cote]
            zones = [zone_gauche, zone_centre, zone_droite]

            surplus_restant = surplus
            for idxZone, (zone, n_supp_th) in enumerate(zip(zones, repart_surplus)):
                capacite_sup_zone = zone.nbMaxEtudiantParRang * max(zone.nbRangUnSurDeux - 1, 0)
                n_a_ajouter = min(n_supp_th, capacite_sup_zone, surplus_restant)

                if n_a_ajouter > 0:
                    if   idxZone == 0:
                            rangDep = 4
                    elif idxZone == 1:
                            rangDep = 2
                    else:
                            rangDep = 4                             
                    nv_places = genere_places(zone, n_a_ajouter,rangDep)# randDep=1 pour démarrer au rang 2
                    zone.placement.extend(nv_places)
                    repartition_finale[idxZone] += len(nv_places)
                    surplus_restant -= len(nv_places)

            if surplus_restant > 0:
                print(
                    f"[AVERTISSEMENT] {surplus_restant} étudiant(s) en surplus "
                    f"n'ont pas pu être placés dans les rangs intermédiaires "
                    f"de l'amphi à 3 zones."
                )

        # Mise à jour finale de la répartition (pour le découpage des étudiants)
        self.repartition = repartition_finale




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