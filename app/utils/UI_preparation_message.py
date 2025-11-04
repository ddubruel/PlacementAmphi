import tkinter as tk
import tkinter.scrolledtext as scrolledtext
from app.classes.c9_classe_dataEpreuve import dataEpreuve

def majContenuMessage(dataEpreuvePourMail : dataEpreuve) -> str :
     

#     # Construction du message personnalisé 
    corps_du_message  = (
    f"Ce message vous rappelle les consignes pour l'examen de l'UE \"{dataEpreuvePourMail.epreuve}\".\n"
    f"Cette épreuve se tiendra le {dataEpreuvePourMail.date} à  {dataEpreuvePourMail.horaires}.\n\n "
        
    "Les étudiants sont placés. La liste des places individuelles sera scotchée "
    "à l'entrée de votre amphithéâtre.\n"
    "Le respect du placement est impératif et de votre responsabilité.\n\n"
    "Vous trouverez en pièce jointe un plan de l'amphithéâtre, avec votre place clairement indiquée.\n\n"
    
    "La signification du code de la place  est la suivante :\n"
    " - la première lettre désigne la zone pour les grands amphithéatre.\n"
    " - le premier nombre désigne le rang dans depuis le bas de l'amphithéâtre.\n"
    " - le dernier chiffre est le numéro de la place dans le rang.\n\n"
    
    
    "Vous devrez ranger votre téléphone portable et tout autre appareil électronique dans votre sac,"
    " lui-même déposé en bas de l'amphithéatre.\n"
    "Tout appareil électronique (téléphone portable, écouteurs, montre connectée, etc) est proscrit. "
    "Si vous êtes en possession de ce type d’appareil , même éteint, pendant l'épreuve, un procès verbal"
    " sera dressé. "
    
    )
    return corps_du_message


def UI_preparation_message (root , dataEpreuvePourMail : dataEpreuve )-> str :
    """
    Ouvre une fenêtre modale Tkinter pour saisir les informations pour configurer le mail.    
    """
    # ----------- valeurs par défaut
    modele_message : str = majContenuMessage( dataEpreuvePourMail )
        
     # ----------- fenêtre modale -----------
    win = tk.Toplevel(root)
    win.title("Préparation du message")
    win.transient(root)
    win.grab_set()
    win.minsize(700, 500)

    # Conteneur principal (partie haute : contenu)
    frame = tk.Frame(win, padx=14, pady=12)
    frame.pack(fill="both", expand=True)

    # 1) Consignes pour l'utilisateur (zone d'aide en haut)
    consignes = (
        "Veuillez vérifier ou modifier les éléments ci-dessous avant l’envoi :\n"
        " • Titre clair (modifiable) pour le mail.\n"
        " • Le contenu du corps du message.\n"
        " • Validez pour enregistrer."
    )
    lbl_consignes = tk.Label(frame, text=consignes, justify="left", anchor="w", wraplength=660)
    lbl_consignes.grid(row=0, column=0, columnspan=2, sticky="nsew", pady=(0, 10))

    # 2) Ligne en gras “Titre du mail”
    lbl_titre_section = tk.Label(frame, text="Titre du mail", anchor="w", font=("TkDefaultFont", 10, "bold"))
    lbl_titre_section.grid(row=1, column=0, columnspan=2, sticky="w", pady=(0, 4))

    # 3) Champ 1 ligne éditable pour le titre
    titre_defaut = f"Epreuve \"{dataEpreuvePourMail.epreuve}\" – {dataEpreuvePourMail.date} - {dataEpreuvePourMail.horaires}  Consignes et placement "
 
    var_titre = tk.StringVar(value=titre_defaut)
    entry_titre = tk.Entry(frame, textvariable=var_titre)
    entry_titre.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(0, 12))

    # 4) Ligne “Corps du message”
    lbl_corps = tk.Label(frame, text="Corps du message", anchor="w")
    lbl_corps.grid(row=3, column=0, columnspan=2, sticky="w", pady=(0, 6))

    # 5) Zone multiligne éditable
    import tkinter.scrolledtext as scrolledtext
    txt_corps = scrolledtext.ScrolledText(frame, width=60, height=18, wrap="word")
    txt_corps.grid(row=4, column=0, columnspan=2, sticky="nsew")
    txt_corps.insert("1.0", modele_message)

    # Rendre le layout extensible
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_columnconfigure(1, weight=1)
    frame.grid_rowconfigure(4, weight=1)
    
    # Résultat final
    result = {"values": None}

    def on_validate(event=None):
        titre_val = var_titre.get().strip()
        corps_val = txt_corps.get("1.0", "end").strip()
        result["values"] = (titre_val, corps_val)
        win.destroy()

    def on_cancel(event=None):
        result["values"] = None 
        win.destroy()

     # ---- Zone de boutons en bas (fixe) ----
    frame_buttons = tk.Frame(win, pady=10)
    frame_buttons.pack(fill="x", side="bottom")

    btn_cancel = tk.Button(frame_buttons, text="Annuler", command=on_cancel)
    btn_validate = tk.Button(frame_buttons, text="Valider", command=on_validate, default="active")
    btn_cancel.pack(side="right", padx=(0, 8))
    btn_validate.pack(side="right")

    # Bindings pratiques
    win.bind("<Return>", on_validate)
    win.bind("<Escape>", on_cancel)

    # Centrage par rapport à la fenêtre principale (identique à ta version)
    win.update_idletasks()
    try:
        rx, ry = root.winfo_rootx(), root.winfo_rooty()
        rw, rh = root.winfo_width(), root.winfo_height()
        ww, wh = win.winfo_width(), win.winfo_height()
        x = rx + (rw - ww)//2
        y = ry + (rh - wh)//2
        win.geometry(f"+{x}+{y}")
    except Exception:
        pass

    # Attente de la fermeture de la fenêtre
    root.wait_window(win)

    # Extraction du résultat
    if result["values"] is None:
        return  None 

    titre, corps = result["values"]
    return titre, corps

def main():
    root = tk.Tk()
    dataEpreuvePourMail: dataEpreuve = dataEpreuve('2nov2025', '14h30', '1h30', 'Initiation Programmation')
    
    print("Ouverture de la fenêtre…")
    titre, corps = UI_preparation_message(root, dataEpreuvePourMail)

    print("\nRésultat de la saisie :")
    print("Titre :", titre)
    print("Corps :\n", corps)

    root.destroy()

# --------------------------------------------------------------------
#  AUTO-TEST
# --------------------------------------------------------------------
if __name__ == "__main__":
        # rien ici (laisser vide), on exécutera depuis le lanceur
    pass

    


