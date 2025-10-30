#apreès avoir quitter proprement
#permet d'afficher uniquement les étudiants.
    
for rang in app.listAmphi[0].zones[0].listeRangDansZoneAmphi:
    for etu in rang.listeEtudiant:
        print(etu)