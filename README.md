# Placement Étudiants

Application Python (Tkinter) permettant de **placer les étudiants dans les amphithéâtres** à partir de fichiers CSV, puis de **générer les documents nécessaires aux examens** (listes d'émargement, mails personnalisés, etc.).
---

##  Fonctionnalités

- Charge des fichiers CSV issus de :
  - **Moodle**
  - **ADE**
  - **Apogée**
- Définit automatiquement le **placement des étudiants dans les amphis**
- Génère les **listes d'émargement au format PDF**
- Envoie un **mail personnalisé à chaque étudiant**
- Interface graphique basée sur **Tkinter**

---

##  Installation

Avec la version python 3.11.2
1) créer un environnement virtuel
python -m venv NomDeVotreEnvironnement

2) activer l'environnement virtuel:
source NomDeVotreEnvironnement/bin/activate

3)installer les requis :
pip install -r requirements.txt

4)lancer le code dans l'environement virtuel
python mainClasse2.py


###  Prérequis

- Python 3.11.2
- `pip` installé
- (Recommandé) Un environnement virtuel

###  Récupérer le projet

git clone https://github.com/ddubruel/PlacementAmphi

####
Avant le lancement il est recomandé de mettre les fichiers de données
dans un même répertoire.

Le code va créer par exemple l'arborescence contenant tous les fichiers de sortie.


├── Amphi_Chimie
│   ├── listes_Emargement_pdf
│   │   ├── Chimie.pdf
│   ├── pngOut
│   │   ├── Chimie_A-11-1.png
│   │   ├── Chimie_A-11-3.png
.../..
│   │   ├── Chimie_B-9-4.png
│   │   └── Chimie_plan_general.png
│   └── texOut
│       ├── Chimie.tex
│       ├── table_alpha.tex
│       └── table.tex
├── Amphi_Informatique
│   ├── listes_Emargement_pdf
│   │   ├── Chimie.pdf
│   ├── pngOut
│   │   ├── Chimie_A-11-1.png
│   │   ├── Chimie_A-11-3.png
.../..
│   │   ├── Chimie_B-9-4.png
│   │   └── Chimie_plan_general.png
│   └── texOut
│       ├── Chimie.tex
│       ├── table_alpha.tex
│       └── table.tex


En complément à côté des fichiers de données initiales vous trouverez les fichiers suivants  contenant le statut d'envoi des mails.

├─etudiants_a_effacer_dans_moodle.csv                                       ├──Z_etudiants_avec_mail_envoyes.csv                                        |──Z_etudiants_avec_mail_NON_envoyes.csv
