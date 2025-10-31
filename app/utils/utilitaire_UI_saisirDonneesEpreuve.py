import tkinter as tk

def UI_saisirDonneesEpreuve(root )-> list[str]:
    """
    Ouvre une fenêtre modale Tkinter pour saisir les informations de l'épreuve.
    Retourne un tuple :
    (annee_universitaire, date, horaires, duree, salle, lieu, batiment, epreuve)
    """

    # ----------- valeurs par défaut -----------
    default_annee   = "ANNEE UNIVERSITAIRE 2025/2026"
    default_date    = ""              
    default_horaires= ""              
    default_duree   = "2h00"          
    default_epreuve = "informatique"

    # ----------- fenêtre modale -----------
    win = tk.Toplevel(root)
    win.title("Saisir les informations de l'épreuve")
    win.transient(root)
    win.grab_set()  # fenêtre modale

    # Conteneur principal
    frame = tk.Frame(win, padx=14, pady=12)
    frame.pack(fill="both", expand=True)

    # Champs à afficher : (label, valeur par défaut)
    fields = [
        ("Année universitaire", default_annee),
        ("Date",                default_date),
        ("Horaires",            default_horaires),
        ("Durée",               default_duree),
        ("Épreuve",             default_epreuve),
    ]

    # Création des widgets de saisie
    vars_ = []
    entries = []
    for i, (lab, val) in enumerate(fields):
        tk.Label(frame, text=lab, anchor="w").grid(row=i, column=0, sticky="w", pady=(0,6))
        v = tk.StringVar(value=val)
        e = tk.Entry(frame, textvariable=v, width=40)
        e.grid(row=i, column=1, sticky="ew", padx=(8,0), pady=(0,6))
        vars_.append(v)
        entries.append(e)

    frame.grid_columnconfigure(1, weight=1)

    # Résultat final
    result = {"values": None}

    def on_validate(event=None):
        result["values"] = tuple(v.get().strip() for v in vars_)
        win.destroy()

    def on_cancel(event=None):
        result["values"] = (None,) * 8
        win.destroy()

    # Boutons
    btns = tk.Frame(frame, pady=6)
    btns.grid(row=len(fields), column=0, columnspan=2, sticky="e")

    btn_cancel = tk.Button(btns, text="Annuler", command=on_cancel)
    btn_validate = tk.Button(btns, text="Valider", command=on_validate, default="active")
    btn_cancel.pack(side="right", padx=(0,8))
    btn_validate.pack(side="right")

    # Bindings pratiques
    win.bind("<Return>", on_validate)
    win.bind("<Escape>", on_cancel)

    # Focus sur le premier champ
    entries[1].focus_set()

    # Centrage par rapport à la fenêtre principale
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
        return (None,) * 8

    (annee_universitaire,
     date,
     horaires,
     duree,
     epreuve) = result["values"]

    return annee_universitaire, date, horaires, duree, epreuve


# --------------------------------------------------------------------
#  AUTO-TEST
# --------------------------------------------------------------------
if __name__ == "__main__":

    root = tk.Tk()
   # root.withdraw()  # masque la fenêtre principale


    print(" Ouverture de la fenêtre de saisie des données d'épreuve…")
    valeurs = UI_saisirDonneesEpreuve(root, 'Mathématiques')
    print("\nRésultat de la saisie :")
    print(valeurs)

    root.destroy()
