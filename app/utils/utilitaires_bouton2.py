from  app.classes.c2_0_classeS_etudiant_a_amphi import amphi,rangDansZoneAmphi
from classes.c5_tracePlanAmphiEtGenerefichier import tracePlanAmphiEtGenerefichier 


    
    

def genererLesPngPlacesIndividuelles(Amphi,arborescence,root,listeFenetreGraphiqueVisuAmphi):
    """ cette méthode affiche et génère avec une temporisation de 200 ms les
    fichier png pour chaque étudiant.  1 minute maxi pour 300 étudiants """
    Amphi.entourePlace = True # on autorise le tracé des ellipses autour des places
    trace=tracePlanAmphiEtGenerefichier(Amphi, arborescence, root)
    
    listeFenetreGraphiqueVisuAmphi.append(trace.window)
        # verif de l'attibut liste des fichiers png dans la zone.                           
    root.update_idletasks()  # rafraîchit l’interface avant de lancer le traitement

    # fin de genererLesPngPlacesIndividuelles


def remplitRangCompleteEtudiant(Amphi):
    # remplissage des classes Etudiant pour tous les étudiants.
        
    for nmrZone in range(len(Amphi.zones))  :
        nbRang =   Amphi.zones[nmrZone].nbRang
        # instanciation des rangs vides
        listeRang=[] # attention indice 0 pour le rang 1 !!!!
        for nmrRang in range(1,nbRang+1) :
            listeRang.append(rangDansZoneAmphi( numeroRang = nmrRang , listeEtudiant=[]  ))
            #print('nmrRang =',nmrRang ,'listeRang[ ]=',listeRang[nmrRang-1])
            #print()
        for  k, (row,col)  in enumerate (Amphi.zones[nmrZone].placement) :
            # remplissage des attributs non encore définit pour les étudiants 
            etudiantPourLeRang = Amphi.zones[nmrZone].listeDesEtudiantDansLaZone[k]
            etudiantPourLeRang.set_numeroPlace(col)
            etudiantPourLeRang.set_numeroRang(row)
            if len(Amphi.zones[nmrZone].liste_nom_fic_png)!=0 : # cas où les fichiers png existent :
                nomFichierPng = Amphi.zones[nmrZone].liste_nom_fic_png[k]
            else :
                nomFichierPng=""                                                   
            # remplissage du rang (indice 0 pour le rang 1 !!!)
            etudiantPourLeRang.set_fichierPng(nomFichierPng)
            listeRang[row-1].ajouterEtudiant(etudiantPourLeRang)
        # ajout des rangs remplis d'etudiants dans la zone.
        #print("longueur liste = ", len(listeRang)) 
        for nmrRang in range(1,nbRang+1) :
            #print('nmrRang =',nmrRang)
            #print(listeRang[nmrRang-1])
            Amphi.zones[nmrZone].ajouterRang(listeRang[nmrRang-1])
