import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

from app.classes.c8_classe_mailConfig import mailConfig

def attach_file(msg: MIMEMultipart, file_path: str | None) -> None:
    """Ajoute une pièce jointe au mail si le fichier existe."""
    if not file_path:
        return
    try:
        if not os.path.exists(file_path):
            print(f"[PJ] Fichier non trouvé : {file_path} (pas de pièce jointe).")
            return

        with open(file_path, "rb") as f:
            part = MIMEApplication(f.read(), Name=os.path.basename(file_path))
        part["Content-Disposition"] = f'attachment; filename="{os.path.basename(file_path)}"'
        msg.attach(part)

    except Exception as e:
        print(f"[PJ] Erreur lors de l'ajout de la pièce jointe '{file_path}': {e}")
        
def send_email_via_smtp(
                        receiver_email: str,
                        subject: str,
                        body_text: str,
                        cfg: mailConfig,
                        attachment_path: str | None = None,
                         ) -> bool:
    """Envoie un email via SMTP à partir de la config fournie."""
    try:
        msg = MIMEMultipart()
        msg["From"] = cfg.EMAIL_SENDER
        msg["To"] = receiver_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body_text, "plain"))

        attach_file(msg, attachment_path)

        with smtplib.SMTP(cfg.SMTP_SERVER, cfg.SMTP_PORT) as server:
            server.starttls()
            server.login(cfg.Nom_utilisateur, cfg.EMAIL_PASSWORD)
            server.sendmail(cfg.EMAIL_SENDER, receiver_email, msg.as_string())
        return True
    except Exception as e:
        print(f"[SMTP] Échec de l'envoi à {receiver_email}: {e}")
        return False        


def envoyerMail(sujet : str ,
                corpsDuMessage : str ,
                email : str,                       
                fichierPng : str,
                setUpMail : mailConfig,
                go: bool = False
                ) -> bool:                
    """
    Prépare et envoie un email avec pièce jointe (optionnelle) en utilisant la config SMTP fournie.
    go=False → mode développement (n'envoie pas, affiche seulement).
    """
    
    if not email or "@" not in email:
        print("[CHK] Adresse email invalide.")
        return False
    if not go:
        print("=== DRY-RUN (go=False) ===")
        print(f"To: {email}")
        print(f"Subject: {sujet}")
        print("body:")
        print(corpsDuMessage)
        if fichierPng:
            print(f"Pièce jointe (si existe) : {fichierPng}")
        print("==========================")
        return True
    
    statut : bool = send_email_via_smtp(
                                            receiver_email=email,
                                            subject=sujet,
                                            body_text=corpsDuMessage,
                                            cfg=setUpMail,
                                            attachment_path=fichierPng,
    )
    return statut

def main():
    cfg = mailConfig(
        EMAIL_PASSWORD=input(" Entrer le mot de passe : ")   
    )

    ok = envoyerMail(   sujet = "news",                        
                        corpsDuMessage="Quoi de neuf ?",
                        email="denis.dubruel@gmail.com",
                        fichierPng="/home/denis/00_Universite/BousGit/GenerateurMoodleApogee/Amphi_Sc_Physiques/pngOut/Sc_Physiques_plan_general.png",
                        setUpMail=cfg,
                        go=True,   # True : envoie vraiment le mail False : tir à blanc!
                    )
    print(f"[AUTO-TEST] Résultat: {ok}")
if __name__ == "__main__":
    pass  # revenir à la racine et lancer test_utilitaire etc pour l'import des classes correct