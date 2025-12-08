import tkinter as tk
from tkinter import messagebox
from app.classes.c8_classe_mailConfig import mailConfig


def UI_mail (root )-> mailConfig :
    """
    Ouvre une fenêtre modale Tkinter pour saisir les informations pour configurer le mail.
    """

    # ----------- valeurs par défaut -----------
    
    SMTP_SERVER : str  = "webmail.univ-cotedazur.fr" 
    SMTP_PORT    : int = 587 
    EMAIL_SENDER :str  = "@univ-cotedazur.fr"
    EMAIL_PASSWORD :str =""
    Nom_utilisateur :str = ""
    t_tempo : str = "10"
    
    # ----------- fenêtre modale -----------
    win = tk.Toplevel(root)
    win.title("Saisir vos identifiants pour le mail.")
    win.transient(root)
    win.grab_set()  # fenêtre modale

    # Conteneur principal
    frame = tk.Frame(win, padx=14, pady=12)
    frame.pack(fill="both", expand=True)

    # Champs à afficher : (label, valeur par défaut)
    fields = [
        ("SMTP SERVER", SMTP_SERVER),
        ("SMTP PORT",                SMTP_PORT),
        ("Votre email",            EMAIL_SENDER),
        ("Votre mot de passe",               EMAIL_PASSWORD),
        ("Votre nom d'utilisateur (session)",             Nom_utilisateur),
        ("Temps de pause entre 2 envois de mails (s)",  t_tempo)
        ]

    # Création des widgets de saisie
    vars_ = []
    entries = []
    for i, (lab, val) in enumerate(fields):
        tk.Label(frame, text=lab, anchor="w").grid(row=i, column=0, sticky="w", pady=(0,6))
        v = tk.StringVar(value=val)
        
        # Mot de passe masqué
        if "mot de passe" in lab.lower():
            e = tk.Entry(frame, textvariable=v, width=40, show="*")
        else:
            e = tk.Entry(frame, textvariable=v, width=40)
        e.grid(row=i, column=1, sticky="ew", padx=(8,0), pady=(0,6))
        vars_.append(v)
        entries.append(e)

    frame.grid_columnconfigure(1, weight=1)

    # Résultat final
    result = {"values": None}

    def on_validate(event=None):
        values = tuple(v.get().strip() for v in vars_)

        SMTP_SERVER, SMTP_PORT, EMAIL_SENDER, EMAIL_PASSWORD, Nom_utilisateur, t_tempo = values

        # --- Vérif email correct ---
        if " " in EMAIL_SENDER:
            messagebox.showwarning("Erreur", "courriel incomplet (espaces interdits)")
            return

        if "@" not in EMAIL_SENDER:
            messagebox.showwarning("Erreur", "courriel incomplet (manque @)")
            return

        local, domain = EMAIL_SENDER.split("@", 1)

        if local == "":
            messagebox.showwarning("Erreur", "courriel incomplet (avant @)")
            return

        if domain == "" or "." not in domain:
            messagebox.showwarning("Erreur", "courriel incomplet (domaine manquant)")
            return
        # --- Vérif mot de passe non vide ---
        if EMAIL_PASSWORD == "":
            messagebox.showwarning("Erreur", "mot de passe à saisir")
            return

        # --- Vérif nom d'utilisateur non vide ---
        if Nom_utilisateur == "":
            messagebox.showwarning("Erreur", "nom d'utilisateur à saisir")
            return
        # --- Vérif t_tempo entier ---
        if not t_tempo.isdigit():
            messagebox.showwarning("Erreur", "Le temps doit être un nombre entier !")
            return

        # Conversion de t_tempo en int
        t_tempo_int = int(t_tempo)

        # On reconstruit les valeurs avec t_tempo entier
        result["values"] = (
            SMTP_SERVER,
            SMTP_PORT,
            EMAIL_SENDER,
            EMAIL_PASSWORD,
            Nom_utilisateur,
            t_tempo_int,
        )

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
        return (None,) * 5

    (SMTP_SERVER,
    SMTP_PORT,
    EMAIL_SENDER,
    EMAIL_PASSWORD,
    Nom_utilisateur,
    t_tempo) = result["values"]
    
    
    setUpMail : mailConfig = mailConfig (SMTP_SERVER,SMTP_PORT,EMAIL_SENDER,EMAIL_PASSWORD,Nom_utilisateur,t_tempo)
    
    return setUpMail 


# --------------------------------------------------------------------
#  AUTO-TEST
# --------------------------------------------------------------------
if __name__ == "__main__":

    root = tk.Tk()
    # root.withdraw()  # masque la fenêtre principale
    print(" Ouverture de la fenêtre de saisie des données d'épreuve…")
    valeurs = UI_mail(root)
    print("\nRésultat de la saisie :")
    print(valeurs)

    root.destroy()

