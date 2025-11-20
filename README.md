# Placement Étudiants

Application Python (Tkinter) permettant de **placer les étudiants dans les amphithéâtres** à partir de fichiers CSV, puis de **générer les documents nécessaires aux examens** (listes d'émargement, mails personnalisés, etc.).
---

##  Fonctionnalités

- Charge des fichiers CSV issus de :
  - **Moodle**
  - **ADE**
  - **Apogée**
- Définit automatiquement le **placement des étudiants dans les amphis**.
- Génère les **listes d'émargement au format PDF**.
- Envoie un **mail personnalisé à chaque étudiant**.
- Interface graphique basée sur **Tkinter**.


- 📄 Listes d’émargement (PDF)
- ✉️ Envoi de mails personnalisés
- 🏛️ Plans d’amphis exportés en images
- 📁 Arborescence organisée par épreuve

###  Prérequis

- **Python 3.11.2**
- `pip` installé
- (Recommandé) Un environnement virtuel


###  Récupérer le projet

```bash
git clone https://github.com/ddubruel/PlacementAmphi
```

##  Installation standard :

Avec la version python **3.11.2**
```bash
#1 créer un environnement virtuel
python -m venv NomDeVotreEnvironnement

#2 activer l'environnement virtuel:
source NomDeVotreEnvironnement/bin/activate # Linux/Mac
# ou pour windows :
# NomDeVotreEnvironnement\Scripts\activate     # Windows

#3 installer les dépendances requises  :
pip install -r requirements.txt

#4 Vérifier la version de Python installée
which python3
python3 -V

#5 vérifier si tkinter est installé :
python3 -c "import tkinter; print(tkinter)"
```

tkinter n'est pas toujours installé sur macOS :

[Télécharger Python pour macOS](https://www.python.org/downloads/macos/)

[Téléccharger Python 3.11.2 pour macOS](https://www.python.org/downloads/release/python-3112/)

```bash
# lancer le code dans l'environnement virtuel activé
python mainClasse2.py
```
Si l'installation standard ne fonctionne pas sur macOs, utiliser l'installation suivante avec Miniconda.

### 🍏   sur macOS (si l’installation standard échoue)

#### Téléchargement et installation de Miniconda :

#### **👉 macOS Intel**
```bash
cd ~
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh
bash Miniconda3-latest-MacOSX-x86_64.sh
```

#### **👉 macOS Apple Silicon (M1/M2/M3)**
```bash
cd ~
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-arm64.sh
bash Miniconda3-latest-MacOSX-arm64.sh
```

#### Initialiser conda  dans votre shell :

```bash
# en fonction de votre shell :
source ~/.zshrc
# source  ~/.bashrc
# pour vérifier si Conda est bien disponible (affiche juste la version) :
conda --version
```

#### Créer l’environnement Conda sur macOS :

environment.yml est un des fichiers du dépôt.

```bash
cd /chemin/vers/ton/projet
conda env create -f environment.yml
```

#### Activer l'environnement virtuel :

```bash
conda activate placement-etudiants
```

Lancer le code :
```bash
python mainClasse2.py
```

## RECOMMANDATIONS
Avant le lancement il est recommandé de mettre les fichiers de données
dans un même répertoire.

Le code va créer  l'arborescence contenant tous les fichiers de sortie.

Part exemple ici le cas de 2 fichiers Moodle pour un partiel, la liste principale avec 50 étudiants, et la liste des étudiants avec tiers temps :
```text
├── Moodle_50_etu.csv
├── MoodleTiersTemps_10_etu.csv
```


Dans le même répertoire  que les fichiers de données, le programme crée l'arborescence suivante avec les
différents fichier de sortie. Comme le plan général des amphithéatres, les plans individuels par étudiant , les fichier LaTeX, la liste d'émargement en pdf.
```text
├── Amphi_Géologie
│   ├── listes_Emargement_pdf
│   │   └── Géologie.pdf
│   ├── pngOut
│   │   └── Géologie_plan_general.png
│   └── texOut
│       ├── Géologie.tex
│       ├── table_alpha.tex
│       └── table.tex
└─ Amphi_Informatique
    ├── listes_Emargement_pdf
    │   └── Informatique.pdf
    ├── pngOut
    │   └── Informatique_plan_general.png
    └── texOut
        ├── Informatique.tex
        ├── table_alpha.tex
        └── table.tex
```

En complément à côté des fichiers de données initiaux le code écrit les fichiers avec le  statut d'envoi des mails, si l'utilisateur souhaite envoyer les messages en plusieurs fois.

```text
├─Z_etudiants_avec_mail_envoyes.csv
├─Z_etudiants_avec_mail_NON_envoyes.csv
```
Eventuellement un fichier de comparaison entre les données ADE(si fournies) et Moodle.

├─Z_etudiants_dans_moodle_mais_pas_dans_ADE.csv
