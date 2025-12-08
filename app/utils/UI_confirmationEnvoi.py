# UI_confirmationEnvoi.py
import tkinter as tk
from tkinter import messagebox


def UI_confirmationEnvoi(parent: tk.Tk | tk.Toplevel | None = None):
    """
    Fenêtre modale "envoi message".
    1) "cocher une case"
    2) Check "Envoi réel" / "Test à blanc" (exclusifs)
    3) Boutons :
        - "confirmation" (actif si Envoi réel)
        - "Faire le test" (actif si Test à blanc)

    Logique de retour :
    - Envoi réel > Confirmation > Oui  -> return True
    - Envoi réel > Confirmation > Non  -> reste ouvert ET revient à l'état initial (cases décochées, boutons off)
    - Test à blanc > Faire le test     -> return False
    - Fermeture sans action            -> None
    """
    # Fenêtre modale
    win = tk.Toplevel(parent) if parent else tk.Tk()
    win.title("envoi message")
    win.resizable(False, False)

    if parent:
        win.transient(parent)
        win.grab_set()

    # État
    mode_var = tk.StringVar(value="")  # "", "reel", "test"
    result = {"value": None}

    # ---- Callbacks ----
    def set_mode(new_mode: str):
        mode_var.set(new_mode)
        update_buttons()

    def reset_to_initial():
        """Revient à l'écran 'Cocher une case' : décoche tout et désactive les boutons."""
        var_reel.set(False)
        var_test.set(False)
        mode_var.set("")
        update_buttons()

    def update_buttons(*_):
        mode = mode_var.get()
        if mode == "reel":
            btn_confirm.config(state=tk.NORMAL)
            btn_test.config(state=tk.DISABLED)
        elif mode == "test":
            btn_confirm.config(state=tk.DISABLED)
            btn_test.config(state=tk.NORMAL)
        else:
            btn_confirm.config(state=tk.DISABLED)
            btn_test.config(state=tk.DISABLED)

    def do_test():
        # "Faire le test" -> renvoie False désormais
        result["value"] = False
        win.destroy()

    def do_confirm():
        # Confirmation pour "Envoi réel"
        if messagebox.askyesno("Confirmation", "Confirmez vous l'envoi des messages ?", parent=win):
            result["value"] = True
            win.destroy()
        else:
            # NON -> revenir à l'état "Cocher une case"
            reset_to_initial()

    def on_close():
        win.destroy()

    # ---- UI ----
    # Ligne 1
    row1 = tk.Frame(win, padx=10, pady=8)
    row1.pack(fill="x")
    tk.Label(row1, text="cocher une case", font=("Arial", 11)).pack(anchor="w")

    # Ligne 2 : cases exclusives
    row2 = tk.Frame(win, padx=10, pady=4)
    row2.pack(fill="x")

    var_reel = tk.BooleanVar(value=False)
    var_test = tk.BooleanVar(value=False)

    def on_reel_toggle():
        if var_reel.get():
            var_test.set(False)
            set_mode("reel")
        else:
            mode_var.set("")
            update_buttons()

    def on_test_toggle():
        if var_test.get():
            var_reel.set(False)
            set_mode("test")
        else:
            mode_var.set("")
            update_buttons()

    cb_reel = tk.Checkbutton(row2, text="Envoi réel", variable=var_reel, command=on_reel_toggle)
    cb_reel.pack(side="left", padx=(0, 20))

    cb_test = tk.Checkbutton(row2, text="Test à blanc", variable=var_test, command=on_test_toggle)
    cb_test.pack(side="left")

    # Ligne 3 : boutons
    row3 = tk.Frame(win, padx=10, pady=10)
    row3.pack(fill="x")

    btn_confirm = tk.Button(row3, text="confirmation", width=14, command=do_confirm, state=tk.DISABLED)
    btn_confirm.pack(side="left")

    btn_test = tk.Button(row3, text="Faire le test", width=14, command=do_test, state=tk.DISABLED)
    btn_test.pack(side="left", padx=(10, 0))

    # Bind fermeture
    win.protocol("WM_DELETE_WINDOW", on_close)

    # Position (optionnel : centrer sur le parent)
    win.update_idletasks()
    try:
        if parent:
            px, py = parent.winfo_rootx(), parent.winfo_rooty()
            pw, ph = parent.winfo_width(), parent.winfo_height()
            ww, wh = win.winfo_width(), win.winfo_height()
            x = px + (pw - ww) // 2
            y = py + (ph - wh) // 2
            win.geometry(f"+{x}+{y}")
    except Exception:
        pass

    # Attente modale
    if parent:
        win.wait_window()
        return result["value"]
    else:
        win.mainloop()
        return result["value"]


# Démo rapide
if __name__ == "__main__":
    root = tk.Tk()
    #root.withdraw()
    ret = UI_confirmationEnvoi(root)
    root.destroy()
    print("Retour UI_confirmationEnvoi:", ret)
