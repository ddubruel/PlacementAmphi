print(app.tousLesEtudiants.listeDesEtudiants[0])
k=0
for etudiant in app.tousLesEtudiants.listeDesEtudiants :
    print( etudiant.courriel)

    
print( [(et.nom,et.courriel) for et in app.tousLesEtudiants.listeDesEtudiants[0:10] ]) 