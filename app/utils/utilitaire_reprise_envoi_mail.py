
import tkinter as tk
import json
import os,sys
import csv
import time 

from tkinter import messagebox
from utils.utilitaire_EnvoiMail import  envoyerMail

from app.utils.utilitaire_json import recupJson
from app.utils.utilitaire_sauvegarde import sauvegarder_compileClasseMail

from classes.c8_classe_mailConfig import mailConfig
from classes.c9_classe_dataEpreuve import dataEpreuve
from classes.c10_classe_compileClasseMail import compileClasseMail

def ouvrir_fenetre_interruption(parent, dataMail : compileClasseMail , repertoire : str , envoiReel : bool ) :
    global controleur_ok, _win_interruption 
    """Ouvre une petite fenêtre avec 'Interuption des envoi' et un bouton 'interuption'."""
    controleur_ok = True  # réinitialise le contrôleur à OK
    _win_interruption = tk.Toplevel(parent)
    _win_interruption.title("Interuption des envoi")
    _win_interruption.resizable(False, False)
    _win_interruption.transient(parent)
    _win_interruption.grab_set()

    frm = tk.Frame(_win_interruption, padx=12, pady=12)
    frm.pack(fill="both", expand=True)

    tk.Label(
        frm,
        text="Interuption des envois.",
        font=("Arial", 12, "bold")
    ).pack(pady=(0, 10))

    tk.Button(
        frm,
        text="interuption",
        width=14,
        command=lambda: _declencher_interuption(dataMail, repertoire, envoiReel)
    ).pack()

    # Si on ferme la fenêtre avec la croix, on laisse l'envoi continuer
    _win_interruption.protocol("WM_DELETE_WINDOW", _fermer_sans_interrompre)


def _declencher_interuption(dataMail : compileClasseMail , repertoire : str , envoiReel:bool ):
    global controleur_ok, _win_interruption
    """Appelé quand on clique sur le bouton 'interuption'."""
    controleur_ok = False

    # On ferme la fenêtre d'interruption si elle existe
    try:
        if _win_interruption is not None and _win_interruption.winfo_exists():
            _win_interruption.destroy()
    except NameError:
        # la fenêtre n'a jamais été créée
        pass
    # On sauvegarde l'état de la classe (dataMail)
    try:
        if envoiReel :
            sauvegarder_compileClasseMail( dataMail,'Z_dataMailEnvoiReel.csv' ,repertoire)   
        else :
            sauvegarder_compileClasseMail( dataMail,'Z_dataMail.csv' ,repertoire)
    except Exception as e:
        messagebox.showerror(
            "Erreur de sauvegarde",
            f"Impossible de sauvegarder les données d'envoi :\n"
            f"{type(e).__name__} : {e}"
        )


def _fermer_sans_interrompre():
    global _win_interruption
    """Fermeture de la mini-fenêtre sans stopper l'envoi."""
    try:
        if _win_interruption is not None and _win_interruption.winfo_exists():
            _win_interruption.destroy()
    except NameError:
        pass

#####################
####################
################

def recupDonneesEtudiant(dataIn : compileClasseMail, indice : int) : 
    """Récupération des données des étudiants à partir de la liste de listes."""
    ligne : list  = dataIn[indice]
    
    nom= ligne[0],
    prenom =  ligne[1],
    numeroEtudiant =  ligne[2],
    courriel =  ligne[3],
    amphi_nom =  ligne[4],
    reference_place =  ligne[5],
    fichierPng =   ligne[6],
    statutMail =  ligne[7]  # True ou False  

    return nom,prenom,numeroEtudiant,courriel,amphi_nom,reference_place,fichierPng,statutMail
    # fin recupDonneesEtudiant  


def envoiMailauxEtudiants(parent,
                            repertoire:str,
                            dataMail : compileClasseMail,
                            setUpMail:mailConfig,
                            sujet:str,
                            corpsDuMessageCommun:str,
                            envoiReel:bool) :
    global controleur_ok

    annee_universitaire,  date, horaires, duree, epreuve = recupJson(repertoire) 
    dataEpreuvePourMail : dataEpreuve = dataEpreuve( date=date,horaires=horaires,duree=None,epreuve=epreuve ) 
                    
        
    # lancer controleur
    ouvrir_fenetre_interruption(parent, dataMail, repertoire, envoiReel)  
    
    # on définit les compteur pour les statistiques d'envoi
    nbEtudiant : int  = dataMail.nombre_etudiant()
    nbEnvoyes : int = dataMail.nombre_mail_envoye()
    
    for k in range(dataMail.nombre_etudiant() ):
        try:
            parent.update_idletasks()
            parent.update()
        except tk.TclError:
            pass  # si la fenêtre principale est fermée

        if not  controleur_ok:
            break  # stop immédiat si l'utilisateur a demandé l'interuption                
        
        nom = dataMail.nom[k]
        prenom = dataMail.prenom[k]
        numeroEtudiant = dataMail.numeroEtu[k]
        courriel = dataMail.courriel[k]
        amphi_nom = dataMail.nomAmphi[k]
        reference_place = dataMail.referencePlace[k]
        prefixeZone = dataMail.prefixeZone[k]
        numeroRang = dataMail.numeroRang[k]
        numeroPlace = dataMail.numeroPlace[k]
        fichierPng = dataMail.fichierPng[k]
        statutMail = dataMail.statutMail[k]
            
        if not statutMail : # on envoie le mail seulement si pas encore envoyé
            debut : str = f"Bonjour {prenom} \n\n"
            fin: str = (
                        f"\n\n Vous avez la place {reference_place}, amphithéâtre {amphi_nom}.\n"
                        f"Qui se trouve en Zone : {prefixeZone} — Rang n° {numeroRang} — Place n° {numeroPlace}.\n"
                        f"\n"
                        f"---Ce courriel a été envoyé automatiquement. Merci de ne pas y répondre.---"
                    )
            corpsDuMessage: str  = debut + corpsDuMessageCommun  +fin # le contenu du mail est complet            
    
            envoiReussi : bool  = envoyerMail (sujet = sujet,
                                        corpsDuMessage = corpsDuMessage,
                                        email = courriel,                      
                                        fichierPng = fichierPng ,
                                        setUpMail = setUpMail,
                                        go = envoiReel  # mis à False pour un test à blanc.
                                        )
            # Pause aléatoire entre les envois
            time.sleep(setUpMail.t_tempo)
            if envoiReussi :
                dataMail.reinitialiser_statut_k(k) # passe le statutMail de l'étudiant k à True
                nbEnvoyes =nbEnvoyes +1 
                print("Il y a ",nbEnvoyes ,'mails déja envoyés sur un total de : ',nbEtudiant," étudiants.")
                
        # sortie propre si demande d'arrêt
        if not controleur_ok:
            break        
    # ---> FERMETURE DE LA FENÊTRE D'INTERRUPTION après la boucle d'envoi terminée 
    try:
        if _win_interruption is not None and _win_interruption.winfo_exists():
            _win_interruption.destroy()
    except NameError:
        pass
            
    messagebox.showinfo("Bilan des envois",f"{nbEnvoyes} mails envoyés pour {nbEtudiant} étudiants.")
    if envoiReel :
        sauvegarder_compileClasseMail( dataMail,'Z_dataMailEnvoiReel.csv' ,repertoire)   
    else :
        sauvegarder_compileClasseMail( dataMail,'Z_dataMail.csv' ,repertoire)
        
    if nbEnvoyes < nbEtudiant :
        messagebox.showinfo("Bilan des envois","Essayez de relancer l'envoi des mails, maintenant ou plus tard.")
    else:
        messagebox.showinfo("Bilan des envois","Tous les mails ont été envoyés avec succès.")
    
    return 

    
        