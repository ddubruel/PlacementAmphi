import subprocess
import os
import copy

from textwrap import dedent

from app.classes.c2_0_classeS_etudiant_a_amphi import amphi # pour avoir la descripteur amphi valide
from app.classes.c7_classe_codeEnteteApoge import codeEnteteApogee

from app.utils.utilitaire_UI_saisirDonneesEpreuve import UI_saisirDonneesEpreuve

def latex_escape(s: str) -> str:
    return (s.replace("\\", "\\textbackslash{}")
            .replace("&", "\\&")
            .replace("%", "\\%")
            .replace("$", "\\$")
            .replace("#", "\\#")
            .replace("_", "\\_")
            .replace("{", "\\{")
            .replace("}", "\\}")
            .replace("~", "\\textasciitilde{}")
            .replace("^", "\\textasciicircum{}"))


def definitionNouvelleListePlaceNomPrenomNumero(Amphi) ->list[list[str]]:
    listeOrdreAlphabetiX : list[list[str]] = []
    # Parcours des zones
    for idx_zone, zone in enumerate(Amphi.zones):
        zone_label = getattr(zone, "labelZone")
        liste_rangs: list = getattr(zone, "listeRangDansZoneAmphi")
        # Parcours des rangs de la zone
        for rang in liste_rangs:    
            etudiants = getattr(rang, "listeEtudiant", [])
            
            # Parcours des étudiants du rang
            for etu in etudiants:
                nom = getattr(etu, "nom", "")
                prenom = getattr(etu, "prenom", "")
                numero = getattr(etu, "numeroEtudiant", "")
                num_rang = getattr(etu, "numeroRang")
                num_place = getattr(etu, "numeroPlace", "")
                # Place formatée : Zone-Rang-Place sauf si une seule zone Rang-Place
                if zone_label!="":
                    place_fmt = f"{zone_label}-{num_rang}-{num_place}"
                else :
                    place_fmt = f"{num_rang}-{num_place}"
                    
                listeOrdreAlphabetiX.append([place_fmt , nom.upper() , prenom.upper() , numero])
    # Tri alphabétique sur le NOM (champ [1])
    listeOrdreAlphabetiX.sort(key=lambda x: x[1])
    
    return listeOrdreAlphabetiX

            
def ajoutTableauPourAffichage(contenuLatex :list[str],
                            enteteTableau : list[str],
                            listeOrdreAlphabetiX: list[list[str]],
                            ) :   
    for k in range(len(enteteTableau)):
        enteteTableau[k]=latex_escape(enteteTableau[k])
        
    def debutTableau(entete, contenu)-> None:
        contenu.append("{\\setlength{\\tabcolsep}{0pt}%\n")
        contenu.append(
                "\\begin{tabular}{@{}|"
                ">{\\centering\\arraybackslash}p{3cm}|"
                ">{\\centering\\arraybackslash}p{3cm}|" 
                "@{}}\n" )
        contenu.append("  \\hline\n")
        contenu.append(
            f"  \\textbf{{{entete[0]}}} & "
            f"\\textbf{{{entete[1]}}} \\\\\n"
        )
        contenu.append("  \\hline\n")
    
    def ajoutLigneTableau(numero:str, place:str, contenu:list[str])-> None:
        contenu.append(f"  {numero} & {place} \\\\ \\hline\n")
        
    def finTableau(contenu)-> None:
        contenu.append("\\end{tabular} \\par % pour fermer centering\n")
        contenu.append("}\n")  # fin du scope \setlength{\tabcolsep}{0pt}
        
    def nouvelleZoneDoubleCol() -> None:
        contenu.append("{\\centering\n")
        contenu.append("\\begin{multicols}{2}\n")
        
    def finZoneDoubleCol() -> None:
        contenu.append("\\end{multicols}\n")
            
    contenu : list[str] = []    
    contenu.append("\\begin{center}\\textbf{LISTE AVEC NUMEROS CROISSANTS}\\end{center}\\par\\medskip\n")

    k_max : int =len(listeOrdreAlphabetiX)
    tableauACreer : bool =True
    tableauOuvert : bool =False 
    colonneGauche : bool =True
    zoneDouble : bool
    nouvelleZoneDoubleCol()  
    zoneDouble=True
    for k, row in enumerate(listeOrdreAlphabetiX):                
        if tableauACreer :
            debutTableau(enteteTableau, contenu)
            tableauOuvert =True
            tableauACreer = False
            
        numero = row[0] if len(row) > 0  else ""
        place  = row[1] if len(row) > 1 else ""        
        place =latex_escape(place)
        ajoutLigneTableau(numero, place, contenu)
        
        if (k+1)%30 ==0 and k < k_max-1 : # on change de colonne ou de page
            tableauACreer = True
            finTableau(contenu)  
            tableauOuvert=False  
            
            if colonneGauche  : 
                colonneGauche =False
                contenu.append("\\newcolumn\n")
            else :
                colonneGauche =True
                finZoneDoubleCol() 
                zoneDouble=False
                contenu.append("\\newpage\n\n")
                nouvelleZoneDoubleCol()
                zoneDouble=True
                
    # Fermeture finale
    if tableauOuvert :
        finTableau(contenu)
        finZoneDoubleCol()
    elif  zoneDouble  :
        finZoneDoubleCol()
        
    for ligne in contenu:
        contenuLatex.append(ligne)
    # fin de la procedure ajoutTableauPourAffichage

def compiler_latex(fichier_tex,dossier_sortie):    
    os.makedirs(dossier_sortie, exist_ok=True)  # Crée le dossier s'il n'existe pas

    commande = [
        "lualatex",
        "-synctex=1",
        "-interaction=nonstopmode",
        f"-output-directory={dossier_sortie}",
        fichier_tex
    ]
    # double compilation pour avoir les numéros  de place corrects
    subprocess.run(commande, check=True)
    subprocess.run(commande, check=True)
    
    
    extensions = (".gz", ".log", ".aux")

    for fichier in os.listdir(dossier_sortie):
        chemin_fichier = os.path.join(dossier_sortie, fichier)
        if os.path.isfile(chemin_fichier) and fichier.endswith(extensions):
            try:
                os.remove(chemin_fichier)
                print(f"Suppression de {fichier}")
            except OSError as e:
                print(f"Impossible de supprimer {fichier} : {e}")
    
    #print(f"\n Pour information, le fichier pdf a été compilé avec les commandes : \n  {' '.join(commande)} ")
    
def ajoutePreambuleLatex(contenuLatex:list[str], nomAmphi,epreuve, date, horaires )-> None:
    
    # utiliser dedent(chaine).lstrip()  pour eviter les indentations parasites et supprimer la premiere ligne vide.

    date=latex_escape(date)
    nomAmphi=latex_escape(nomAmphi)
    horaires=latex_escape(horaires)
    epreuve=latex_escape(epreuve)

    contenu = f"""% !TeX TS-program = lualatex
    \\documentclass[french]{{article}}
    \\renewcommand{{\\familydefault}}{{\\sfdefault}} % Définit la police sans-serif par défaut
    \\makeatletter \\renewcommand\\normalsize{{
            \\@setfontsize\\normalsize{{12pt}}{{16pt}}% police à 12 interligne à 16
    }}
    \\makeatother
    \\usepackage[left=1.5cm,right=1.5cm,top=2cm,bottom=2cm]{{geometry}}
    \\usepackage[T1]{{fontenc}}    % Police T1 pour caractères accentués
    \\usepackage[french]{{babel}} % Langue française

    \\usepackage{{lastpage}}
    \\usepackage{{graphicx}}
    \\usepackage{{setspace}}
    \\usepackage{{fancyhdr}}
    \\usepackage{{textcomp}}
    \\usepackage{{tabularx}}
    \\usepackage{{needspace}}
    \\usepackage{{multicol}}"""

    

    # retrait des indentations parasites et suppression de la premiere ligne vide.
    contenu = dedent(contenu).lstrip()    
    contenuLatex.append(contenu)
    # fin de la procedure ajoutePreambuleLatex

def ajouteDefinitionHautEtBasPages( typeEntete :str, 
                                contenuLatex:list[str],
                                date : str , 
                                annee_universitaire : str ,
                                horaires : str ,
                                nomAmphi : str) -> None:    
    annee_universitaire=latex_escape(annee_universitaire)
    date=latex_escape(date)
    nomAmphi=latex_escape(nomAmphi)
    if typeEntete=="enteteApogee":
        contenu = f"""
        \\pagestyle{{fancy}}
            \\lhead{{\\textbf{{Université Côte d'Azur}}}}  
            \\chead{{ {annee_universitaire} }}  
            \\rhead{{Date : {date} }}  
            \\cfoot{{\\thepage/\\pageref{{LastPage}}}} %
            \\lfoot {{ Amphithéatre {nomAmphi} }}
            \\rfoot {{ horaire : {horaires} }}
        \\renewcommand{{\\headrulewidth}}{{0.4pt}} 
        \\renewcommand{{\\footrulewidth}}{{0.4pt}}"""
    else  : 
        contenu = f"""
        \\pagestyle{{fancy}}
            \\lhead{{\\textbf{{Université Côte d'Azur}}}}  
            \\chead{{ {annee_universitaire} }}  
            \\rhead{{Date : {date} }}  
            \\cfoot{{\\thepage/\\pageref{{LastPage}}}} %
            \\lfoot {{ Amphithéatre {nomAmphi} }}
            \\rfoot {{ horaire : {horaires} }}
        \\renewcommand{{\\headrulewidth}}{{0.4pt}} 
        \\renewcommand{{\\footrulewidth}}{{0.4pt}}"""
            
    # retrait des indentations parasites et suppression de la premiere ligne vide.
    contenu = dedent(contenu).lstrip()    
    contenuLatex.append(contenu)
    # fin de la procedure ajouteDefinitionHautEtBasPages
    
    
def ajouteTableauEmargementAmphi( contenuLatex:list[str], Amphi: amphi ) -> None: 
    """
    Génère la partie du fichier LaTeX  contenant, pour chaque rang de chaque zone
    de l'amphi, un tableau d'émargement avec colonnes :
    Place (ex: A-3-1), Nom, Prénom, Numéro, Signature.
    Un tableau par rang, précédé de 'Rang N {row}', non coupé sur deux pages.
    Saut de page après chaque Zone.
    """
    blocs = []
    # Parcours des zones
    for idx_zone, zone in enumerate(Amphi.zones):
        # Tente de récupérer un label lisible pour la zone (ex: 'A'),
        zone_label = getattr(zone, "labelZone")           
        titre_zone = (
            f"\\begin{{center}}\\textbf{{Zone {zone_label}}}\\end{{center}}\\par\\medskip\n"
        )
        titre_zone=dedent(titre_zone).lstrip()
        blocs.append(titre_zone)
        # Liste des rangs        
        liste_rangs :list [rangDansZoneAmphi] = getattr(zone, "listeRangDansZoneAmphi")
        # extraction des rangs remplis :
        listeRangsRemplis :list [rangDansZoneAmphi] =[]        
        for rang in liste_rangs:
            etudiants = getattr(rang, "listeEtudiant")
            if len(etudiants)!=0 :
                listeRangsRemplis.append(rang)
        for rang in listeRangsRemplis:
            etudiants = getattr(rang, "listeEtudiant")
            numero_rang = getattr(rang, "numeroRang")
            
            # calcul de la place à réserver pour le tableau à venir.
            n = len(etudiants)
            need_cm = 3.5 + 1.5 * n  # 3.5 cm ~ titre + entête tableau + petite marge
            # Réserve l'espace pour garder titre + tableau sur la même page
            reserve = f"\\Needspace{{{need_cm:.1f}cm}}\n"
            reserve=dedent(reserve).lstrip()
            blocs.append(reserve)
            # Début bloc non sécable
            debut_samepage = "\\begin{samepage}\n"
            debut_samepage=dedent(debut_samepage).lstrip()
            blocs.append(debut_samepage)
            # En-tête "Rang N° avec le caractère \\\\[2pt]  pour retour à la ligne."            
            numero_rang=numero_rang
            zone_label=latex_escape(zone_label)
            en_tete = (
                f"\\par\\noindent\\textbf{{Rang N\\textdegree~{numero_rang} --- Zone {zone_label}}}\\\\[2pt]\n"
                        )
            en_tete=dedent(en_tete).lstrip() 
            blocs.append(en_tete)           
            # Début du tableau (structure imposée)
            table = (
                "\\begin{tabularx}{18cm}{|p{1.5cm}|p{3.75cm}|p{3.75cm}|p{2cm}|X|}\n"
                "    \\hline\n"
                "    Place & Nom & Prénom & Numéro & Signature \\\\\n"
                "    \\hline\n"
            )
            table=dedent(table).lstrip()
            blocs.append (table )
            # Lignes du tableau
            for etu in etudiants:
                nom = getattr(etu, "nom")
                prenom = getattr(etu, "prenom")
                numero = getattr(etu, "numeroEtudiant")
                num_rang = getattr(etu, "numeroRang")
                num_place = getattr(etu, "numeroPlace")
                # Place formatée : Zone-Rang-Place
                
                # Place formatée : Zone-Rang-Place sauf si une seule zone Rang-Place
                if zone_label!="":
                    place_fmt = f"{zone_label}-{num_rang}-{num_place}"
                else :
                    place_fmt = f"{num_rang}-{num_place}"
                place_fmt=dedent(place_fmt).lstrip()
                
                nom=latex_escape(nom)
                prenom=latex_escape(prenom)
                ligne : str =  (
                    f"  \\rule{{0pt}}{{1.5cm}} {place_fmt} & {nom.upper()} & {prenom.upper()} & {numero} & \\\\ \\hline\n"
                )
                ligne=dedent(ligne).lstrip()
                blocs.append(ligne)
            blocs.append("\\end{tabularx}\n")            
            # Fin bloc non sécable + petit espace
            fin_samepage = "\\end{samepage}\n\\par\\medskip\n"
            blocs.append(fin_samepage)
        # --- Fin de litération de la boucle sur le contenu de la zone : saut de page ---
        blocs.append("\\newpage\n")
    for ligne in blocs:        
        contenuLatex.append(ligne)
    # fin de la procedure ajouteTableauEmargementAmphi

def definirParametresGraphiquesAmphi( Amphi : amphi ) -> tuple[float,int]  :
    if len(Amphi.zones)==3 : # detection facile du PV
            echelle : float  = 0.5
            angleRot : int  = 90
    elif len(Amphi.zones)==2:
            echelle : float =  0.7
            angleRot : int = 90
    else :
            echelle : float =  0.7
            angleRot : int = 0    
    return echelle, angleRot
    
def  ajouteImagePlanAmphi( contenuLatex:list[str], nomFicPlanAmphiPng : str ,scale : float , angle :int ) -> None:
    nomFicPlanAmphiPng=latex_escape(nomFicPlanAmphiPng)
    contenu :str  = f"""
    \\begin{{center}}
    \\includegraphics[scale={scale}, angle={angle}]{{{nomFicPlanAmphiPng}}}
    \\end{{center}}
    \\newpage
    """
    # retrait des indentations parasites et suppression de la premiere ligne vide.
    contenu = dedent(contenu).lstrip()    
    contenuLatex.append(contenu)
    # fin de la procedure ajouteImagePlanAmphi  

def ajouteTableauOrdreAlphabetique( contenuLatex, listeOrdreAlphabetiX ) -> None:
    """
    Génère un fichier LaTeX 'fichierTexAlpha' contenant un tableau à 4 colonnes :
        - Place (1.5cm)
        - Nom   (4.5cm)
        - Prénom (4.5cm)
        - Numéro (3cm)    
    """
    def debutNouvellePage(contenu: list[str]):
        contenu.append("\\begin{tabular}{@{}|p{1.5cm}|p{6.5cm}|p{6.5cm}|p{3cm}|@{}}\n")
        contenu.append("\\hline\n")
        contenu.append("\\textbf{Place} & \\textbf{Nom} & \\textbf{Prénom} & \\textbf{Numéro} \\\\\n")
        contenu.append("\\hline\n")
    # En-tête + tableau (largeurs exactes via @{ } et \tabcolsep=0pt)
    contenu : list[str] = []
    contenu.append("\\begin{center}\\textbf{LISTE PAR ORDRE ALPHABÉTIQUE}\\end{center}\\par\\medskip\n")
    contenu.append("{\\setlength{\\tabcolsep}{0pt}%\n")
    debutNouvellePage(contenu)
    k_max : int =len(listeOrdreAlphabetiX)
    for k, row in enumerate(listeOrdreAlphabetiX):        
        # Attendu : [place_fmt, nom, prenom, numero]
        place  = row[0] if len(row) > 0 else ""
        nom    = row[1] if len(row) > 1 else ""
        prenom = row[2] if len(row) > 2 else ""
        numero = row[3] if len(row) > 3 else ""        
        place =latex_escape(place)
        nom =latex_escape(nom)
        prenom =latex_escape(prenom)                
        contenu.append(f"{place} & {nom} & {prenom} & {numero} \\\\ \\hline\n")        
        if (k+1)%36 ==0 and k < k_max-1 : # on change de page         
            contenu.append("\\end{tabular}\n")
            contenu.append("\\newpage\n\n")
            debutNouvellePage(contenu) # début de la nouvelle page    
    # Fermeture finale
    contenu.append("\\end{tabular}\n")
    contenu.append("}\n")  # fin du scope \setlength{\tabcolsep}{0pt}
    for ligne in contenu:
        contenuLatex.append(ligne)
    # fin de la procedure ajouteTableauOrdreAlphabetique
    
def compilerContenuLatex(contenuLatex: list[str],cheminRepPdf : str ,fichierTex : str )-> None:
    
    with open(fichierTex, "w", encoding="utf-8") as f:
        for ligne in contenuLatex:
            if not ligne.endswith("\n"):  # pour être sûr qu'il y a un saut de ligne à la fin de chaque ligne
                ligne += "\n"
            f.write(ligne)
    print(f"Ecriture du fichier {fichierTex}")
            
    os.makedirs(cheminRepPdf, exist_ok=True)  # Crée le dossier s'il n'existe pas
    commande = [
        "lualatex",
        "-synctex=1",
        "-interaction=nonstopmode",
        f"-output-directory={cheminRepPdf}",
        fichierTex
    ]
    # double compilation pour avoir les numéros  de place corrects
    subprocess.run(commande, check=True)
    subprocess.run(commande, check=True)
        
    extensions = (".gz", ".log", ".aux")

    for fichier in os.listdir(cheminRepPdf):
        chemin_fichier = os.path.join(cheminRepPdf, fichier)
        if os.path.isfile(chemin_fichier) and fichier.endswith(extensions):
            try:
                os.remove(chemin_fichier)
                print(f"Suppression de {fichier}")
            except OSError as e:
                print(f"Impossible de supprimer {fichier} : {e}")
    
    print(f"\n Pour information, le fichier pdf a été compilé avec les commandes : \n  {' '.join(commande)} ")

def ajouteDebutPage( contenuLatex : list[str],
                    nomAmphi : str ,
                    date : str ,
                    horaires : str ,
                    duree : str,                    
                    epreuve : str ,                                       
                    ) -> None:
    salle=latex_escape(nomAmphi)
    date=latex_escape(date)
    horaires=latex_escape(horaires)
    duree=latex_escape(duree)
    epreuve=latex_escape(epreuve)

    lieu=latex_escape("Valrose")        

    
    contenu =f"""\\textbf{{Date : {date}}} \\hfill  \\textbf{{Horaires {horaires}}} \\hfill \\textbf{{Durée {duree}}} \\par \\noindent
    Amphithéatre : {salle} \\hfill {lieu} \\hfill  \\par \\noindent 
    Epreuve : {epreuve} \\hspace{{3cm}} \\vspace{{5mm}} """
    contenu = dedent(contenu).lstrip()
    contenuLatex.append(contenu)
    
    
def genererPdf(Amphi : amphi ,  # besoin pour définir des param graphiques 
            cheminRepTex : str ,
            cheminRepPdf : str ,
            entetePdf : list[str] ,
            root ) :
    
    # Génération de la liste d'émargement + plan amphi + liste alphabétique.
    contenuLatex : list[str] =[]
    ajoutePreambuleLatex(contenuLatex, Amphi.nom, entetePdf.epreuve, entetePdf.date, entetePdf.horaires)
    ajouteDefinitionHautEtBasPages( "enteteApogee",
                                contenuLatex, 
                                entetePdf.date , 
                                entetePdf.annee_universitaire, 
                                entetePdf.horaires,
                                Amphi.nom )
    contenuLatex.append("\\begin{document}")
    ajouteDebutPage(contenuLatex,Amphi.nom,entetePdf.date,entetePdf.horaires,entetePdf.duree, entetePdf.epreuve)
    
    ajouteTableauEmargementAmphi( contenuLatex, Amphi )
    echelle, angleRot = definirParametresGraphiquesAmphi(Amphi)    
    ajouteImagePlanAmphi( contenuLatex, Amphi.nomFicPlanAmphiPng, echelle, angleRot )
    listeOrdreAlphabetiX = definitionNouvelleListePlaceNomPrenomNumero( Amphi )
    ajouteTableauOrdreAlphabetique( contenuLatex, listeOrdreAlphabetiX )
    contenuLatex.append("\\end{document}")
    nomAmphi : str =Amphi.nom.replace("_", "")  # pour éviter le plantage à la compilation tex
    fichierTex = cheminRepTex+f"/{nomAmphi}.tex"
    compilerContenuLatex(contenuLatex, cheminRepPdf,fichierTex)
        
    # creation des listes pour affichage devant les amphis
    contenuLatex : list[str] =[]
    ajoutePreambuleLatex(contenuLatex, Amphi.nom, entetePdf.epreuve, entetePdf.date, entetePdf.horaires)
    ajouteDefinitionHautEtBasPages( "",
                                contenuLatex,
                                entetePdf.date,
                                entetePdf.annee_universitaire,
                                entetePdf.horaires,
                                Amphi.nom )
    contenuLatex.append("\\begin{document}")
    ajouteDebutPage(contenuLatex,Amphi.nom,entetePdf.date,entetePdf.horaires,entetePdf.duree, entetePdf.epreuve)    
    # la liste des élémént à afficher : 
    listeNmrPlace : list[list[str]]=[ [numero, place] for place, _, _, numero in listeOrdreAlphabetiX ]
    # Tri alphabétique sur le numero (qui est une str ) (champ [1])
    listeNmrPlace.sort(key=lambda x: x[0])
    enteteTableau : list[str] = ['Numero Etudiant','Place']
    ajoutTableauPourAffichage(contenuLatex, enteteTableau, listeNmrPlace )   
    echelle, angleRot = definirParametresGraphiquesAmphi(Amphi)    
    ajouteImagePlanAmphi( contenuLatex, Amphi.nomFicPlanAmphiPng, echelle, angleRot ) 
    contenuLatex.append("\\end{document}")
    nomAmphi=nomAmphi.replace("_", "")  # pour éviter le plantage à la compilation tex
    fichierAffichageNmrPlace   = cheminRepTex+f"/PourAffichage_1_{Amphi.nom}.tex"
    compilerContenuLatex(contenuLatex, cheminRepPdf, fichierAffichageNmrPlace)   

        
    
    
    
    




