import subprocess
import os
import copy

from app.classes.c2_0_classeS_etudiant_a_amphi import amphi # pour avoir la descripteur amphi valide
from app.classes.c7_classe_codeEnteteApoge import codeEnteteApogee

from app.utils.utilitaire_UI_saisirDonneesEpreuve import UI_saisirDonneesEpreuve

def generer_fichier_latex(nom_fichier,
                          annee_universitaire,
                          date,
                          horaires,
                          duree,
                          salle,
                          lieu,
                          batiment,
                          epreuve,
                          matiere,
                          nom_image,
                          fic_tex_in,
                          fic_tex_in2,
                          scale,
                          angle):


    contenu = f"""% !TeX TS-program = lualatex
    \\documentclass[french]{{article}}

    \\renewcommand{{\\familydefault}}{{\\sfdefault}} % Définit la police sans-serif par défaut
    \\makeatletter \\renewcommand\\normalsize{{
            \\@setfontsize\\normalsize{{12pt}}{{16pt}}% police à 12 interligne à 16
    }}
     \\makeatother
     
    \\usepackage[left=1.5cm,right=1.5cm,top=2cm,bottom=2cm]{{geometry}}

    \\usepackage[utf8]{{inputenc}} % Encodage UTF-8
    \\usepackage[T1]{{fontenc}}    % Police T1 pour caractères accentués
    \\usepackage[french]{{babel}} % Langue française

    \\usepackage{{lastpage}}
    \\usepackage{{graphicx}}
    \\usepackage{{setspace}}
    \\usepackage{{fancyhdr}}
    \\usepackage{{textcomp}}
    \\usepackage{{tabularx}}
    \\usepackage{{needspace}}

    \\pagestyle{{fancy}}
        \\lhead{{\\textbf{{Université Côte d'Azur}}}}  
        \\chead{{ {annee_universitaire} }}  
        \\rhead{{Date : {date} }}  
        \\cfoot{{\\thepage/\\pageref{{LastPage}}}} %
    \\renewcommand{{\\headrulewidth}}{{0.4pt}} 
    \\renewcommand{{\\footrulewidth}}{{0.4pt}}

    \\begin{{document}}

    \\textbf{{Date : {date}}} \\hfill  \\textbf{{Horaires {horaires}}} \\hfill \\textbf{{Durée {duree}}} \\par \\noindent

    Salle : {salle} \\hfill {lieu} \\hfill Bâtiment : {batiment} \\par \\noindent 

    Epreuve : {epreuve} \\hspace{{3cm}} {matiere} \\vspace{{5mm}}

    \\input{{{fic_tex_in}}}
    \\newpage
    \\includegraphics[scale={scale}, angle={angle}]{{{nom_image}}}
   \\newpage 
    \\input{{{fic_tex_in2}}}
    \\end{{document}}
    """    
    with open(nom_fichier, 'w', encoding='utf-8') as f:
            f.write(contenu)
            print(f"Ecriture du fichier {nom_fichier}")
            
    return # juste pour marquer  la fin de la procedure!!!        

def definitionNouvelleListePlaceNomPrenomNumero(Amphi):
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
        
            
def generer_tableau_liste_ordre_alphabetique(listeOrdreAlphabetiX: list[list[str]],
                                             fichierTexAlpha: str = "table_alpha.tex") :
    """
    Génère un fichier LaTeX 'fichierTexAlpha' contenant un tableau à 4 colonnes :
      - Place (1.5cm)
      - Nom   (4.5cm)
      - Prénom (4.5cm)
      - Numéro (3cm)    
    """
    def debutNouvellePage(contenu):
        contenu.append("\\begin{tabular}{@{}|p{1.5cm}|p{4.5cm}|p{4.5cm}|p{3cm}|@{}}\n")
        contenu.append("  \\hline\n")
        contenu.append("  \\textbf{Place} & \\textbf{Nom} & \\textbf{Prénom} & \\textbf{Numéro} \\\\\n")
        contenu.append("  \\hline\n")
    
    # En-tête + tableau (largeurs exactes via @{ } et \tabcolsep=0pt)
    contenu : list[list[str]] = []
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
        
        contenu.append(f"  {place} & {nom} & {prenom} & {numero} \\\\ \\hline\n")
        
        if (k+1)%36 ==0 and k < k_max-1 : # on change de page         
            contenu.append("\\end{tabular}\n")
            contenu.append("\\newpage\n\n")
            debutNouvellePage(contenu) # début de la nouvelle page
    
    # Fermeture finale
    contenu.append("\\end{tabular}\n")
    contenu.append("}\n")  # fin du scope \setlength{\tabcolsep}{0pt}

    with open(fichierTexAlpha, "w", encoding="utf-8") as f:
        f.write("".join(contenu))



def generer_tableau_emargement_amphi(Amphi, ficLatex="table.tex"):
    """
    Génère un fichier LaTeX 'table.tex' contenant, pour chaque rang de chaque zone
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
            
            # Début bloc non sécable
            debut_samepage = "\\begin{samepage}\n"
            # En-tête "Rang N° avec le caractère \\\\[2pt]  pour retour à la ligne."
            
            en_tete = (
                f"\\par\\noindent\\textbf{{Rang N\\textdegree~{numero_rang} — Zone {zone_label}}}\\\\[2pt]\n"
                        )

            # Début du tableau (structure imposée)
            table = (
                "\\begin{tabularx}{18cm}{|p{1.5cm}|p{3.75cm}|p{3.75cm}|p{2cm}|X|}\n"
                "    \\hline\n"
                "    Place & Nom & Prénom & Numéro & Signature \\\\\n"
                "    \\hline\n"
            )

            # Lignes du tableau
            for etu in etudiants:
                nom = getattr(etu, "nom")
                prenom = getattr(etu, "prenom")
                numero = getattr(etu, "numeroEtudiant")
                num_rang = getattr(etu, "numeroRang")
                num_place = getattr(etu, "numeroPlace")
                # Place formatée : Zone-Rang-Place
                place_fmt = f"{zone_label}-{num_rang}-{num_place}"
                table = table + (
                    f"  \\rule{{0pt}}{{1.5cm}} {place_fmt} & {nom} & {prenom} & {numero} & \\\\ \\hline\n"
                )

            table = table + "\\end{tabularx}\n"

            # Fin bloc non sécable + petit espace
            fin_samepage = "\\end{samepage}\n\\par\\medskip\n"

            blocs.append(reserve + debut_samepage + en_tete   + table + fin_samepage)
        # --- Fin de litération de la boucle sur le contenu de la zone : saut de page ---
        blocs.append("\\newpage\n")

    # Assemble tous les blocs dans un unique fichier
    contenu = "".join(blocs) if blocs else "% Aucun rang/étudiant à afficher.\n"
    with open(ficLatex, "w", encoding="utf-8") as f:
        f.write(contenu)

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

def genererPdf(Amphi : amphi ,  # besoin pour définir des param graphiques 
              cheminRepTex : str ,
              cheminRepPdf : str ,
              entetePdf : list[str] ,
              root ) :
    
    fichierTableTex        = cheminRepTex+"/table.tex"
    fichierOrdreAlphabetiX = cheminRepTex+"/table_alpha.tex"
    fichierPrincipalTex    = cheminRepTex+f"/{Amphi.nom}.tex"
    
    generer_tableau_emargement_amphi(Amphi, ficLatex= fichierTableTex)
    
    listeOrdreAlphabetiX = definitionNouvelleListePlaceNomPrenomNumero( Amphi )
    generer_tableau_liste_ordre_alphabetique( listeOrdreAlphabetiX , fichierOrdreAlphabetiX ) 
        
    # appel de la fonction.
    if len(Amphi.zones)==3 : # detection facile du PV
        echelle : float  = 0.5
        angleRot : int  = 90
    elif len(Amphi.zones)==2:
        echelle : float =  0.7
        angleRot : int = 90
    else :
        echelle : float =  0.7
        angleRot : int = 0

         
             
           
            
            
           
    generer_fichier_latex(  nom_fichier =  fichierPrincipalTex ,
                            annee_universitaire = entetePdf.annee_universitaire ,
                            date =    entetePdf.date ,        
                            horaires = entetePdf.horaires,
                            duree =  entetePdf.duree ,       
                            salle=   '',            
                            lieu=   'Valrose',             
                            batiment= entetePdf.LIB_SAL,
                            epreuve=  entetePdf.epreuve ,         
                            matiere= '',
                            nom_image=             Amphi.nomFicPlanAmphiPng,
                            fic_tex_in=            fichierTableTex ,
                            fic_tex_in2=           fichierOrdreAlphabetiX,
                            scale=  echelle ,
                            angle= angleRot)
#     else : # mode =="Partiel"
        # saisie des paramètres inexistants
        
#         generer_fichier_latex(  fichierPrincipalTex , annee_universitaire , date ,horaires ,duree ,salle,lieu,
#                               batiment,epreuve, matiere= '',
#                               nom_image=             Amphi.nomFicPlanAmphiPng,
#                               fic_tex_in=            fichierTableTex ,
#                               fic_tex_in2=           fichierOrdreAlphabetiX,
#                               scale=  echelle ,
#                               angle= angleRot)                   
    
    compiler_latex(fichierPrincipalTex,cheminRepPdf) 





