from PIL import ImageGrab

def save_canvas(nom_fichier, canvas):
    """
    Sauvegarde le contenu d'un canvas Tkinter dans un fichier PNG.
    Args:
        nom_fichier (str): Le nom complet du fichier PNG à créer (ex: "./png_out/zone1.png").
        canvas (tk.Canvas): L'objet canvas à capturer.
    """
    # Obtenir les coordonnées du canvas à l'écran
    canvas.update()
    x = canvas.winfo_rootx()
    y = canvas.winfo_rooty()
    w = x + canvas.winfo_width()
    h = y + canvas.winfo_height()

    # Capturer et sauvegarder la zone spécifiée
    img = ImageGrab.grab(bbox=(x, y, w, h))
    img.save(nom_fichier)
