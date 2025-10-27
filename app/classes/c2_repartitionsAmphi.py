# from dataclasses import dataclass
# 
# from classes.c1_classe_chargementCsv import chargementCSV
# # ────────────────────────────────────────────────────────────────────────────────
# # Modèles de données
# # ────────────────────────────────────────────────────────────────────────────────
# 
# @dataclass(init=False)  # parce qu'il y a un __init__
# class etudiant:
#     nom : str =""
#     prenom : str =""
#     numeroEtudiant : str =""
#     courriel : str =""
#     
#     def __init__(self, nom, prenom, numeroEtud, courriel):
#         self.nom: str = nom
#         self.prenom: str = prenom
#         self.numeroEtudiant: int = numeroEtud
#         self.courriel : str = courriel
#         self.numeroPlace : int = numeroPlace
#         self.numeroRang : int = numeroRang
#         self.fichierPng : str = fichierPng
#     
#     def set_numeroPlace(self,col : int ) -> None :
#         """ col est le numero de la colonne dans la grille de placement"""
#         self.numeroPlace = col
#         
#     def set_numeroRang(self,row : int ) -> None :
#         """ row est le numero de la ligne dans la grille de placement (commence à 1 !!)
#             ce qui correspond au numéro du rang dans l'amphi à partir du bas.      """        
#         self.numeroRang = row
#         
#     def set_fichierPng(self, fichierPng  : int ) -> None :
#         """ row est le numero de la ligne dans la grille de placement (commence à 1 !!)
#             ce qui correspond au numéro du rang dans l'amphi à partir du bas.      """        
#         self.fichierPng  = fichierPng
# 
# @dataclass(init=False)  # parce qu'il y a un __init__
# class amphi :
#     nom : str =""
#     listEtudiant : list[etudiant]
#     
#     def __init__(self, nomAmphi) :
#         self.nom = nomAmphi
#         self.listEtudiant =[]
#         
#     def ajouteEtudiant(self, Etudiant) :
#         self.listEtudiant.append(Etudiant)
# 
# @dataclass(init=False)  # parce qu'il y a un __init__
# 
# class repartitionAmphi:
#     """Représente les répertoires d'un amphithéâtre donné."""
# 
#     dataBrutes : chargementCSV
#             
#     def __init__(self, dataBrutes):
#         self.dataBrutes = dataBrutes
#         
#         self.repartiAmphi()
#         
#         
#     def repartiAmphi(self) :
#         if dataBrutes.apogee 
#             self.apogee = dataBrutes.apogee.data
#             self.moodle = dataBrutes.moodle.data
#             self.rempliAmphiApogee()
#         else :
#             self.rempliAmphiMoodle()
#  
#     def decodeCodeAmphi(code: str) -> str:
#         match code:
#             case 'SAMPINFO': return 'Informatique'
#             case 'SAMPVAL':  return 'Petit_Valrose'
#             case 'SPHYS2':   return 'Sc_Physiques'
#             case 'SAMPBIOL': return 'Biologie'
#             case 'SAMPHIM':  return 'Mathématiques'
#             case 'SCHIMIE':  return 'Chimie'
#             case 'SAMPGEOL': return 'Géologie'
#             case 'SSNAT':    return 'Sc_Naturelles'
#             case _:          raise ValueError(f"Code inconnu: {code}. Revoir le fichier Apogée.")
#        
#     
#     def rempliAmphiApogee(self) :
#          
#         # on parcourt les data apogee et on rempli la liste de l'amphi en cours.
#         # si un nouveau nom d'amphi apparait alors on crée une nouvelle instance d'amph
#         listCode : list [str] =[]
#         for k in range (len(self.apogee) ) :
#             nomAmphi = decodeCodeAmphi (self.apogee[k])
#             if nomAmphi not in listCode : # on crée une nouvelle instance
#                 amphiARemplir = amphi(nomAmphi,"")
#             amphiARemplir.ajouteEtudiant(
#                 
#             
# 
#     def rempliAmphiMoodle(self) :
#         pass 
#         
#         