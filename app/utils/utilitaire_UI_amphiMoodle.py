import tkinter as tk
from tkinter import messagebox

def definitRemplissage(nb_etudiants: int, nb_tiers_temps: int, parent: tk.Misc | None = None):
    """
    Répartition des étudiants par amphithéâtre, avec un amphi 'Tiers-temps' (TT) unique.

    Spécifications:
      - Coche Amphi: n'affecte PAS la valeur; active/désactive seulement la spinbox.
      - Coche TT: n'affecte PAS la valeur NI le max affiché; TT est unique.
      - Colonne 'Max' = capacité de base (inchangée, même si TT).
      - Total/Reste: une ligne compte si Amphi cochée OU TT cochée.
      - Sortie: [(nom_amphi, valeur, is_tiers_temps), ...]
    """

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

    # --- fenêtre ---
    owns_root = False
    if parent is not None:
        win = tk.Toplevel(parent)
        win.transient(parent)
        win.grab_set()
    else:
        win = tk.Tk()
        owns_root = True

    win.title("Répartition – amphithéâtres")
    win.resizable(False, False)

    # --- frames ---
    f_top = tk.Frame(win, padx=12, pady=10)
    f_mid = tk.Frame(win, padx=12, pady=6)
    f_bot = tk.Frame(win, padx=12, pady=10)
    f_top.pack(fill="x")
    f_mid.pack(fill="x")
    f_bot.pack(fill="x")

    # --- Titre ---
    tk.Label(
        f_top,
        text=f"Placement de {nb_etudiants} étudiant(s) — TT ({nb_tiers_temps})",
        font=("Arial", 12, "bold")
    ).pack(anchor="w")

    # --- Test/Reste ---
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
            lbl_test.config(text=f"Parfait : Total = {total} / {nb_etudiants}", fg="blue")
        else:
            lbl_test.config(text=f"DEPASSE : Total = {total} / {nb_etudiants}", fg="red")

    # --- entêtes ---
    tk.Label(f_mid, text="Amphi").grid(row=0, column=0, sticky="w", padx=(0, 8))
    tk.Label(f_mid, text="TT").grid(row=0, column=1, sticky="w", padx=(0, 8))
    tk.Label(f_mid, text="Valeur").grid(row=0, column=2, sticky="w", padx=(0, 8))
    tk.Label(f_mid, text="Max").grid(row=0, column=3, sticky="w", padx=(0, 8))

    # (nom, max_base, vAmphi, vTT, vInt, spin, lbl_max, cb_amphi)
    selections = []
    total_var = tk.IntVar(value=0)
    tt_index = {"idx": None}  # index de la ligne TT (unique), None si aucun

    def update_total(*_):
        """Somme des valeurs des lignes où Amphi OU TT est coché."""
        total = 0
        for nom, max_base, vA, vTT, vInt, _spin, _lbl_max, _cb in selections:
            if vA.get() or vTT.get():
                try:
                    total += int(vInt.get() or 0)
                except ValueError:
                    pass
        total_var.set(total)
        lbl_total_val.config(text=f"Total = {total} pour {nb_etudiants} étudiant(s) à placer.")
        maj_test(total)

    # --- Gestion Amphi : activer/désactiver saisie uniquement ---
    def on_toggle_amphi(idx: int):
        nom, max_base, vA, vTT, vInt, spin, lbl_max, cb = selections[idx]
        spin.configure(state=("normal" if vA.get() else "disabled"))
        update_total()

    # --- Gestion TT : unique, sans effet sur valeur ni max ---
    def on_click_tt(idx_clicked: int):
        idx_old = tt_index["idx"]
        nom_c, max_base_c, vA_c, vTT_c, vInt_c, spin_c, lbl_max_c, cb_c = selections[idx_clicked]

        if idx_old is None:
            # activer TT sur la ligne cliquée
            vTT_c.set(1)
            tt_index["idx"] = idx_clicked
            update_total()
            return

        if idx_old == idx_clicked:
            # retirer TT
            vTT_c.set(0)
            tt_index["idx"] = None
            update_total()
            return

        # transfert : retirer l'ancien et activer le nouveau
        nom_o, max_base_o, vA_o, vTT_o, vInt_o, spin_o, lbl_max_o, cb_o = selections[idx_old]
        vTT_o.set(0)
        vTT_c.set(1)
        tt_index["idx"] = idx_clicked
        update_total()

    # --- Création des lignes ---
    for i, (nom, max_base) in enumerate(amphis_spec, start=1):
        row = i
        vA  = tk.IntVar(value=0)
        vTT = tk.IntVar(value=0)
        vInt = tk.StringVar(value="0")

        # Spinbox (bornée au max de base, jamais modifié par TT)
        spin = tk.Spinbox(
            f_mid, from_=0, to=max_base, width=6, justify="right",
            textvariable=vInt, state="disabled", validate="key"
        )

        def _validate_int(P, max_b=max_base):
            if P == "":
                return True
            if P.isdigit():
                try:
                    return int(P) <= max_b
                except ValueError:
                    return False
            return False

        vcmd = (win.register(_validate_int), "%P")
        spin.configure(validatecommand=vcmd)
        spin.grid(row=row, column=2, sticky="w", padx=(0, 8))
        vInt.trace_add("write", lambda *_: update_total())

        # Label Max (affiche le max de base, constant)
        lbl_max = tk.Label(f_mid, text=str(max_base))
        lbl_max.grid(row=row, column=3, sticky="w", padx=(0, 8))

        # Checkbutton Amphi
        cb_amphi = tk.Checkbutton(
            f_mid, text=nom, variable=vA,
            command=lambda idx=i-1: on_toggle_amphi(idx)
        )
        cb_amphi.grid(row=row, column=0, sticky="w", padx=(0, 8))

        # Checkbutton TT (unique, passif)
        cb_tt = tk.Checkbutton(
            f_mid, text="", variable=vTT,
            command=lambda idx=i-1: on_click_tt(idx)
        )
        cb_tt.grid(row=row, column=1, sticky="w", padx=(0, 8))

        selections.append([nom, max_base, vA, vTT, vInt, spin, lbl_max, cb_amphi])

    # --- Bas de page ---
    lbl_total_val = tk.Label(
        f_bot,
        text=f"Total = 0 pour {nb_etudiants} étudiant(s) à placer.",
        font=("Arial", 11)
    )
    lbl_total_val.pack(anchor="w")

    frm_btn = tk.Frame(f_bot)
    frm_btn.pack(anchor="e", pady=(6, 0))

    result = []

    def do_validate():
        nonlocal result
        total = total_var.get()
        if total > nb_etudiants:
            messagebox.showwarning(
                "Total trop grand",
                f"Le total ({total}) dépasse {nb_etudiants}."
            )
            return
        if total < nb_etudiants:
            messagebox.showwarning(
                "Total insuffisant",
                f"Le total ({total}) est inférieur à {nb_etudiants}."
            )
            return

        out = []
        for nom, _max_base, vA, vTT, vInt, _spin, _lbl_max, _cb in selections:
            if vA.get() or vTT.get():
                try:
                    val = int(vInt.get() or 0)
                except ValueError:
                    val = 0
                out.append((nom, val, bool(vTT.get())))
        result = out
        win.destroy()

    def do_cancel():
        win.destroy()

    tk.Button(frm_btn, text="Annuler", command=do_cancel).pack(side="right", padx=6)
    tk.Button(frm_btn, text="Valider", command=do_validate).pack(side="right")

    # --- Init ---
    update_total()

    win.protocol("WM_DELETE_WINDOW", do_cancel)
    win.wait_window()

    if owns_root:
        try:
            win.destroy()
        except Exception:
            pass

    return result


# Test autonome
if __name__ == "__main__":
    res = definitRemplissage(nb_etudiants=90, nb_tiers_temps=12, parent=None)
    print("Résultat :", res)
