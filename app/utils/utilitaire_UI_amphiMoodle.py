import tkinter as tk
from tkinter import messagebox

def definitRemplissage(nb_etudiants: int, parent: tk.Misc | None = None):
    """
    Ouvre une fenêtre UI pour choisir les amphithéâtres et leurs capacités.
    - En haut : "Placement de N étudiants"
    - Sous le titre : une ligne de TEST dédiée (OK / DEPASSE) -> 'test à part au début'
    - Milieu : cases à cocher + spinbox (entiers) sur la même ligne
    - Bas : total dynamique + boutons Valider/Annuler

    Retourne: list[tuple[str, int]] pour les cases cochées.
    
    Fais avec chatgpt...
    """

    # Ordre et max EXACTS demandés
    amphis_spec = [
        ("Petit_Valrose", 165),
        ("Chimie", 84),
        ("Mathématiques", 84),
        ("Sc_Physiques", 84),
        ("Informatique", 84),
        ("Sc_Naturelles", 84),
        ("Biologie", 25),
        ("Géologie", 25),
    ]

    # --- fenêtre (Toplevel si parent, sinon Tk autonome) ---
    owns_root = False
    if parent is not None:
        win = tk.Toplevel(parent)
        win.transient(parent)
        win.grab_set()
    else:
        win = tk.Tk()
        owns_root = True  # pour détruire le root en fin d’exécution

    win.title("Répartition – amphithéâtres")
    win.resizable(False, False)

    # --- frames ---
    f_top = tk.Frame(win, padx=12, pady=10)
    f_mid = tk.Frame(win, padx=12, pady=6)
    f_bot = tk.Frame(win, padx=12, pady=10)
    f_top.pack(fill="x")
    f_mid.pack(fill="x")
    f_bot.pack(fill="x")

    # --- haut : Titre ---
    tk.Label(
        f_top,
        text=f"Placement de {nb_etudiants} étudiant(s)",
        font=("Arial", 12, "bold")
    ).pack(anchor="w")

    # --- TEST DÉDIÉ (à part au début) ---
    # Affiche l’état du total par rapport à nb_etudiants (OK/DEPASSE)
    frm_test = tk.Frame(f_top)
    frm_test.pack(fill="x", pady=(6, 0), anchor="w")
    
    tk.Label(frm_test, text="Test :", font=("Arial", 10, "bold")).pack(side="left")

    lbl_test = tk.Label(frm_test, text=f"Total = 0 / attendu = {nb_etudiants}")
    lbl_test.pack(side="left", padx=6)

    lbl_reste = tk.Label(frm_test, text=f"Reste à placer : {nb_etudiants}", font=("Arial", 10))
    lbl_reste.pack(side="left", padx=12)

    def maj_test(total: int):
        reste = nb_etudiants - total
        lbl_reste.config(text=f"Reste à placer : {max(reste, 0)}")

        if total == 0:
            lbl_test.config(text=f"Total = 0 / attendu = {nb_etudiants}", fg="black")
        elif total < nb_etudiants:
            lbl_test.config(text=f"OK : Total = {total} / {nb_etudiants}", fg="green")
        elif total == nb_etudiants:
            lbl_test.config(text=f"Parfait  : Total = {total} / {nb_etudiants}", fg="blue")
        else:
            lbl_test.config(text=f"DEPASSE : Total = {total} / {nb_etudiants}", fg="red")


    # --- milieu : cases + spinbox ---
    tk.Label(
        f_mid,
        text="Choisir les amphithéâtres",
        font=("Arial", 11, "bold")
    ).grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 6))

    selections = []  # (nom, vcheck, vint, spin)
    
    total_var = tk.IntVar(value=0)   #   mémoriser le total courant


    def update_total(*_):
        total = 0
        for _, vcheck, vint, _spin in selections:
            if vcheck.get():
                try:
                    total += int(vint.get() or 0)
                except ValueError:
                    pass
        total_var.set(total)
        lbl_total_val.configure(
            text=f"Total = {total} pour {nb_etudiants} étudiant(s) à placer."
        )
        maj_test(total)

    def on_toggle_spin(vcheck: tk.IntVar, vint: tk.StringVar, spin: tk.Spinbox, maxv: int):
        if vcheck.get():
            # Si coché : activer et mettre la valeur max
            spin.configure(state="normal")
            vint.set(str(maxv))
        else:
            # Si décoché : désactiver et remettre à 0
            spin.configure(state="disabled")
            vint.set("0")
        update_total()

    for i, (nom, maxv) in enumerate(amphis_spec, start=1):
        row = i  # la ligne 0 est le titre de section
        vcheck = tk.IntVar(value=0)
        vint = tk.StringVar(value="0")

        # --- Spinbox d'abord ---
        spin = tk.Spinbox(
            f_mid, from_=0, to=maxv, width=6, justify="right",
            textvariable=vint, state="disabled", validate="key"
        )

        def _validate_int(P, max_value=maxv):
            if P == "":
                return True
            if P.isdigit():
                try:
                    return int(P) <= max_value
                except ValueError:
                    return False
            return False

        vcmd = (win.register(_validate_int), "%P")
        spin.configure(validatecommand=vcmd)
        spin.grid(row=row, column=1, sticky="w", padx=(0, 8))

        # Mettre à jour le total dès qu’on tape
        vint.trace_add("write", lambda *_: update_total())

        # --- Puis le Checkbutton (la commande voit bien 'spin' maintenant)
        cb_text = f"{nom} (max={maxv})"
        cb = tk.Checkbutton(
            f_mid, text=cb_text, variable=vcheck,
            command=lambda vc=vcheck, vi=vint, sp=spin, mv=maxv: on_toggle_spin(vc, vi, sp, mv)
        )
        cb.grid(row=row, column=0, sticky="w", padx=(0, 8))

        selections.append((nom, vcheck, vint, spin))


    # --- bas : total + boutons ---
    lbl_total_val = tk.Label(
        f_bot,
        text=f"Total = 0 pour {nb_etudiants} étudiant(s) à placer.",
        font=("Arial", 11)
    )
    lbl_total_val.pack(anchor="w")

    frm_btn = tk.Frame(f_bot)
    frm_btn.pack(anchor="e", pady=(6, 0))

    result = []

    def _ramener_fenetre():
        """Remet la fenêtre devant et le focus sur elle."""
        try:
            win.lift()
            win.focus_force()
            win.bell()
        except Exception:
            pass
        
    def do_validate():
        nonlocal result
        total = total_var.get()

        if total > nb_etudiants:
            messagebox.showwarning(
                "Total trop grand",
                f"Le total ({total}) dépasse le nombre d’étudiants à placer ({nb_etudiants})."
                "\nAjustez les valeurs puis réessayez."
            )
            _ramener_fenetre()
            return

        if total < nb_etudiants:
            messagebox.showwarning(
                "Total insuffisant",
                f"Le total ({total}) est inférieur au nombre d’étudiants à placer ({nb_etudiants})."
                "\nAjustez les valeurs puis réessayez."
            )
            _ramener_fenetre()
            return

        # total == nb_etudiants → OK : on collecte et on ferme
        out = []
        for nom, vcheck, vint, _spin in selections:
            if vcheck.get():
                try:
                    val = int(vint.get() or 0)
                except ValueError:
                    val = 0
                out.append((nom, val))
        result = out
        win.destroy()

    def do_cancel():
        win.destroy()

    tk.Button(frm_btn, text="Annuler", command=do_cancel).pack(side="right", padx=6)
    tk.Button(frm_btn, text="Valider. ", command=do_validate).pack(side="right")

    # Init total + test
    update_total()

    win.protocol("WM_DELETE_WINDOW", do_cancel)
    win.wait_window()  # bloque jusqu’à Valider/Annuler

    if owns_root:
        try:
            win.destroy()
        except Exception:
            pass

    return result


# Petit test autonome (exécution directe du fichier)
if __name__ == '__main__':
    # Exemple : 320 étudiants à placer
    res = definitRemplissage(nb_etudiants=90, parent=None)
    print("Résultat :", res)
